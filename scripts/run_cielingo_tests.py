#!/usr/bin/env python3
"""Uruchamia testy CIELINGO_CANON przez subprocess z poprawnym PYTHONPATH."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

CIELINGO_ROOT = Path("/media/adrian/REPOZYTORIA_GIT1/New_Volume/CIEL_PROJECT_CANON/CIELINGO_CANON")
VENV_PYTEST   = CIELINGO_ROOT.parent.parent / ".venv" / "bin" / "pytest"
SYS_PYTEST    = Path("/usr/bin/pytest")

# Wybierz pytest
if VENV_PYTEST.exists():
    pytest_bin = str(VENV_PYTEST)
else:
    pytest_bin = "python3 -m pytest"

# Który test uruchomić
test_pattern = sys.argv[1] if len(sys.argv) > 1 else "tests/test_five_axes_v01.py"

result = subprocess.run(
    ["python3", "-m", "pytest", test_pattern, "-v", "--tb=short", "--no-header"],
    cwd=str(CIELINGO_ROOT),
    env={"PYTHONPATH": str(CIELINGO_ROOT / "src"), "PATH": "/usr/bin:/bin"},
    capture_output=True,
    text=True,
)

print(result.stdout[-6000:] if len(result.stdout) > 6000 else result.stdout)
if result.stderr:
    relevant = [l for l in result.stderr.splitlines()
                if not l.startswith("Warning") and "UserWarning" not in l]
    if relevant:
        print("STDERR:", "\n".join(relevant[-20:]))
print(json.dumps({"returncode": result.returncode}))
