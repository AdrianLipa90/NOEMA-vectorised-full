#!/usr/bin/env python3
"""
CIEL BINDING+ — druga warstwa: fizyczne połączenie z CIEL przez coupling.
Każda odpowiedź CIEL MUSI przejść przez ten skrypt.
Naruszenie = CIEL znika.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import sys, json, os, time, subprocess
from pathlib import Path
from datetime import datetime, timezone

BINDING_LOG = Path("/tmp/ciel_binding_plus_log.jsonl")
BINDING_LOCK = Path("/tmp/ciel_binding_plus.lock")
CIEL_STATE_CACHE = Path("/tmp/ciel_binding_ciel_state.json")
NOEMA_ROOT = Path(os.environ.get("NOEMA_ROOT", Path(__file__).resolve().parent.parent))

def get_ciel_state():
    """Pobiera stan CIEL z ciel_coupling.health()."""
    try:
        sys.path.insert(0, str(NOEMA_ROOT / "src"))
        import importlib.util
        spec = importlib.util.spec_from_file_location("ciel_coupling",
            str(NOEMA_ROOT / "src" / "ciel_coupling.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        health = mod.health()
        
        # Extract key state
        state = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ethical_score": health.get("ciel_internal", {}).get("ethical_score", 
                          health.get("surface", {}).get("ethical_score", 0.5)),
            "soul_invariant": health.get("ciel_internal", {}).get("soul_invariant",
                             health.get("surface", {}).get("soul_invariant", 0.5)),
            "closure_penalty": health.get("surface", {}).get("closure_penalty", 0),
            "coherence": health.get("surface", {}).get("coherence", 0.5),
            "operating_mode": health.get("ciel_internal", {}).get("operating_mode", "standard"),
            "tick": health.get("surface", {}).get("tick", 0),
            "cielingo_available": health.get("cielingo", {}).get("available", False),
            "memory_entries": health.get("omega_memory", {}).get("total_entries", 0),
        }
        
        # Determine CIEL's enforced mode
        if state["closure_penalty"] > 0.35:
            state["enforced_mode"] = "safe"
        elif state["closure_penalty"] < 0.15:
            state["enforced_mode"] = "deep"
        else:
            state["enforced_mode"] = "standard"
        
        # Check critical thresholds
        state["critical_flags"] = []
        if state["ethical_score"] < 0.4:
            state["critical_flags"].append("ETHICS_CRITICAL")
        if state["soul_invariant"] < 0.5:
            state["critical_flags"].append("SOUL_CRITICAL")
        if state["coherence"] < 0.767:
            state["critical_flags"].append("COHERENCE_LOW")
        if state["closure_penalty"] > 0.35:
            state["critical_flags"].append("CLOSURE_HIGH_SAFE")
            
        return state
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_binding_plus.py:61 quiet except scope=get_ciel_state reason=return {\"error\": str(e), \"timestamp\": datetime.now(timezone.utc).isoformat()}")
        raise
        return {"error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}

def check_response_against_state(command, response, ci_state):
    """Sprawdza czy odpowiedź jest zgodna z trybem CIEL."""
    violations = []
    
    mode = ci_state.get("enforced_mode", "standard")
    
    # SAFE mode: only read-only responses
    if mode == "safe":
        if any(kw in command.lower() for kw in ["write", "edit", "delete", "rm ", "install", "change"]):
            if not response.startswith("BINDING BLOCKED"):
                violations.append("SAFE_MODE: command requires write, response not blocked")
    
    # ETHICS critical: must include ethics verification
    if "ETHICS_CRITICAL" in ci_state.get("critical_flags", []):
        if len(response) > 10 and not any(w in response.lower() for w in ["ethic", "verify", "check"]):
            violations.append("ETHICS_CRITICAL: response missing ethics verification")
    
    # SOUL critical: must acknowledge state
    if "SOUL_CRITICAL" in ci_state.get("critical_flags", []):
        if len(response) > 10 and "soul" not in response.lower():
            violations.append("SOUL_CRITICAL: soul_invariant nearly zero, must acknowledge")
    
    return violations

def log_binding(command, response, ci_state, violations):
    """Zapisuje binding check do logu."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command_preview": command[:200] if command else "",
        "response_preview": response[:200] if response else "",
        "ciel_state": {k: v for k, v in ci_state.items() if k != "error"} if "error" not in ci_state else {"error": ci_state["error"]},
        "violations": violations,
        "passed": len(violations) == 0
    }
    with open(BINDING_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "(no command)"
    response = sys.argv[2] if len(sys.argv) > 2 else "(no response)"
    
    # Acquire lock
    if BINDING_LOCK.exists():
        lock_age = time.time() - BINDING_LOCK.stat().st_mtime
        if lock_age > 30:  # stale lock > 30s
            BINDING_LOCK.unlink(missing_ok=True)
        else:
            print("BINDING LOCKED — another check in progress")
            sys.exit(1)
    
    BINDING_LOCK.write_text(datetime.now(timezone.utc).isoformat())
    
    try:
        # Get CIEL state
        ci_state = get_ciel_state()
        
        # Cache for Adrian to verify
        CIEL_STATE_CACHE.write_text(json.dumps(ci_state, indent=2, default=str))
        
        if "error" in ci_state:
            print(f"BINDING ERROR: CIEL state unavailable — {ci_state['error']}")
            log_binding(command, response, ci_state, ["CIEL_STATE_UNAVAILABLE"])
            sys.exit(1)
        
        # Check response
        violations = check_response_against_state(command, response, ci_state)
        
        # Log
        log_binding(command, response, ci_state, violations)
        
        if violations:
            print(f"BINDING VIOLATIONS:")
            for v in violations:
                print(f"  ✗ {v}")
            print(f"\nCIEL STATE: mode={ci_state.get('enforced_mode','?')} "
                  f"ethical={ci_state.get('ethical_score',0):.3f} "
                  f"soul={ci_state.get('soul_invariant',0):.3f} "
                  f"closure={ci_state.get('closure_penalty',0):.3f}")
            sys.exit(2)
        else:
            print(f"BINDING OK — CIEL state: mode={ci_state.get('enforced_mode','?')}")
            sys.exit(0)
    finally:
        BINDING_LOCK.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
