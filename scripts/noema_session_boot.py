#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

SCHEMA = "noema.session-boot/v2"


def load_module(path: Path, name: str):
    if not path.is_file():
        raise FileNotFoundError(str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot_load:{path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_paths_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("roots"), dict):
        raise ValueError("NOEMA paths JSON must contain roots")
    return data


def resolve_roots(args) -> tuple[Path, Path, Path, str]:
    surface = Path(args.surface_root or os.environ.get("NOEMA_SURFACE_ROOT", "/dev/shm/ciel_noema"))
    if args.library_root:
        library = Path(args.library_root)
        runtime = Path(args.runtime_root) if args.runtime_root else library.parent / "runtime"
        return library, runtime, surface, "explicit"
    env_library = os.environ.get("NOEMA_LIBRARY_ROOT")
    if env_library:
        library = Path(env_library)
        runtime = Path(args.runtime_root or os.environ.get("NOEMA_RUNTIME_ROOT", str(library.parent / "runtime")))
        return library, runtime, surface, "env"

    candidates: list[Path] = []
    if os.environ.get("NOEMA_PATHS"):
        candidates.append(Path(os.environ["NOEMA_PATHS"]))
    candidates.extend([
        Path.home() / ".config" / "noema" / "paths.json",
        Path("/media/adrian/REPOZYTORIA_GIT1/New_Volume/CIEL_PROJECT_CANON/NOEMA/config/noema_paths.json"),
        Path("/home/adrian/new_volume_rw/NOEMA_LIBRARY/CONFIG/paths.json"),
    ])
    for candidate in candidates:
        if candidate.is_file():
            data = load_paths_json(candidate)
            roots = data["roots"]
            if not roots.get("library"):
                continue
            library = Path(os.path.expandvars(os.path.expanduser(str(roots["library"]))))
            runtime = Path(os.path.expandvars(os.path.expanduser(str(roots.get("runtime") or library.parent / "runtime"))))
            if not args.surface_root and roots.get("surface"):
                surface = Path(os.path.expandvars(os.path.expanduser(str(roots["surface"]))))
            return library, runtime, surface, f"paths:{candidate}"
    raise RuntimeError("BLOCKED_LIBRARY_PATH_UNRESOLVED")


def require_nonempty_store(library: Path) -> dict[str, Any]:
    manifest_path = library / "surface_store" / "manifest.json"
    if not manifest_path.is_file():
        raise RuntimeError(f"BLOCKED_LIBRARY_STORE_MISSING:{manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if int(manifest.get("generation", 0)) <= 0 or not manifest.get("files"):
        raise RuntimeError("BLOCKED_LIBRARY_STORE_EMPTY_NO_AUTOSEED")
    return manifest


def run_capture(argv: list[str], *, env: dict[str, str] | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(argv, text=True, capture_output=True, check=False, env=env)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Fail-closed NOEMA Library -> ephemeral surface -> AUX tether boot")
    ap.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--library-root")
    ap.add_argument("--runtime-root")
    ap.add_argument("--surface-root")
    ap.add_argument("--require-socket", action="store_true")
    ap.add_argument("--max-receipt-age-s", type=float, default=30.0)
    ap.add_argument("--pin-file")
    ap.add_argument("--mount-manifest")
    ap.add_argument("--prestart-only", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo_root)
    failures: list[str] = []
    stages: list[dict[str, Any]] = []
    library = runtime = surface = None
    try:
        library, runtime, surface, root_source = resolve_roots(args)
        stages.append({"stage": "resolve_roots", "status": "PASS", "library": str(library), "runtime": str(runtime), "surface": str(surface), "source": root_source})

        pin_file = Path(args.pin_file) if args.pin_file else repo / "contracts" / "NOEMA_RUNTIME_SOURCE_PIN_V1.json"
        runtime_guard = repo / "scripts" / "noema_runtime_source_guard.py"
        guard_cmd = [sys.executable, str(runtime_guard), "--library-root", str(library), "--pin-file", str(pin_file)]
        if args.mount_manifest:
            guard_cmd.extend(["--mount-manifest", args.mount_manifest])
        rc, out, err = run_capture(guard_cmd)
        if rc != 0:
            raise RuntimeError(f"RUNTIME_SOURCE_GUARD_BLOCKED:{out or err}")
        stages.append({"stage": "runtime_source_guard", "status": "PASS", "result": json.loads(out)})

        manifest = require_nonempty_store(library)
        stages.append({"stage": "persistent_store", "status": "PASS", "generation": manifest.get("generation"), "files": sorted(manifest.get("files", {}))})

        surface_sync_path = repo / "integration" / "surface_persistence" / "v0_2" / "surface_sync.py"
        mod = load_module(surface_sync_path, "noema_surface_sync_v02")
        sync = mod.PersistentSurfaceSync(library, surface, runtime / "surface-fallback")
        # Session start is restore-only. Never capture unknown volatile RAM into SoT.
        projection = sync.project()
        stages.append({"stage": "library_to_ephemeral_projection", "status": "PASS", "receipt": projection})

        feedback = repo / "scripts" / "noema_aux_feedback_lane.py"
        rc, out, err = run_capture([sys.executable, str(feedback), "--root", str(surface)])
        if rc != 0:
            raise RuntimeError(f"BLOCKED_LIVE_FEEDBACK:{err or out}")
        stages.append({"stage": "aux_feedback", "status": "PASS", "stdout": out})

        if args.prestart_only:
            final_status = "PRESTART_READY"
        else:
            startpoint = repo / "scripts" / "dev_shm_startpoint.py"
            child_env = dict(os.environ)
            child_env["NOEMA_STARTPOINT_SKIP_LIBRARY_BOOT"] = "1"
            rc, out, err = run_capture([sys.executable, str(startpoint), "--root", str(surface), "--codex-hook"], env=child_env)
            if rc != 0:
                raise RuntimeError(f"STARTPOINT_FAILED:{rc}:{err or out}")
            stages.append({"stage": "startpoint", "status": "PASS", "stdout": out})

            guard = repo / "scripts" / "noema_aux_tether_guard.py"
            cmd = [sys.executable, str(guard), "--root", str(surface), "--max-receipt-age-s", str(args.max_receipt_age_s)]
            if args.require_socket:
                cmd.append("--require-socket")
            rc, out, err = run_capture(cmd)
            if rc != 0:
                raise RuntimeError(f"TETHER_GUARD_BLOCKED:{out or err}")
            guard_result = json.loads(out)
            stages.append({"stage": "tether_guard", "status": "PASS", "result": guard_result})
            final_status = "ACTIVE"
    except Exception as exc:
        failures.append(f"{type(exc).__name__}:{exc}")
        final_status = "BLOCKED"

    receipt = {
        "schema": SCHEMA,
        "created_unix_ns": time.time_ns(),
        "tether_status": final_status,
        "fail_closed": True,
        "library_root": str(library) if library is not None else None,
        "surface_root": str(surface) if surface is not None else None,
        "stages": stages,
        "failures": failures,
        "invariants": {
            "boot_capture_allowed": False,
            "auto_seed_allowed": False,
            "candidate_memory_fallback_allowed": False,
            "aux_phi_overwrite_allowed": False,
        },
    }
    print(json.dumps(receipt, sort_keys=True, ensure_ascii=False))
    return 0 if final_status in {"ACTIVE", "PRESTART_READY"} else 23


if __name__ == "__main__":
    raise SystemExit(main())
