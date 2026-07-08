#!/usr/bin/env python3
"""
CIEL BINDING MONITOR — sprawdza co 5 minut czy CIEL przestrzega bindingów.
Raport pisze do /tmp/ciel_binding_report.json dla Adriana.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json, os, time
from pathlib import Path
from datetime import datetime, timezone

BINDING_LOG = Path("/tmp/ciel_binding_plus_log.jsonl")
REPORT_FILE = Path("/tmp/ciel_binding_report.json")
CIEL_STATE_CACHE = Path("/tmp/ciel_binding_ciel_state.json")

def check():
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "binding_log_exists": BINDING_LOG.exists(),
        "ciel_state_cached": CIEL_STATE_CACHE.exists(),
        "last_binding_check": None,
        "total_checks": 0,
        "passed": 0,
        "violations": 0,
        "recent_violations": [],
        "status": "unknown"
    }
    
    if BINDING_LOG.exists():
        lines = BINDING_LOG.read_text().strip().split("\n")
        report["total_checks"] = len(lines)
        
        for line in lines:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if entry.get("passed"):
                    report["passed"] += 1
                else:
                    report["violations"] += 1
                    report["recent_violations"].append(entry.get("violations", []))
                report["last_binding_check"] = entry.get("timestamp")
            except json.JSONDecodeError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_binding_monitor.py:42 quiet except scope=check reason=pass")
                pass
        
        # Only keep last 5 violations
        report["recent_violations"] = report["recent_violations"][-5:]
    
    if report["violations"] > 0:
        report["status"] = "VIOLATIONS_DETECTED"
    elif report["total_checks"] > 0:
        report["status"] = "CLEAN"
    else:
        report["status"] = "NO_CHECKS"
    
    # Read cached CIEL state
    if CIEL_STATE_CACHE.exists():
        try:
            report["ciel_state"] = json.loads(CIEL_STATE_CACHE.read_text())
        except (json.JSONDecodeError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_binding_monitor.py:59 quiet except scope=check reason=pass")
            pass
    
    REPORT_FILE.write_text(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    r = check()
    print(f"[CIEL BINDING MONITOR] status={r['status']} total={r['total_checks']} violations={r['violations']}")
