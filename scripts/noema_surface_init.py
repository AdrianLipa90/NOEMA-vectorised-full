"""
noema_surface_init.py — NOEMA /dev/shm surface bootstrap

Uruchamiany przez noema-surface-init.service (Type=oneshot) PRZED wszystkimi
demonami NOEMA. Odtwarza strukturę tmpfs /dev/shm/ciel_noema/ po każdym restarcie.

/dev/shm jest tmpfs (RAM) — Linux czyści go przy każdym starcie jądra.
Ten skrypt sprawia, że demony zawsze znajdą gotową strukturę katalogów i plików.
"""
import os
import pathlib
import json
import struct
import datetime
import sys

BASE = pathlib.Path("/dev/shm/ciel_noema")
IMAGINAL = pathlib.Path("/dev/shm/ciel_noema_imaginal")
TMP = pathlib.Path("/tmp")

# ── Rozmiary plików mmap (float64 = 8B, int64 = 8B) ────────────────────────
# 36 oscylatorów × 8B = 288
N_OSC = 36
F64 = 8
I64 = 8
N_COUPLING = N_OSC * N_OSC * F64   # 10368 — macierz sprzężeń 36×36

MMAP_SIZES = {
    "phi":           N_OSC * F64,     # 288  — fazy Kuramoto
    "omega":         N_OSC * F64,     # 288  — prędkości kątowe
    "tau":           N_OSC * F64,     # 288  — czas relacyjny
    "R_geom":        N_OSC * F64,     # 288  — geometria R
    "Z_geom":        N_OSC * F64,     # 288  — geometria Z
    "psi_geom":      N_OSC * F64,     # 288  — geometria psi
    "sensor_raw":    N_OSC * F64,     # 288  — raw sensor
    "g":             N_COUPLING,      # 10368 — macierz g
    "gravity":       8 * F64,         # 64   — wektor gravity
    "flavor":        6 * F64,         # 48   — smaki neutrin
    "holonomy":      7 * F64,         # 56   — holonomia
    "tick":          I64,             # 8    — globalny tick
    # analog bus
    "analog/phi_hot":    N_OSC * F64,
    "analog/phi_cold":   N_OSC * F64,
    "analog/coupling":   N_COUPLING,
    "analog/resonance":  I64,
    "analog/temp":       I64,
    "analog/tick":       I64,
}


def ensure_dir(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_zeros(path: pathlib.Path, size: int) -> None:
    """Tworzy plik zero-filled jeśli nie istnieje lub ma błędny rozmiar."""
    if path.exists() and path.stat().st_size == size:
        return  # Już poprawny — daemon mógł już go zainicjować
    path.write_bytes(bytes(size))
    print(f"  init: {path.relative_to(BASE)}  ({size}B)")


def main() -> None:
    print(f"[noema-surface-init] {datetime.datetime.now().isoformat()}")
    print(f"  BASE: {BASE}")

    # ── Katalogi ────────────────────────────────────────────────────────────
    for subdir in ["analog", "zip_catalog", "registry", "phasenav"]:
        ensure_dir(BASE / subdir)
    print("  dirs: OK")

    # ── Pliki mmap (zero-fill przy braku / złym rozmiarze) ─────────────────
    for rel, size in MMAP_SIZES.items():
        create_zeros(BASE / rel, size)

    # ── Sentinel: CIEL binding ──────────────────────────────────────────────
    binding = BASE / "ciel_binding_status"
    binding.write_text("ACTIVE")
    print("  ciel_binding_status: ACTIVE")

    # ── Sentinel: zip catalog index ─────────────────────────────────────────
    catalog = BASE / "zip_catalog" / "index.jsonl"
    if not catalog.exists():
        catalog.write_text("")
    print("  zip_catalog/index.jsonl: OK")

    # ── Sentinel: phasenav surface (alias do BASE dla zgodności) ───────────
    phasenav = BASE / "phasenav"
    for name in ("phi", "omega", "tau", "gravity", "flavor", "tick"):
        link_target = BASE / name
        alias = phasenav / name
        # Kopiuj rozmiar z BASE (już utworzony wyżej)
        if not alias.exists() and link_target.exists():
            alias.write_bytes(link_target.read_bytes())
            print(f"  phasenav/{name}: seeded")

    # ── /tmp: ciel_hardbinding.jsonl ────────────────────────────────────────
    hardbinding = TMP / "ciel_hardbinding.jsonl"
    if not hardbinding.exists():
        entry = {
            "ts": datetime.datetime.now().isoformat(),
            "event": "surface_init",
            "ciel_binding_status": "ACTIVE",
            "source": "noema-surface-init.service",
        }
        hardbinding.write_text(json.dumps(entry) + "\n")
        print("  /tmp/ciel_hardbinding.jsonl: seeded")

    # ── /tmp: ciel_binding_plus_log.jsonl ──────────────────────────────────
    plus_log = TMP / "ciel_binding_plus_log.jsonl"
    if not plus_log.exists():
        plus_log.write_text("")
        print("  /tmp/ciel_binding_plus_log.jsonl: created")

    # ── Imaginal surface (/dev/shm/ciel_noema_imaginal) ────────────────────
    # Required by noema-kuramoto.service. Same field layout as main surface,
    # separate directory so kuramoto can own it exclusively.
    ensure_dir(IMAGINAL)
    for rel, size in MMAP_SIZES.items():
        if "/" not in rel:  # skip analog/* sub-fields
            create_zeros(IMAGINAL / rel, size)
    print(f"  imaginal surface: OK ({IMAGINAL})")

    # ── Podsumowanie ─────────────────────────────────────────────────────────
    files = list(BASE.rglob("*"))
    dirs  = [f for f in files if f.is_dir()]
    blobs = [f for f in files if f.is_file()]
    print(f"  DONE: {len(dirs)} dirs, {len(blobs)} files in {BASE}")
    sys.exit(0)


if __name__ == "__main__":
    main()
