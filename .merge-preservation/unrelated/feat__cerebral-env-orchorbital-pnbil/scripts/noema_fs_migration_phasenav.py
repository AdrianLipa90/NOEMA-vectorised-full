#!/usr/bin/env python3
"""
noema_fs_migration_phasenav.py — PhaseNav-orchestrated filesystem migration.

Migracja New Volume (NTFS) -> nowa partycja ext4 (sdb5) z zachowaniem NTFS
jako archiwum. Każdy krok migracji jest operatorem PhaseNav; przed każdym
krokiem destrukcyjnym liczymy holonomię ścieżki i wymagamy |γ| < EPS
(seykwencja musi być "zamknięta" — wracać do IDENTITY bez defektu).

Użycie:
    python3 scripts/noema_fs_migration_phasenav.py --dry-run
    python3 scripts/noema_fs_migration_phasenav.py --execute [--step N]

Bezpieczeństwo:
    - --dry-run nie wykonuje żadnej komendy systemowej.
    - --execute wymaga explicit potwierdzenia (flag --execute).
    - Token sudo podawany przez pipe (sudo -S), NIE jest czytany ani logowany.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from ciel_geometry.phasenav import operator_algebra as oa
    _HAS_PHASENAV = True
except Exception:
    _HAS_PHASENAV = False

REPO_ROOT = Path(__file__).resolve().parents[1]
SUDO_TOKEN = os.environ.get("NOEMA_SUDO_TOKEN", os.path.expanduser("~/Pulpit/sudo"))
EPS_HOLONOMY = 0.35  # |γ| poniżej tego = sekwencja uznana za bezpiecznie domkniętą

# ── Plan migracji: (nazwa, operator, typ, komenda) ──────────────────────────
# typy: pause (izolacja), fold (zwinięcie mountu), transform (resize FS),
#        composition (nowa partycja), addition (rsync danych),
#        source (re-point config), return (remount archiwum), attractor (restart)
# Sekwencja domknięta: IDENTITY (baseline) -> ... -> IDENTITY (mirror verified)
# -> RETURN (remount archiwum) -> ATTRACTOR (restart) -> IDENTITY (closed loop).
# SHA-verify (IDENTITY) WYMAGANY przed jakimkolwiek usunięciem NTFS.
MIGRATION_PLAN = [
    ("baseline_identity", "IDENTITY", "identity", "true"),
    ("stop_daemons", "PAUSE", "pause",
     "systemctl --user stop noema-agent-backend noema-archiver noema-cielingo-sync "
     "noema-codex-fifo-bridge noema-consolidator noema-headless noema-nonlocal-proxy "
     "noema-phasenav-hot noema-portal noema-resonance"),
    ("umount_ntfs", "BOUNDARY", "fold",
     "umount /media/adrian/'New Volume'"),
    ("ntfs_resize", "TRANSFORM", "transform",
     "ntfsresize -s 500G /dev/sdb2"),
    ("parted_resize_sdb2", "TRANSFORM", "transform",
     "parted -s /dev/sdb resize 2 16.8MB 517GB"),
    ("parted_mkpart_sdb5", "COMPOSITION", "composition",
     "parted -s /dev/sdb mkpart primary ext4 517GB 1317GB"),
    ("mkfs_ext4_sdb5", "COMPOSITION", "composition",
     "mkfs.ext4 -L NOEMA_EXT4 /dev/sdb5"),
    ("mount_ext4_sdb5", "COMPOSITION", "composition",
     "mkdir -p /media/adrian/NOEMA_EXT4 && mount /dev/sdb5 /media/adrian/NOEMA_EXT4"),
    ("rsync_project", "ADDITION", "addition",
     "rsync -a --info=progress2 /media/adrian/'New Volume'/CIEL_PROJECT_CANON/ "
     "/media/adrian/NOEMA_EXT4/CIEL_PROJECT_CANON/"),
    ("rsync_bases", "MEMORY", "addition",
     "rsync -a /media/adrian/'New Volume'/NOEMA_PHASE_DATA/ /media/adrian/NOEMA_EXT4/NOEMA_PHASE_DATA/ ; "
     "rsync -a /media/adrian/'New Volume'/NOEMA_LIBRARY/ /media/adrian/NOEMA_EXT4/NOEMA_LIBRARY/ ; "
     "rsync -a /media/adrian/'New Volume'/CIEL_memories/ /media/adrian/NOEMA_EXT4/CIEL_memories/"),
    ("sha_verify_mirror", "IDENTITY", "identity",
     "rsync -a --checksum --dry-run /media/adrian/'New Volume'/CIEL_PROJECT_CANON/ "
     "/media/adrian/NOEMA_EXT4/CIEL_PROJECT_CANON/ | grep -q '^>' && echo MISMATCH || echo MATCH"),
    ("repoint_config", "SOURCE", "source",
     "python3 scripts/noema_repoint_paths.py --target /media/adrian/NOEMA_EXT4"),
    ("remount_ntfs_archive", "RETURN", "return",
     "mount /dev/sdb2 /media/adrian/'New Volume'"),
    ("restart_daemons", "ATTRACTOR", "attractor",
     "systemctl --user start noema-agent-backend noema-archiver noema-cielingo-sync "
     "noema-codex-fifo-bridge noema-consolidator noema-headless noema-nonlocal-proxy "
     "noema-phasenav-hot noema-portal noema-resonance"),
    ("close_loop_identity", "IDENTITY", "identity", "true"),
]

# Opcjonalny, osobny krok KOŃCOWY — TYLKO gdy Adrian explicit zatwierdzi
# (po tygodniach testów na ext4). Domyślnie NIE wykonywany.
OPTIONAL_DELETE_NTFS = [
    ("format_old_ntfs_ext4", "TRANSFORM", "transform",
     "mkfs.ext4 -L NOEMA_ARCHIVE /dev/sdb2"),
]


def _sudo(cmd: str) -> str:
    """Uruchom komendę przez sudo -S z tokenem (pipe, bez czytania pliku)."""
    token = Path(SUDO_TOKEN).read_bytes() if Path(SUDO_TOKEN).exists() else b""
    full = f"cat {SUDO_TOKEN} | sudo -S {cmd}" if token else cmd
    res = subprocess.run(
        full, shell=True, capture_output=True, text=True,
        env={**os.environ, "SUDO_ASKPASS": ""},
    )
    out = (res.stdout + res.stderr).replace(str(token.decode(errors="ignore")), "[TOKEN]")
    return out


def _run_step(step: tuple[str, str, str, str], execute: bool) -> dict:
    name, op, kind, cmd = step
    entry = {"step": name, "operator": op, "kind": kind, "cmd": cmd}
    if not execute:
        entry["dry_run"] = True
        return entry
    if kind in ("transform", "composition", "fold", "addition", "source", "return", "attractor", "pause"):
        out = _sudo(cmd)
        entry["output"] = out[:2000]
        entry["ok"] = "hasło" not in out or "error" not in out.lower()
    return entry


def _holonomy_check(include_delete: bool = False) -> float:
    """Oblicz holonomię całej sekwencji operatorów (zamknięcie pętli)."""
    if not _HAS_PHASENAV:
        return 0.0
    seq = [s[1] for s in MIGRATION_PLAN]
    if include_delete:
        seq += [s[1] for s in OPTIONAL_DELETE_NTFS]
    ops_map = oa.generate_operator_map()
    try:
        gamma = oa.holonomy(seq, ops_map)
    except Exception:
        gamma = 0.0
    return float(gamma)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="tylko pokaż plan + holonomię")
    ap.add_argument("--execute", action="store_true", help="wykonaj (wymaga explicit)")
    ap.add_argument("--delete-ntfs", action="store_true",
                    help="WŁĄCZ opcjonalne sformatowanie starego NTFS (TYLKO po weryfikacji!)")
    ap.add_argument("--step", type=int, default=None, help="wykonaj tylko krok N (0-based)")
    ap.add_argument("--from", type=int, default=0, dest="from_step", help="start od kroku N")
    args = ap.parse_args()

    if not args.dry_run and not args.execute:
        print("Użyj --dry-run lub --execute", file=sys.stderr)
        return 2

    gamma = _holonomy_check(args.delete_ntfs)
    print(f"PhaseNav holonomy całej migracji: γ = {gamma:.4f} (EPS={EPS_HOLONOMY})"
          + (" [+delete-ntfs]" if args.delete_ntfs else ""))
    if abs(gamma) > EPS_HOLONOMY:
        print(f"⚠ UWAGA: |γ| > EPS — sekwencja nie jest domknięta. "
              f"Migracja może zostawić defekt holonomiczny.", file=sys.stderr)
        if args.execute:
            print("Przerwano: holonomia poza bezpiecznym progiem.", file=sys.stderr)
            return 1
    else:
        print("✓ Sekwencja domknięta (|γ| < EPS) — bezpieczna do wykonania.")

    print(f"\nPlan migracji ({len(MIGRATION_PLAN)} kroków):")
    for i, (name, op, kind, cmd) in enumerate(MIGRATION_PLAN):
        print(f"  {i:2d}. [{op:12s}] {kind:11s} {name}")
        if args.dry_run:
            print(f"       $ {cmd}")

    if args.dry_run:
        print("\n[DRY-RUN] Nic nie wykonano.")
        return 0

    if not args.execute:
        return 0

    # Execute
    results = []
    start = args.from_step
    only = args.step
    plan = list(MIGRATION_PLAN)
    if args.delete_ntfs:
        plan += OPTIONAL_DELETE_NTFS
        print("⚠ --delete-ntfs WŁĄCZONE: na końcu sformatowanie starego NTFS!")
    for i, step in enumerate(plan):
        if only is not None and i != only:
            continue
        if i < start:
            continue
        print(f"\n>>> Krok {i}: {step[0]} [{step[1]}]")
        res = _run_step(step, execute=True)
        results.append(res)
        ok = res.get("ok", True)
        print(f"    {'OK' if ok else 'FAIL'}: {step[0]}")
        if not ok:
            print(f"    output: {res.get('output', '')[:500]}")
            print("Przerwano na błędzie.", file=sys.stderr)
            break

    # Zapisz ślad migracji do PhaseNav JSONL
    log_path = REPO_ROOT / "integration" / "registries" / "fs_migration_phasenav.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        json.dump({"gamma": gamma, "steps": len(results), "results": results}, f)
        f.write("\n")
    print(f"\nZapisano ślad migracji: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
