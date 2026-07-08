"""NOEMA-style pytest matrix runner.

Navigation/classification is manifest-driven; pytest is used only as executor.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .pain_surface import PainPoint, classify_test_result


@dataclass(frozen=True)
class TestEntry:
    path: str
    kind: str


@dataclass(frozen=True)
class TestResult:
    path: str
    kind: str
    status: str
    returncode: int
    elapsed_s: float
    stdout_tail: str
    stderr_tail: str
    pain: dict | None


def classify_path(path: str) -> str:
    if "test_deb_e2e.py" in path or "packaging" in path:
        return "e2e_gate"
    if path.startswith("src/CIEL_OMEGA_COMPLETE_SYSTEM/"):
        return "embedded_legacy"
    if "noema" in path or "htri" in path or "holonomic" in path:
        return "noema_subsystem"
    if path.startswith("tests/"):
        return "unit_or_integration"
    return "unknown"


def discover_tests(root: str | Path) -> list[TestEntry]:
    root_path = Path(root).resolve()
    paths = []
    for base in (root_path / "tests", root_path / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"):
        if not base.exists():
            continue
        for path in sorted(base.rglob("test*.py")):
            rel = path.relative_to(root_path).as_posix()
            paths.append(TestEntry(path=rel, kind=classify_path(rel)))
    return paths


def run_one(root: str | Path, entry: TestEntry, *, timeout_s: float = 20.0) -> TestResult:
    """Run one test file through an external timeout guard.

    The timeout command is used only as an executor guard; navigation and
    reporting remain NOEMA manifest-driven.
    """
    root_path = Path(root).resolve()
    started = time.time()
    cmd = ["timeout", f"{int(timeout_s)}s", sys.executable, "-m", "pytest", entry.path, "-q"]
    proc = subprocess.run(
        cmd,
        cwd=root_path,
        text=True,
        capture_output=True,
        timeout=timeout_s + 5.0,
    )
    elapsed = time.time() - started
    pain = classify_test_result(entry.path, proc.returncode, elapsed, timeout_s, proc.stdout, proc.stderr)
    status = "PASS" if proc.returncode == 0 and pain is None else (pain.class_ if pain else "FAIL")
    return TestResult(entry.path, entry.kind, status, proc.returncode, elapsed, proc.stdout[-2000:], proc.stderr[-2000:], pain.to_json_dict() if pain else None)


def summarize(results: Iterable[TestResult]) -> dict:
    results = list(results)
    by_status: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1
        by_kind[r.kind] = by_kind.get(r.kind, 0) + 1
    return {
        "schema": "noema/test-matrix-summary/v0.1",
        "total": len(results),
        "by_status": by_status,
        "by_kind": by_kind,
        "pain_count": sum(1 for r in results if r.pain),
    }


def write_reports(root: str | Path, results: list[TestResult], out_dir: str = "integration/reports/noema_tests") -> dict:
    root_path = Path(root).resolve()
    target = root_path / out_dir
    target.mkdir(parents=True, exist_ok=True)
    matrix_path = target / "test_matrix.noema.jsonl"
    summary_path = target / "test_matrix_summary.noema.json"
    with matrix_path.open("w", encoding="utf-8") as fh:
        for result in results:
            fh.write(json.dumps(asdict(result), sort_keys=True) + "\n")
    summary = summarize(results)
    summary["matrix_path"] = matrix_path.as_posix()
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"matrix_path": matrix_path.as_posix(), "summary_path": summary_path.as_posix(), "summary": summary}


__all__ = ["TestEntry", "TestResult", "classify_path", "discover_tests", "run_one", "summarize", "write_reports"]
