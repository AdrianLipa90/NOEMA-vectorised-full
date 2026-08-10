from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_sot_agent.function_identity_cli import scan_payload


def test_scan_payload_is_explicitly_threshold_free(tmp_path: Path):
    source = tmp_path / "sample.py"
    source.write_text(
        "import json\nimport numpy as np\ndef f(x):\n    return np.asarray(x)\n",
        encoding="utf-8",
    )
    payload = scan_payload(tmp_path)
    assert payload["schema"] == "CIELPC_FUNCTION_IDENTITY_SCAN_V1"
    assert payload["thresholds"] == []
    dependencies = payload["dependencies"]
    assert "json" in dependencies["stdlib_imports"]
    assert "numpy" in dependencies["external_imports"]
    assert len(payload["functions"]) == 1
