#!/usr/bin/env python3
"""Keep canonical runtime hashes synchronized after intentional edits.

The watcher is deliberately narrow: it only touches generated hash metadata
and the two Codex registration arguments, never source code or operational
state.  JSON path-contract hashing is semantic, so formatting-only edits do
not churn the policy hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "runtime" / "hooks" / "codex_lifecycle_hook.py"
POLICY = ROOT / "runtime" / "hooks" / "codex_hook_policy.json"
PATHS = ROOT / "config" / "noema_paths.json"
HEADLESS_MANIFEST = ROOT / "config" / "headless_runtime.sha256"
CODEX_CONFIG = Path.home() / ".codex" / "config.toml"
HEADLESS_SOURCES = (
    ROOT / "scripts" / "sync_canonical_hashes.py",
    ROOT / "scripts" / "ciel_headless_daemon.py",
    ROOT / "config" / "ciel_headless_runtime.json",
    ROOT / "data" / "cielingo" / "verified_knowledge" / "einstein_maxwell_v1.json",
    ROOT / "src" / "cielingo_core" / "autonomous_response.py",
    ROOT / "src" / "ciel_geometry" / "phasenav" / "operator_algebra.py",
    ROOT / "src" / "ciel_geometry" / "paths.py",
    ROOT / "src" / "ciel_geometry" / "orbital_state_contract.py",
    ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega" / "ciel" / "engine.py",
    PATHS,
)


def raw_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_json_sha(path: Path) -> str:
    value = json.loads(path.read_text(encoding="utf-8"))
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def sync_policy() -> bool:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    expected = semantic_json_sha(PATHS)
    changed = policy.get("noema_paths_sha256") != expected
    if changed:
        policy["noema_paths_sha256"] = expected
        atomic_write(POLICY, json.dumps(policy, ensure_ascii=False, indent=2) + "\n")
    return changed


def sync_headless_manifest() -> bool:
    expected = "\n".join(f"{raw_sha(path)}  {path.relative_to(ROOT)}" for path in HEADLESS_SOURCES) + "\n"
    current = HEADLESS_MANIFEST.read_text(encoding="utf-8") if HEADLESS_MANIFEST.exists() else ""
    if current == expected:
        return False
    atomic_write(HEADLESS_MANIFEST, expected)
    return True


def sync_codex_registration() -> bool:
    if not CODEX_CONFIG.exists():
        return False
    text = CODEX_CONFIG.read_text(encoding="utf-8")
    hook_sha = raw_sha(HOOK)
    policy_sha = raw_sha(POLICY)
    updated = re.sub(r'(--expected-hook-sha256\s+")[0-9a-f]{64}(" )', rf'\g<1>{hook_sha}\g<2>', text)
    updated = re.sub(r'(--expected-policy-sha256\s+")[0-9a-f]{64}(" )', rf'\g<1>{policy_sha}\g<2>', updated)
    if updated == text:
        return False
    atomic_write(CODEX_CONFIG, updated)
    return True


def headless_failures() -> list[str]:
    failures: list[str] = []
    expected_manifest = "\n".join(f"{raw_sha(path)}  {path.relative_to(ROOT)}" for path in HEADLESS_SOURCES) + "\n"
    if HEADLESS_MANIFEST.read_text(encoding="utf-8") != expected_manifest:
        failures.append(str(HEADLESS_MANIFEST))
    return failures


def report_check(failures: list[str]) -> int:
    if failures:
        print("HASH_SYNC_FAIL")
        for path in failures:
            print(path)
        return 1
    print("HASH_SYNC_OK")
    return 0


def check() -> int:
    failures = headless_failures()
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    if policy.get("noema_paths_sha256") != semantic_json_sha(PATHS):
        failures.append(str(POLICY))
    if CODEX_CONFIG.exists():
        text = CODEX_CONFIG.read_text(encoding="utf-8")
        if raw_sha(HOOK) not in text or raw_sha(POLICY) not in text:
            failures.append(str(CODEX_CONFIG))
    return report_check(failures)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--headless-only",
        action="store_true",
        help="synchronize/check only the headless manifest; never edit Codex registration",
    )
    args = parser.parse_args()
    if args.headless_only:
        changed = sync_headless_manifest() if args.update else False
        if args.update:
            print(json.dumps({"status": "updated", "headless_manifest": changed}, sort_keys=True))
        return report_check(headless_failures())
    if args.update:
        policy_changed = sync_policy()
        manifest_changed = sync_headless_manifest()
        registration_changed = sync_codex_registration()
        print(json.dumps({
            "status": "updated",
            "policy": policy_changed,
            "headless_manifest": manifest_changed,
            "codex_registration": registration_changed,
        }, sort_keys=True))
        return check()
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
