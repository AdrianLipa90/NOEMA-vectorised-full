from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from .protocol import JokeHealOutput, TensionInput


def default_scar_jsonl_path() -> Path:
    return Path("/media/adrian/New Volume1/CIEL_memories") / "jokeheal" / "jokeheal_scars.jsonl"


def build_scar_record(inp: TensionInput, symbolic_object: str, output_stub: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema": "ciel/jokeheal-scar/v0.1",
        "scar_id": f"JH-SCAR-{uuid.uuid4().hex[:12]}",
        "timestamp": time.time(),
        "source": inp.source,
        "symbolic_object": symbolic_object,
        "input_hash_hint": abs(hash(inp.text)) % (10**12),
        "mode": output_stub.get("mode"),
        "humor_dose": output_stub.get("humor_dose"),
        "boundary_level": output_stub.get("boundary_level"),
        "boundary_literal": bool(output_stub.get("boundary_literal", False)),
        "boundary_reasons": output_stub.get("boundary_reasons", []),
        "closure_score": output_stub.get("closure_score"),
        "residual_tension": output_stub.get("residual_tension"),
        "cognitive_tension": output_stub.get("cognitive_tension"),
        "symbolic_density": output_stub.get("symbolic_density"),
        "mnemonic_likely": bool(output_stub.get("mnemonic_likely", False)),
        "pain_overflow": bool(output_stub.get("pain_overflow", False)),
        "tags": output_stub.get("tags", []),
    }


def append_scar_record(record: Dict[str, Any], jsonl_path: Optional[str]) -> None:
    path = Path(jsonl_path).expanduser() if jsonl_path else default_scar_jsonl_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/jokeheal/scar_writer.py:45 quiet except scope=append_scar_record reason=return None")
        return
