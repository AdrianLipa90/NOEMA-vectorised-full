"""Tests for the ``python -m ciel_sot_agent`` entry point (__main__.py)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    src = str(Path(__file__).resolve().parents[1] / "src")
    env = {**os.environ, "PYTHONPATH": src}
    return subprocess.run(
        [sys.executable, "-m", "ciel_sot_agent", *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_main_no_args_shows_help() -> None:
    result = _run()
    assert result.returncode == 0
    assert "python -m ciel_sot_agent" in result.stdout
    assert "sync" in result.stdout


def test_main_help_flag() -> None:
    result = _run("--help")
    assert result.returncode == 0
    assert "python -m ciel_sot_agent" in result.stdout
    assert "sync" in result.stdout


def test_main_unknown_command() -> None:
    result = _run("nonexistent-command")
    assert result.returncode != 0
    assert "Unknown command" in result.stderr


def test_main_lists_all_commands() -> None:
    result = _run("--help")
    expected_commands = [
        "sync",
        "sync-v2",
        "gh-coupling",
        "gh-coupling-v2",
        "index-validate",
        "index-validate-v2",
        "orbital-bridge",
        "sapiens-client",
        "runtime-evidence-ingest",
        "buildroot-phase-probe",
        "gui",
    ]
    for cmd in expected_commands:
        assert cmd in result.stdout, f"Command {cmd!r} missing from help output"
