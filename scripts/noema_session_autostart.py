#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _env_or(value: str | None, name: str) -> str | None:
    return value if value else os.environ.get(name)


def _required(value: str | None, name: str) -> str:
    if not value:
        raise RuntimeError(f"missing required path: {name}")
    return value


def _load_surface_sync(repo_root: Path):
    path = repo_root / "integration/surface_persistence/v0_2/surface_sync.py"
    if not path.is_file():
        raise RuntimeError(f"surface_sync.py not found: {path}")
    spec = importlib.util.spec_from_file_location("noema_surface_sync", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load surface_sync module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fresh_runtime_status(path: Path, max_age: float = 2.0) -> tuple[bool, dict]:
    if not path.is_file():
        return False, {}
    try:
        status = json.loads(path.read_text(encoding="utf-8"))
        age = (time.time_ns() - int(status.get("heartbeat_ns", 0))) / 1e9
        pid = int(status.get("pid", -1))
        return status.get("status") == "ACTIVE" and 0 <= age <= max_age and _alive(pid), status
    except Exception:
        return False, {}


def main() -> int:
    ap = argparse.ArgumentParser(description="ACTIVE-only NOEMA session autostart")
    ap.add_argument("--root", default=os.environ.get("NOEMA_SURFACE_ROOT", "/dev/shm/ciel_noema"))
    ap.add_argument("--library-root")
    ap.add_argument("--fallback-root")
    ap.add_argument("--runtime-root")
    ap.add_argument("--aux-state-file")
    ap.add_argument("--geometry-root")
    ap.add_argument("--socket", default=os.environ.get("NOEMA_CIEL_SOCKET", "/run/user/1000/noema/ciel_headless.sock"))
    ap.add_argument("--startup-timeout", type=float, default=5.0)
    args = ap.parse_args()

    failures: list[str] = []
    evidence: dict[str, object] = {}
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    root = Path(args.root)

    try:
        library_root = Path(_required(_env_or(args.library_root, "NOEMA_LIBRARY_ROOT"), "NOEMA_LIBRARY_ROOT"))
        fallback_root = Path(_required(_env_or(args.fallback_root, "NOEMA_SURFACE_FALLBACK_ROOT"), "NOEMA_SURFACE_FALLBACK_ROOT"))
        runtime_root = Path(_required(_env_or(args.runtime_root, "NOEMA_RUNTIME_TETHER_ROOT"), "NOEMA_RUNTIME_TETHER_ROOT"))
        geometry_raw = _env_or(args.geometry_root, "NOEMA_GEOMETRY_ROOT")
        geometry_root = Path(geometry_raw) if geometry_raw else None
        aux_raw = _env_or(args.aux_state_file, "NOEMA_AUX_STATE_FILE")
        aux_state_file = Path(aux_raw) if aux_raw else runtime_root / "aux/self_state.npy"
    except Exception as exc:
        failures.append(f"PATH_RESOLUTION:{type(exc).__name__}:{exc}")
        library_root = fallback_root = runtime_root = Path(".")
        geometry_root = None
        aux_state_file = Path(".")

    # Persistent canonical memory -> volatile projection only. Boot never seeds
    # persistent truth from RAM and never captures producer-owned siblings.
    if not failures:
        try:
            module = _load_surface_sync(repo_root)
            sync = module.PersistentSurfaceSync(library_root, root, fallback_root)
            manifest = sync.init()
            if int(manifest.get("generation", 0)) <= 0 or not manifest.get("files"):
                raise RuntimeError("persistent canonical memory store empty")
            evidence["memory_projection"] = sync.project()
            evidence["memory_generation"] = sync.manifest()["generation"]
        except Exception as exc:
            failures.append(f"MEMORY_PROJECTION:{type(exc).__name__}:{exc}")

    # AUX input producer. A missing daemon is a cold-start condition, not an
    # excuse for a static placeholder.
    aux_status_path = root / "aux_stream_status.json"
    aux_ok, _ = _fresh_runtime_status(aux_status_path)
    if not failures and not aux_ok:
        try:
            log = runtime_root / "logs/aux_input_runtime.log"
            log.parent.mkdir(parents=True, exist_ok=True)
            fh = log.open("ab", buffering=0)
            cmd = [
                sys.executable,
                str(script_dir / "noema_aux_input_runtime.py"),
                "--surface-root", str(root),
                "--persistent-file", str(aux_state_file),
            ]
            if geometry_root is not None:
                cmd += ["--geometry-root", str(geometry_root)]
            proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT, start_new_session=True)
            evidence["started_aux_input_pid"] = proc.pid
        except Exception as exc:
            failures.append(f"AUX_START:{type(exc).__name__}:{exc}")

    # Native NOEMA phase + raw duplex feedback producer.
    tether_status_path = root / "tether_runtime_status.json"
    tether_ok, _ = _fresh_runtime_status(tether_status_path)
    if not failures and not tether_ok:
        try:
            log = runtime_root / "logs/tether_runtime.log"
            log.parent.mkdir(parents=True, exist_ok=True)
            fh = log.open("ab", buffering=0)
            cmd = [
                sys.executable,
                str(script_dir / "noema_tether_runtime.py"),
                "--surface-root", str(root),
                "--persistent-root", str(runtime_root),
                "--socket", args.socket,
            ]
            if geometry_root is not None:
                cmd += ["--geometry-root", str(geometry_root)]
            proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT, start_new_session=True)
            evidence["started_tether_runtime_pid"] = proc.pid
        except Exception as exc:
            failures.append(f"TETHER_START:{type(exc).__name__}:{exc}")

    # Bounded convergence. No infinite wait and no PARTIAL success.
    deadline = time.monotonic() + max(0.1, args.startup_timeout)
    while not failures and time.monotonic() < deadline:
        aux_ok, aux_status = _fresh_runtime_status(aux_status_path)
        tether_ok, tether_status = _fresh_runtime_status(tether_status_path)
        required = [root / "phi", root / "aux_phi", root / "aux_feedback_phi", Path(args.socket)]
        if aux_ok and tether_ok and all(path.exists() for path in required):
            evidence["aux_runtime"] = aux_status
            evidence["tether_runtime"] = tether_status
            break
        time.sleep(0.1)
    else:
        if not failures:
            failures.append("STARTUP_CONVERGENCE_TIMEOUT")

    # Derived session capsule. PARTIAL is explicitly rejected here.
    if not failures:
        start = subprocess.run(
            [sys.executable, str(script_dir / "dev_shm_startpoint.py"), "--root", str(root)],
            text=True, capture_output=True,
        )
        evidence["startpoint_rc"] = start.returncode
        if start.returncode != 0:
            failures.append(f"STARTPOINT_RC:{start.returncode}:{start.stderr.strip()}")
        else:
            try:
                packet = json.loads(start.stdout)
                evidence["startpoint_status"] = packet.get("status")
                if packet.get("status") != "VERIFIED":
                    failures.append(f"STARTPOINT_NOT_VERIFIED:{packet.get('status')}")
                if not packet.get("current_task"):
                    failures.append("STARTPOINT_MISSING_CURRENT_TASK")
                if not packet.get("active_path"):
                    failures.append("STARTPOINT_MISSING_ACTIVE_PATH")
            except Exception as exc:
                failures.append(f"STARTPOINT_PARSE:{type(exc).__name__}:{exc}")

    # Hard structural guard + fresh transport/receipt guard.
    if not failures:
        basic = subprocess.run(
            [sys.executable, str(script_dir / "noema_aux_tether_guard.py"), "--root", str(root), "--socket", args.socket, "--require-socket"],
            text=True, capture_output=True,
        )
        evidence["basic_guard_rc"] = basic.returncode
        evidence["basic_guard_stdout"] = basic.stdout.strip()
        if basic.returncode != 0:
            failures.append(f"BASIC_GUARD:{basic.stdout.strip()}")

    if not failures:
        fresh = subprocess.run(
            [sys.executable, str(script_dir / "noema_tether_receipt_guard.py"), "--root", str(root), "--socket", args.socket],
            text=True, capture_output=True,
        )
        evidence["receipt_guard_rc"] = fresh.returncode
        evidence["receipt_guard_stdout"] = fresh.stdout.strip()
        if fresh.returncode != 0:
            failures.append(f"RECEIPT_GUARD:{fresh.stdout.strip()}")

    status = "ACTIVE" if not failures else "BLOCKED"
    output = {
        "schema": "noema.session-autostart/v2",
        "tether_status": status,
        "working_state_allowed": status == "ACTIVE",
        "fail_closed": True,
        "partial_is_working_state": False,
        "failures": failures,
        "evidence": evidence,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if status == "ACTIVE" else 25


if __name__ == "__main__":
    raise SystemExit(main())
