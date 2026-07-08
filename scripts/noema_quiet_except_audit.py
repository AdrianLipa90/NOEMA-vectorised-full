#!/usr/bin/env python3
"""NOEMA AST audit for quiet exception handlers.

The audit does not use grep-like text matching. It parses Python files with
`ast` and reports exception handlers that swallow errors without logging or
raising.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import ast
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(os.environ.get("NOEMA_ROOT", Path(__file__).resolve().parent.parent))
REPORT_MD = ROOT / "QUIET_EXCEPT_AUDIT.md"
REPORT_JSON = ROOT / "QUIET_EXCEPT_AUDIT.json"

EXCLUDE_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    "build",
    "dist",
    "site-packages",
    "raw-sessions",
}

LOG_OR_RAISE_NAMES = {
    "breakpoint",
    "critical",
    "debug",
    "error",
    "exception",
    "info",
    "log",
    "logger",
    "logging",
    "print",
    "raise",
    "traceback",
    "warn",
    "warning",
    "warnings",
}


def _skip(path: Path) -> bool:
    return any(part in EXCLUDE_PARTS for part in path.parts)


def _segment(source: str, node: ast.AST | None) -> str:
    if node is None:
        return "None"
    try:
        text = ast.get_source_segment(source, node) or ast.unparse(node)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_quiet_except_audit.py:64 quiet except scope=_segment reason=assign_fallback")
        text = ast.dump(node)
    return " ".join(text.strip().split())[:220]


def _exception_name(node: ast.AST | None) -> str:
    if node is None:
        return "bare"
    try:
        return ast.unparse(node)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_quiet_except_audit.py:74 quiet except scope=_exception_name reason=return ast.dump(node)")
        return ast.dump(node)


def _is_logging_or_raise(node: ast.AST) -> bool:
    if isinstance(node, ast.Raise):
        return True
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in LOG_OR_RAISE_NAMES
    if isinstance(func, ast.Attribute):
        if func.attr in LOG_OR_RAISE_NAMES:
            return True
        if isinstance(func.value, ast.Name):
            return func.value.id in LOG_OR_RAISE_NAMES
    return False


def _handler_has_logging_or_raise(handler: ast.ExceptHandler) -> bool:
    for stmt in handler.body:
        for node in ast.walk(stmt):
            if _is_logging_or_raise(node):
                return True
    return False


def _body_action(stmt: ast.stmt | None, source: str) -> str:
    if stmt is None:
        return "empty"
    if isinstance(stmt, ast.Pass):
        return "pass"
    if isinstance(stmt, ast.Continue):
        return "continue"
    if isinstance(stmt, ast.Break):
        return "break"
    if isinstance(stmt, ast.Return):
        return "return " + _segment(source, stmt.value)
    if isinstance(stmt, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        return "assign_fallback"
    return type(stmt).__name__


def _quiet_reason(handler: ast.ExceptHandler, source: str) -> str | None:
    if _handler_has_logging_or_raise(handler):
        return None
    if not handler.body:
        return "empty_handler"
    if len(handler.body) == 1:
        return _body_action(handler.body[0], source)
    return "no_log_no_raise"


def _scope_for(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> str:
    scope: list[str] = []
    current = node
    while current in parents:
        current = parents[current]
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            scope.append(current.name)
    return ".".join(reversed(scope))


def _scan_file(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    rel = path.relative_to(ROOT).as_posix()
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(path))
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_quiet_except_audit.py:143 quiet except scope=_scan_file reason=return [], {\"path\": rel, \"error\": repr(exc)}")
        return [], {"path": rel, "error": repr(exc)}

    parents: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node

    lines = source.splitlines()
    findings: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        reason = _quiet_reason(node, source)
        if reason is None:
            continue
        line = node.lineno
        findings.append(
            {
                "path": rel,
                "line": line,
                "end_line": getattr(node, "end_lineno", line),
                "scope": _scope_for(node, parents),
                "exception": _exception_name(node.type),
                "reason": reason,
                "body": _body_action(node.body[0] if node.body else None, source),
                "source": lines[line - 1].strip() if 0 < line <= len(lines) else "",
            }
        )
    return findings, None


def run_audit() -> dict[str, Any]:
    files = sorted(path for path in ROOT.rglob("*.py") if not _skip(path))
    findings: list[dict[str, Any]] = []
    parse_errors: list[dict[str, Any]] = []
    for path in files:
        file_findings, parse_error = _scan_file(path)
        findings.extend(file_findings)
        if parse_error:
            parse_errors.append(parse_error)

    findings.sort(key=lambda item: (item["path"], item["line"]))
    by_reason = Counter(item["reason"].split()[0] for item in findings)
    by_top = Counter(item["path"].split("/")[0] for item in findings)
    by_file = Counter(item["path"] for item in findings)

    payload = {
        "root": str(ROOT),
        "files_scanned": len(files),
        "quiet_except_count": len(findings),
        "parse_errors": parse_errors,
        "by_reason": by_reason.most_common(),
        "by_top_directory": by_top.most_common(),
        "worst_files": by_file.most_common(),
        "items": findings,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Quiet Except Audit",
        "",
        f"- root: `{ROOT}`",
        f"- files scanned: `{len(files)}`",
        f"- quiet except handlers: `{len(findings)}`",
        f"- parse errors: `{len(parse_errors)}`",
        "",
        "## Counts By Reason",
    ]
    lines.extend(f"- `{key}`: {value}" for key, value in by_reason.most_common())
    lines.append("")
    lines.append("## Counts By Top Directory")
    lines.extend(f"- `{key}`: {value}" for key, value in by_top.most_common())
    lines.append("")
    lines.append("## Worst Files")
    lines.extend(f"- `{key}`: {value}" for key, value in by_file.most_common(50))
    lines.append("")
    lines.append("## Full List")
    for index, item in enumerate(findings, 1):
        scope = f" `{item['scope']}`" if item["scope"] else ""
        lines.append(
            f"{index}. `{item['path']}:{item['line']}`{scope} "
            f"except `{item['exception']}` -> `{item['reason']}` / `{item['body']}`"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run_audit()
    print(
        json.dumps(
            {
                "files_scanned": result["files_scanned"],
                "quiet_except_count": result["quiet_except_count"],
                "parse_errors": len(result["parse_errors"]),
                "report_md": str(REPORT_MD),
                "report_json": str(REPORT_JSON),
                "worst_files": result["worst_files"][:20],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
