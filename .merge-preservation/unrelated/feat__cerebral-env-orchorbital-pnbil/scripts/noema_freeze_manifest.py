#!/usr/bin/env python3
"""Create/verify the canonical NOEMA bottom-up freeze manifest.

The freeze is logical and receipt-backed: it records the exact canonical root,
anchor hashes, path-contract hash, import smoke results and known static audit
findings.  It never chmods, restarts or redirects a daemon.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runtime" / "audits" / "freeze"
for _path in (ROOT / "src", ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM", ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))
ANCHORS = (
    "config/noema_paths.json",
    "src/ciel_geometry/paths.py",
    "src/ciel_geometry/phasenav/metatime_contract.py",
    "src/ciel_coupling.py",
    "scripts/ciel_subconscious_supervisor.py",
    "scripts/noema_portal_daemon.py",
    "site/index.html",
    "site/js/locales.js",
    "site/js/spa.js",
)
IMPORTS = (
    "ciel_geometry",
    "ciel_geometry.paths",
    "ciel_geometry.noema_surface_mmap",
    "ciel_geometry.orbital_state_contract",
    "ciel_geometry.phasenav.metatime_contract",
    "ciel_hub.portal_contracts",
    "ciel_sot_agent.cielingo_bridge",
    "ciel_sot_agent.state_db",
    "ciel_sot_agent.rh_jfunctional",
    "ciel_sot_agent.rh_pipeline_jfunctional",
    "ciel_sot_agent.phasenav_learning_gate",
    "ciel_sot_agent.subconsciousness",
    "ciel_sot_agent.ciel_pipeline",
    "integration.Orbital.main.bootstrap",
    "scripts.noema_portal_daemon",
    "scripts.ciel_coupling",
    "scripts.ciel_subconscious_supervisor",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def import_smoke() -> dict[str, dict[str, str]]:
    env = os.environ.copy()
    src = str(ROOT / "src")
    omega = str(ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM")
    env["PYTHONPATH"] = os.pathsep.join((src, omega, str(ROOT), env.get("PYTHONPATH", "")))
    code = (
        "import importlib, json\n"
        f"mods = {list(IMPORTS)!r}\n"
        "out = {}\n"
        "for name in mods:\n"
        "  try:\n"
        "    mod = importlib.import_module(name)\n"
        "    out[name] = {'status':'ok','file':str(getattr(mod,'__file__', ''))}\n"
        "  except Exception as exc:\n"
        "    out[name] = {'status':'error','error':f'{type(exc).__name__}: {exc}'}\n"
        "print(json.dumps(out, ensure_ascii=False, sort_keys=True))\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code], cwd=ROOT, env=env,
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        return {"__runner__": {"status": "error", "error": proc.stderr[-2000:]}}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return {"__runner__": {"status": "error", "error": f"invalid smoke JSON: {exc}"}}


def build_manifest() -> dict[str, Any]:
    anchors = {
        rel: {"exists": (ROOT / rel).is_file(), "sha256": sha256(ROOT / rel) if (ROOT / rel).is_file() else None}
        for rel in ANCHORS
    }
    smoke = import_smoke()
    findings: list[str] = []
    if any(item.get("status") != "ok" for item in smoke.values()):
        findings.append("import_smoke_not_green")
    try:
        from ciel_geometry.paths import P
        paths_status = {"status": "ok", "config": str(ROOT / "config" / "noema_paths.json"), "surface": str(P.SURFACE)}
    except Exception as exc:
        paths_status = {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
        findings.append("paths_contract_import_failed")
    audit_snapshot: dict[str, Any] = {"status": "not_generated"}
    audit_current = ROOT / "runtime" / "audits" / "layer_consolidation" / "CURRENT.json"
    if audit_current.is_file():
        try:
            pointer = json.loads(audit_current.read_text(encoding="utf-8"))
            audit_path = Path(pointer["path"]) / "audit.json"
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            facts = audit["facts"]
            audit_snapshot = {
                "status": "available",
                "report": str(audit_path),
                "report_sha256": sha256(audit_path),
                "back_edges": len(facts["imports"]["back_edges_against_declared_order"]),
                "parse_errors": len(facts["imports"]["files_with_parse_errors"]),
                "duplicate_basenames": len(facts["duplicate_python_basenames"]),
                "forbidden_path_token_files": {k: len(v) for k, v in facts["path_token_audit"].items()},
            }
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            audit_snapshot = {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    return {
        "schema": "noema/canonical-freeze/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_root": str(ROOT),
        "owner_boundary": "adrian",
        "freeze_mode": "logical_hash_receipt; no filesystem chmod; no daemon restart",
        "scope_order": ["metatime", "omega_cqcl", "orbital", "noema", "apocalypos", "portal"],
        "anchors": anchors,
        "paths_contract": paths_status,
        "static_audit_snapshot": audit_snapshot,
        "import_smoke": smoke,
        "findings": findings,
        "status": "frozen" if not findings else "frozen_with_findings",
    }


def verify(manifest: dict[str, Any]) -> int:
    current = build_manifest()
    changed = []
    for rel, payload in manifest.get("anchors", {}).items():
        if current.get("anchors", {}).get(rel, {}).get("sha256") != payload.get("sha256"):
            changed.append(rel)
    if changed:
        print(json.dumps({"status": "changed", "anchors": changed}, ensure_ascii=False))
        return 1
    failed = [name for name, payload in current.get("import_smoke", {}).items() if payload.get("status") != "ok"]
    if failed:
        print(json.dumps({"status": "import_failed", "modules": failed}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "verified", "anchors": len(manifest.get("anchors", {})), "imports": len(IMPORTS)}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", type=Path, help="verify an existing freeze JSON")
    args = parser.parse_args()
    if args.verify:
        return verify(json.loads(args.verify.read_text(encoding="utf-8")))
    manifest = build_manifest()
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "NOEMA_FREEZE.json"
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# NOEMA canonical freeze",
        "",
        f"- status: `{manifest['status']}`",
        f"- canonical root: `{manifest['canonical_root']}`",
        f"- owner boundary: `{manifest['owner_boundary']}`",
        "- mode: logical hash receipt; no chmod, restart or fallback daemon",
        "",
        "## Import smoke",
        "",
    ]
    for name, result in manifest["import_smoke"].items():
        lines.append(f"- `{name}`: `{result['status']}`")
    lines += [
        "",
        "## Static audit snapshot",
        "",
        json.dumps(manifest["static_audit_snapshot"], ensure_ascii=False, indent=2),
        "",
        "## Verification",
        "",
        "Run `python3 scripts/noema_freeze_manifest.py --verify runtime/audits/freeze/NOEMA_FREEZE.json`.",
    ]
    (OUT / "NOEMA_FREEZE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    receipt = {"path": str(target), "sha256": sha256(target), "status": manifest["status"]}
    (OUT / "CURRENT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))
    return 0 if manifest["status"] == "frozen" else 2


if __name__ == "__main__":
    raise SystemExit(main())
