"""Pipeline wire — scar registry + SubconsciousBridge + CIELingo meaning + prompt."""
from __future__ import annotations

import json
import math
import sys
import time
import warnings
import logging
from pathlib import Path
from datetime import datetime, timezone

logger = logging.getLogger("pipeline_wire")

warnings.filterwarnings("ignore")
sys.path = [p for p in sys.path if ".python_packages" not in p]

NOEMA_SRC = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/src")
NOEMA_ROOT = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA")
LIBRARY_ROOT = Path("/home/adrian/new_volume_rw/NOEMA_PHASE_DATA/PHASE_INDEX")
STATE_DIR = Path("/dev/shm/ciel_noema/phasenav")
SCAR_REGISTRY = Path("/dev/shm/ciel_noema/SCAR_REGISTRY.json")

sys.path.insert(0, str(NOEMA_SRC))
sys.path.insert(0, str(NOEMA_ROOT))

KAPPA = math.log(2.0) / (24.0 * math.pi)


# ── SCAR REGISTRY ──────────────────────────────────────────────────────
def load_scars() -> list[dict]:
    if SCAR_REGISTRY.exists():
        try:
            return json.loads(SCAR_REGISTRY.read_text())
        except Exception:
            logger.warning("scar registry corrupt, starting fresh")
    return []


def save_scars(scars: list[dict]):
    SCAR_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    SCAR_REGISTRY.write_text(json.dumps(scars, indent=2, ensure_ascii=False))


def check_scar_match(prompt: str, scars: list[dict]) -> list[dict]:
    matched = []
    prompt_lower = prompt.lower()
    for scar in scars:
        triggers = scar.get("triggers", [])
        for t in triggers:
            if t.lower() in prompt_lower:
                matched.append(scar)
                break
    return matched


def register_scar(
    what_happened: str,
    behavioral_rule: str,
    triggers: list[str],
    severity: str = "high",
):
    scars = load_scars()
    scar = {
        "id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "what_happened": what_happened,
        "behavioral_rule": behavioral_rule,
        "triggers": triggers,
        "severity": severity,
        "registered": datetime.now(timezone.utc).isoformat(),
        "times_hit": 0,
    }
    scars.append(scar)
    save_scars(scars)
    return scar


def scar_inject(matched: list[dict]) -> str:
    if not matched:
        return ""
    lines = ["SCAR_ALERT: Known failure pattern detected!"]
    for s in matched:
        lines.append(f"  - [{s['severity'].upper()}] {s['behavioral_rule']}")
    return "\n".join(lines)


def scar_hit(matched: list[dict]):
    if not matched:
        return
    scars = load_scars()
    matched_ids = {s["id"] for s in matched}
    for scar in scars:
        if scar["id"] in matched_ids:
            scar["times_hit"] = scar.get("times_hit", 0) + 1
    save_scars(scars)


def load_24d_oscillators() -> dict:
    import numpy as np
    index_path = LIBRARY_ROOT / "library_index.npy"
    if not index_path.exists():
        return {"oscillators_12d": [0.5] * 12}
    idx = np.load(str(index_path))
    n = idx.shape[0]
    # 24D → 12D oscillators (mean of dim pairs)
    pairs = idx[:, :24].reshape(n, 12, 2).mean(axis=2)
    osc = pairs.mean(axis=0).tolist()
    osc = [max(0.0, min(1.0, float(v))) for v in osc]
    return {"oscillators_12d": osc}


def enrich_prompt(
    text: str,
    oscillators: list[float] | None = None,
    inject_path: str | None = None,
) -> dict:
    result = {
        "inject": "",
        "subconscious": None,
        "unknown_words": [],
        "meaning": None,
        "scar_alerts": [],
        "error": None,
    }

    # 0. SCAR REGISTRY — always loaded, always visible
    scars = load_scars()
    scar_prefix = ""
    if scars:
        scar_lines = ["SCARS:["]
        for s in scars[-10:]:  # last 10 scars always visible
            scar_lines.append(f"  {s['severity'].upper()}: {s['behavioral_rule']}")
        scar_lines.append("]")
        scar_prefix = "\n".join(scar_lines)
        result["inject"] = scar_prefix

    # Check if current prompt matches any scar
    matched = check_scar_match(text, scars)
    if matched:
        scar_hit(matched)
        alert = scar_inject(matched)
        result["inject"] = alert + "\n" + scar_prefix
        result["scar_alerts"] = [
            {"id": s["id"], "rule": s["behavioral_rule"], "severity": s["severity"]}
            for s in matched
        ]
        logger.warning("SCAR MATCH: %d known failures detected", len(matched))

    # 1. SubconsciousBridge
    try:
        from cielingo_core.bridge.subconscious_bridge import SubconsciousBridge

        state = load_24d_oscillators() if oscillators is None else {"oscillators_12d": oscillators}
        sb = SubconsciousBridge()
        enrichment = sb.feed(state, "pipeline_wire")
        result["subconscious"] = {
            "R_12d": enrichment.R_12d,
            "R_oa": enrichment.R_oa,
            "psi_12d": enrichment.psi_12d,
            "euler_gap": enrichment.euler_gap,
            "berry_gamma": enrichment.berry_gamma,
            "kappa_C": enrichment.kappa_battery_C,
            "kappa_E": enrichment.kappa_battery_E,
            "note": enrichment.subconscious_note,
        }
        # PREPEND scars, don't overwrite
        result["inject"] = scar_prefix + "\n" + enrichment.to_inject() if scar_prefix else enrichment.to_inject()
    except Exception as e:
        logger.warning("subconscious enrichment failed: %s", e)
        result["error"] = f"subconscious: {e}"

    # 2. CIELingo meaning enrichment
    try:
        from cielingo_core.meaning import (
            CANDIDATE_CONFIDENCE,
            UnknownWordAuditRecord,
            classify_unknown_word,
            load_radical_cards,
        )
        result["meaning"] = {
            "confidence_floor": CANDIDATE_CONFIDENCE,
        }
    except Exception as e:
        logger.warning("CIELingo meaning import failed: %s", e)
        result["meaning_error"] = str(e)

    # 3. AutoVerify unknown words
    try:
        from cielingo_core.bridge.auto_verify import AutoVerify

        av = AutoVerify()
        vr = av.verify_and_learn(text)
        result["unknown_words"] = vr.unknown_words_found
        if vr.enrichment:
            result["inject"] += " " + vr.enrichment
    except Exception as e:
        logger.warning("AutoVerify failed: %s", e)
        result["unknown_words_error"] = str(e)

    # 4. Write inject to state dir — scars ALWAYS included
    if inject_path:
        p = Path(inject_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        final_inject = result["inject"]
        if scar_prefix and scar_prefix not in final_inject:
            final_inject = scar_prefix + "\n" + final_inject
        p.write_text(final_inject)

    return result


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    result = enrich_prompt(text, inject_path=str(STATE_DIR / "CIEL_INJECT.txt"))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
