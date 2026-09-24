import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)
#!/usr/bin/env python3
"""NOEMA Sentinel — 24/7 watchdog: daemon health, attractor audit, surface integrity."""

import json
import os
import struct
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_registry import registry

SHM = Path("/dev/shm/ciel_noema")
SERVICES = [
    "noema-kuramoto", "noema-resonance-bridge", "noema-neutrino",
    "noema-cielingo-sync", "noema-nonlocal-proxy", "noema-linux-sensor",
    "noema-phasenav-hot", "noema-phasenav", "noema-analog-blend",
    "noema-archiver", "noema-consolidator", "noema-agent-backend",
]
CHECK_INTERVAL = 10
HISTORY_MAX = 360  # 1h at 10s


def read_surface():
    s = {"phi": [], "omega": [], "flavor": [], "gravity": [], "tick": 0}
    try:
        if (SHM / "tick").exists():
            with open(SHM / "tick", "rb") as f:
                s["tick"] = struct.unpack("Q", f.read())[0]
        if (SHM / "phi").exists():
            with open(SHM / "phi", "rb") as f:
                _raw = f.read()
                s["phi"] = list(struct.unpack(f"{len(_raw)//8}d", _raw))
        if (SHM / "omega").exists():
            with open(SHM / "omega", "rb") as f:
                _raw = f.read()
                s["omega"] = list(struct.unpack(f"{len(_raw)//8}d", _raw))
        if (SHM / "gravity").exists():
            with open(SHM / "gravity", "rb") as f:
                _graw = f.read()
                s["gravity"] = list(struct.unpack(f"{len(_graw)//8}d", _graw))
        if (SHM / "flavor").exists():
            with open(SHM / "flavor", "rb") as f:
                s["flavor"] = list(struct.unpack("6d", f.read()))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sentinel.py:55 quiet except scope=read_surface reason=pass")
        raise
        pass
    return s


def check_daemons():
    out = subprocess.run(
        ["systemctl", "--user", "list-units", "noema-*", "--no-legend"],
        capture_output=True, text=True, timeout=5,
    )
    states = {}
    for line in out.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 3:
            name = parts[0]
            state = parts[2]
            states[name] = state
    return states


def restart_daemon(name):
    try:
        subprocess.run(
            ["systemctl", "--user", "restart", name],
            capture_output=True, timeout=10,
        )
        return True
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sentinel.py:84 quiet except scope=restart_daemon reason=return False")
        raise
        return False


def coherence(phi):
    if not phi:
        return 0.0
    n = len(phi)
    r = abs(sum(__import__("cmath").exp(1j * p) for p in phi)) / n
    return round(r, 4)


def attractor_lock(phi, omega):
    """AGENT attractor lock status: M1(phi[3:6]) → π/4 ≈ 0.785 rad."""
    if len(phi) < 6:
        return {"status": "unknown", "error_rad": 99.0}
    target = 0.7853981633974483  # π/4
    errs = [abs((p % (2 * 3.141592653589793)) - target) for p in phi[3:6]]
    min_errs = [min(e, abs(2 * 3.141592653589793 - e)) for e in errs]
    mean_err = sum(min_errs) / len(min_errs)

    if mean_err < 0.1:
        status = "locked"
    elif mean_err < 0.3:
        status = "drifting"
    else:
        status = "free"

    return {
        "status": status,
        "error_rad": round(mean_err, 4),
        "phi_m1": [round(p, 4) for p in phi[3:6]],
        "omega_m1": [round(w, 4) for w in omega[3:6]] if len(omega) >= 6 else [],
    }


MAX_LOG_SIZE = 50 * 1024 * 1024  # 50 MB — po przekroczeniu rotuj

def _rotate_log(log_path: Path) -> None:
    """Rotuje log jeśli za duży — przenosi do .1, .2 itd."""
    try:
        if log_path.exists() and log_path.stat().st_size > MAX_LOG_SIZE:
            for i in range(9, 0, -1):  # max 9 backupów
                older = log_path.with_suffix(f".jsonl.{i}")
                newer = log_path.with_suffix(f".jsonl.{i-1}") if i > 1 else log_path
                if older.exists():
                    older.unlink()
                if newer.exists():
                    newer.rename(older)
            # skompresuj stary log
            import gzip
            with open(log_path, "rb") as f_in:
                with gzip.open(str(log_path) + ".gz.0", "wb") as f_out:
                    f_out.write(f_in.read())
            log_path.write_text("")  # wyczyść
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sentinel.py:139 quiet except scope=_rotate_log reason=pass")
        raise
        pass


def main():
    log_path = Path(os.environ.get("NOEMA_LOG_DIR", "/tmp")) / "noema_sentinel.jsonl"
    history = []
    _rotate_log(log_path)  # rotacja przy starcie
    hb_count = 0
    reg_token = registry.register("sentinel")

    while True:
        hb_count += 1
        if hb_count % 30 == 0:
            try:
                registry.heartbeat(reg_token)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sentinel.py:155 quiet except scope=main reason=pass")
                raise
                pass

        loop_start = time.monotonic()
        ts = datetime.now(tz=timezone.utc).isoformat()

        surface = read_surface()
        daemon_states = check_daemons()
        phi = surface.get("phi", [])
        coh = coherence(phi)

        attractor = attractor_lock(phi, surface.get("omega", []))

        failed = [n for n, s in daemon_states.items()
                  if s not in ("active", "activating") and "noema-archiver" not in n]

        # auto-restart failed daemons (except archiver which may be legitimately waiting)
        for name in failed:
            ok = restart_daemon(name)
            daemon_states[name] = "restarted" if ok else "dead"

        entry = {
            "ts": ts,
            "tick": surface.get("tick", 0),
            "coh": coh,
            "daemons_total": len([s for s in daemon_states.values() if s == "active"]),
            "daemons": daemon_states,
            "failed": failed,
            "gravity": surface.get("gravity", []),
            "flavor_4": surface.get("flavor", [0] * 6)[4] if len(surface.get("flavor", [])) > 4 else 0,
            "flavor_5": surface.get("flavor", [0] * 6)[5] if len(surface.get("flavor", [])) > 5 else 0,
            "attractor": attractor,
        }

        history.append(entry)
        if len(history) > HISTORY_MAX:
            history = history[-HISTORY_MAX:]

        try:
            with open(log_path, "a") as f:
                f.write(json.dumps(entry, separators=(",", ":")) + "\n")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sentinel.py:196 quiet except scope=main reason=pass")
            raise
            pass

        # write live health to surface
        try:
            health_path = SHM / "health"
            health_path.write_text(json.dumps({
                "ts": ts, "tick": entry["tick"], "coh": coh,
                "alive": entry["daemons_total"],
                "failed": entry["failed"],
                "g": entry["gravity"][:2] if entry["gravity"] else [],
                "attractor": attractor["status"],
                "attractor_err": attractor["error_rad"],
            }, separators=(",", ":")) + "\n")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sentinel.py:210 quiet except scope=main reason=pass")
            raise
            pass

        elapsed = time.monotonic() - loop_start
        sleep = max(0, CHECK_INTERVAL - elapsed)
        time.sleep(sleep)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sentinel.py:221 quiet except scope=<module> reason=pass")
        raise
        pass
