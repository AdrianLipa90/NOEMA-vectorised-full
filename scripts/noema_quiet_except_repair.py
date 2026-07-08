#!/usr/bin/env python3
"""Make quiet exception handlers observable without changing their control flow."""

from __future__ import annotations

import ast
import json
import logging as _noema_quiet_logging
from collections import defaultdict
from pathlib import Path

_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "QUIET_EXCEPT_AUDIT.json"
REPORT_JSON = ROOT / "QUIET_EXCEPT_REPAIR.json"
LOGGER_IMPORT = "import logging as _noema_quiet_logging"
LOGGER_BIND = "_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)"


def _line_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" \t"))]


def _support_insert_index(source: str) -> int:
    tree = ast.parse(source)
    lines = source.splitlines()
    idx = 0

    if lines and lines[0].startswith("#!"):
        idx = 1
    if len(lines) > idx and "coding" in lines[idx] and lines[idx].lstrip().startswith("#"):
        idx += 1

    body = list(tree.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        idx = max(idx, int(getattr(body[0], "end_lineno", body[0].lineno)))
        body = body[1:]

    for node in body:
        if (
            isinstance(node, ast.ImportFrom)
            and node.module == "__future__"
            and int(getattr(node, "lineno", 0)) >= idx
        ):
            idx = max(idx, int(getattr(node, "end_lineno", node.lineno)))
            continue
        break

    return idx


def _has_logger_support(source: str) -> bool:
    return LOGGER_BIND in source


def _repair_file(path: Path, items: list[dict[str, object]]) -> dict[str, object]:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    changed = False
    inserted_handlers = 0

    for item in sorted(items, key=lambda item: int(item["line"]), reverse=True):
        except_line_no = int(item["line"])
        end_line_no = int(item.get("end_line") or except_line_no)
        if except_line_no < 1 or except_line_no > len(lines):
            continue

        window = lines[except_line_no:end_line_no]
        if any("_NOEMA_QUIET_EXCEPT_LOGGER.exception(" in line for line in window):
            continue

        rel = path.relative_to(ROOT).as_posix()
        scope = str(item.get("scope") or "<module>").replace("\\", "\\\\").replace('"', '\\"')
        reason = str(item.get("reason") or "quiet").replace("\\", "\\\\").replace('"', '\\"')
        message = f"{rel}:{except_line_no} quiet except scope={scope} reason={reason}"

        header_end_idx = except_line_no - 1
        while header_end_idx < len(lines) and ":" not in lines[header_end_idx]:
            header_end_idx += 1
        if header_end_idx >= len(lines):
            continue

        except_line = lines[header_end_idx]
        header, colon, trailing = except_line.partition(":")
        if colon and trailing.strip():
            body_indent = _line_indent(except_line) + "    "
            lines[header_end_idx] = f"{header}:"
            log_line = f'{body_indent}_NOEMA_QUIET_EXCEPT_LOGGER.exception("{message}")'
            lines.insert(header_end_idx + 1, f"{body_indent}{trailing.strip()}")
            lines.insert(header_end_idx + 1, log_line)
            changed = True
            inserted_handlers += 1
            continue

        body_indent = None
        for candidate in lines[header_end_idx + 1:end_line_no]:
            if candidate.strip() and not candidate.lstrip().startswith("#"):
                body_indent = _line_indent(candidate)
                break
        if body_indent is None:
            body_indent = _line_indent(lines[header_end_idx]) + "    "

        log_line = f'{body_indent}_NOEMA_QUIET_EXCEPT_LOGGER.exception("{message}")'
        lines.insert(header_end_idx + 1, log_line)
        changed = True
        inserted_handlers += 1

    if changed and not _has_logger_support("\n".join(lines)):
        current = "\n".join(lines) + ("\n" if source.endswith("\n") else "")
        insert_idx = _support_insert_index(current)
        lines = current.splitlines()
        block = [LOGGER_IMPORT, LOGGER_BIND, ""]
        lines[insert_idx:insert_idx] = block

    if changed:
        path.write_text("\n".join(lines) + ("\n" if source.endswith("\n") else ""), encoding="utf-8")

    return {
        "path": path.relative_to(ROOT).as_posix(),
        "inserted_handlers": inserted_handlers,
        "changed": changed,
    }


def main() -> int:
    audit = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in audit.get("items", []):
        rel = str(item.get("path") or "")
        if rel.endswith(".py"):
            grouped[rel].append(item)

    results = []
    parse_failures = []
    for rel, items in sorted(grouped.items()):
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            results.append(_repair_file(path, items))
        except SyntaxError as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_quiet_except_repair.py quiet except scope=main reason=parse_failure")
            parse_failures.append({"path": rel, "error": repr(exc)})

    changed_files = [item for item in results if item["changed"]]
    report = {
        "audit": str(AUDIT_JSON),
        "files_considered": len(grouped),
        "files_changed": len(changed_files),
        "handlers_instrumented": sum(int(item["inserted_handlers"]) for item in changed_files),
        "parse_failures": parse_failures,
        "changed_files": changed_files,
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("files_considered", "files_changed", "handlers_instrumented", "parse_failures")}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
