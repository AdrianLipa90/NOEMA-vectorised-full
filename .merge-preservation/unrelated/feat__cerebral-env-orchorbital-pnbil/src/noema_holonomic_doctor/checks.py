"""Static diagnostic checks for NOEMA Holonomic Doctor."""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .manifest import ManifestEntry

_TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".diff", ".patch"}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    path: str | None = None
    evidence: dict[str, Any] = field(default_factory=dict)


def _read_text(root: Path, entry: ManifestEntry, max_bytes: int) -> str | None:
    if entry.suffix not in _TEXT_SUFFIXES or entry.size > max_bytes:
        return None
    try:
        return (root / entry.path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/checks.py:27 quiet except scope=_read_text reason=return None")
        return None


def _path_kind(path: str) -> str:
    """Classify scanned paths so fixtures/policy text do not become runtime findings."""
    if path.startswith((".python_packages/", "node_modules/", "vendor/")):
        return "vendored"
    if path.startswith("tests/") or "/tests/" in path:
        return "test_fixture"
    if path == "src/noema_holonomic_doctor/constraints.py":
        return "policy_text"
    if path.endswith((".md", ".rst", ".txt")):
        return "documentation"
    if path.endswith((".diff", ".patch")) or path.startswith("patches/"):
        return "patch_candidate"
    return "runtime_code"


def check_inverted_rh(root: Path, manifest: list[ManifestEntry], *, max_bytes: int = 256_000) -> list[Finding]:
    findings: list[Finding] = []
    for entry in manifest:
        text = _read_text(root, entry, max_bytes)
        if text is None or "R_H" not in text:
            continue

        suspicious = (
            "1 - R_H" in text
            or "1.0 - snap.get(\"R_H\"" in text
            or "1.0 - snapshot.get(\"R_H\"" in text
        )
        uses_helper = "rh_defect_score" in text or "rh_coherence_score" in text
        kind = _path_kind(entry.path)

        if kind != "runtime_code":
            continue

        if suspicious and not uses_helper:
            findings.append(
                Finding(
                    code="inverted_rh_metric_candidate",
                    severity="high",
                    message="Raw R_H appears converted through 1 - R_H without the canonical bounded helper.",
                    path=entry.path,
                    evidence={"constraint": "no_inverted_rh_metric", "path_kind": kind},
                )
            )
    return findings


def check_rh_pipeline_hook(root: Path, manifest: list[ManifestEntry], *, max_bytes: int = 256_000) -> list[Finding]:
    paths = {entry.path for entry in manifest}

    if "src/ciel_sot_agent/rh_pipeline_jfunctional.py" not in paths:
        return []

    pipeline_entry = next((entry for entry in manifest if entry.path == "src/ciel_sot_agent/ciel_pipeline.py"), None)
    if pipeline_entry is None:
        return []

    text = _read_text(root, pipeline_entry, max_bytes) or ""

    if "compute_pipeline_j_functional" in text:
        return []

    if "patches/fix_rh_jfunctional_pipeline_hook.diff" in paths:
        return [
            Finding(
                code="rh_pipeline_hook_pending",
                severity="medium",
                message="R_H pipeline adapter exists, but ciel_pipeline.py is not hooked yet; patch candidate is present.",
                path="src/ciel_sot_agent/ciel_pipeline.py",
                evidence={"patch": "patches/fix_rh_jfunctional_pipeline_hook.diff"},
            )
        ]

    return [
        Finding(
            code="dead_rh_pipeline_adapter",
            severity="medium",
            message="R_H pipeline adapter exists, but no runtime hook or patch candidate was found.",
            path="src/ciel_sot_agent/rh_pipeline_jfunctional.py",
        )
    ]


def check_syntax_errors(root: Path, manifest: list[ManifestEntry], *, max_bytes: int = 2_000_000) -> list[Finding]:
    """Parse every .py file with ast.parse to catch real syntax/indentation breakage.

    Unlike `python -m compileall`, this reports one Finding per broken file with
    exact line/offset instead of dumping raw tracebacks to stdout.
    """
    findings: list[Finding] = []
    for entry in manifest:
        if entry.suffix != ".py" or entry.size > max_bytes:
            continue
        path = root / entry.path
        try:
            source = path.read_bytes()
        except OSError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/checks.py:syntax quiet except scope=check_syntax_errors reason=continue")
            continue
        try:
            ast.parse(source, filename=entry.path)
        except (SyntaxError, ValueError) as exc:
            findings.append(
                Finding(
                    code="tab_error" if isinstance(exc, TabError) else "syntax_error",
                    severity="high",
                    message=f"{type(exc).__name__}: {exc.msg if hasattr(exc, 'msg') else exc}",
                    path=entry.path,
                    evidence={"lineno": getattr(exc, "lineno", None), "offset": getattr(exc, "offset", None)},
                )
            )
    return findings


def _except_body_is_silent(body: list[ast.stmt]) -> bool:
    if len(body) != 1:
        return False
    stmt = body[0]
    if isinstance(stmt, ast.Pass):
        return True
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
        return True
    return False


def _except_body_logs_and_swallows(body: list[ast.stmt]) -> bool:
    # Only flag high-visibility log calls that produce stack traces or ERROR/CRITICAL
    # lines in journalctl — these make caught exceptions look like live crashes.
    # .debug() is intentional quiet catch; do not flag it.
    _LOUD_ATTRS = {"exception", "error", "critical", "warning"}
    has_loud_log = False
    has_reraise = False
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Raise):
                has_reraise = True
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in _LOUD_ATTRS:
                    has_loud_log = True
    return has_loud_log and not has_reraise


def check_bare_except(root: Path, manifest: list[ManifestEntry], *, max_bytes: int = 512_000) -> list[Finding]:
    """Find except blocks that swallow errors: fully silent (no log, no re-raise)
    vs. logged-but-swallowed (the `_NOEMA_QUIET_EXCEPT_LOGGER` pattern that made
    genuinely-caught exceptions look like live crashes in journalctl this session).
    """
    findings: list[Finding] = []
    for entry in manifest:
        if entry.suffix != ".py" or entry.size > max_bytes:
            continue
        if _path_kind(entry.path) != "runtime_code":
            continue
        text = _read_text(root, entry, max_bytes)
        if text is None:
            continue
        try:
            tree = ast.parse(text, filename=entry.path)
        except (SyntaxError, ValueError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/checks.py:bare_except quiet except scope=check_bare_except reason=continue")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ExceptHandler):
                continue
            is_bare = node.type is None
            is_broad_exception = isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}
            if not (is_bare or is_broad_exception):
                continue
            if _except_body_is_silent(node.body):
                findings.append(
                    Finding(
                        code="silent_except_swallow",
                        severity="high",
                        message="except block with no logging, no re-raise, body is only pass/Ellipsis — error is fully discarded.",
                        path=entry.path,
                        evidence={"lineno": node.lineno, "bare": is_bare},
                    )
                )
            elif _except_body_logs_and_swallows(node.body):
                findings.append(
                    Finding(
                        code="quiet_except_logged",
                        severity="low",
                        message="except block logs the exception (often via .exception(), producing a full traceback) but does not re-raise — appears as a live crash in log tails even though it is caught.",
                        path=entry.path,
                        evidence={"lineno": node.lineno, "bare": is_bare},
                    )
                )
    return findings


def _module_name_for(rel_path: str) -> str | None:
    if not rel_path.startswith("src/"):
        return None
    parts = rel_path[len("src/"):].split("/")
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    elif parts[-1].endswith(".py"):
        parts[-1] = parts[-1][:-3]
    else:
        return None
    if not parts or not all(parts):
        return None
    return ".".join(parts)


def check_orphan_modules(root: Path, manifest: list[ManifestEntry], *, max_bytes: int = 512_000) -> list[Finding]:
    """Best-effort dead-code-island detector: src/ modules never imported by any
    other file in the manifest (source or scripts/). Heuristic — dynamic imports
    (importlib, plugin loaders, string-built module paths) are invisible to
    static AST parsing and will show up as false positives here; treat findings
    as leads to review, not confirmed dead code.
    """
    py_entries = [e for e in manifest if e.suffix == ".py"]
    module_by_path: dict[str, str] = {}
    for entry in py_entries:
        mod = _module_name_for(entry.path)
        if mod:
            module_by_path[entry.path] = mod
    all_modules = set(module_by_path.values())
    referenced: set[str] = set()

    for entry in py_entries:
        text = _read_text(root, entry, max_bytes)
        if text is None:
            continue
        try:
            tree = ast.parse(text, filename=entry.path)
        except (SyntaxError, ValueError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/noema_holonomic_doctor/checks.py:orphan quiet except scope=check_orphan_modules reason=continue")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    referenced.add(alias.name)
                    parts = alias.name.split(".")
                    for i in range(1, len(parts) + 1):
                        referenced.add(".".join(parts[:i]))
            elif isinstance(node, ast.ImportFrom) and node.module:
                referenced.add(node.module)
                parts = node.module.split(".")
                for i in range(1, len(parts) + 1):
                    referenced.add(".".join(parts[:i]))
                for alias in node.names:
                    referenced.add(f"{node.module}.{alias.name}")

    findings: list[Finding] = []
    for path, mod in sorted(module_by_path.items()):
        if mod in referenced:
            continue
        if any(mod.endswith(f".{ref}") or ref.endswith(f".{mod}") for ref in referenced):
            continue
        if path.endswith("__init__.py"):
            continue
        text = _read_text(root, next(e for e in py_entries if e.path == path), max_bytes) or ""
        if "__main__" in text and "if __name__" in text:
            continue
        if _path_kind(path) != "runtime_code":
            continue
        findings.append(
            Finding(
                code="orphan_module_candidate",
                severity="medium",
                message=f"Module '{mod}' is not imported anywhere else in the manifest (heuristic AST scan — dynamic imports not detected).",
                path=path,
                evidence={"module": mod},
            )
        )
    return findings


def run_static_checks(root: str | Path, manifest: list[ManifestEntry], *, max_bytes: int = 256_000) -> list[Finding]:
    root_path = Path(root).resolve()
    findings: list[Finding] = []
    findings.extend(check_inverted_rh(root_path, manifest, max_bytes=max_bytes))
    findings.extend(check_rh_pipeline_hook(root_path, manifest, max_bytes=max_bytes))
    findings.extend(check_syntax_errors(root_path, manifest))
    findings.extend(check_bare_except(root_path, manifest))
    findings.extend(check_orphan_modules(root_path, manifest))
    return findings


__all__ = [
    "Finding",
    "check_inverted_rh",
    "check_rh_pipeline_hook",
    "check_syntax_errors",
    "check_bare_except",
    "check_orphan_modules",
    "run_static_checks",
    "_path_kind",
]
