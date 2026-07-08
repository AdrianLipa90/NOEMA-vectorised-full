#!/usr/bin/env python3
"""NOEMA ZIP Catalog — indeksuje zawartość archiwów CIEL bez wypakowywania.

Kataloguje strukturę wszystkich ZIPów w REPO/*.zip, zapisuje indeks do
/dev/shm/ciel_noema/zip_catalog/ jako JSONL + PhaseNav enrichment per plik.

Usage (dry-run):
    python scripts/catalog_zips_noema.py --dry-run

Usage (real):
    python scripts/catalog_zips_noema.py

Wymagane: python3 -c "import zipfile"  (stdlib)
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
NOEMA = Path("/dev/shm/ciel_noema")
CATALOG_DIR = NOEMA / "zip_catalog"

# System dirs to skip entirely (avoid /proc, /sys, etc.)
SKIP_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "node_modules", "venv", ".venv",
    ".npm", ".cargo", ".cache", ".local/share/Trash",
    "/proc", "/sys", "/dev", "/run", "/snap", "/lost+found",
    "/boot", "/lib", "/lib64", "/lib32", "/sbin", "/bin", "/usr/sbin", "/usr/bin",
    "/usr/lib", "/usr/lib64", "/usr/lib32", "/usr/share", "/usr/include",
    "/usr/src/linux", "/usr/src/linux-headers*",
    "/var/lib/apt", "/var/cache", "/var/log",
    "/etc", "/opt/tor-browser", "/opt/google",
    "AppData/Local/Temp", "AppData/Local/Microsoft",
}
# Prefix-based skips (e.g. /snap/*, /var/lib/docker/*)
SKIP_PREFIXES = ("/proc/", "/sys/", "/dev/", "/run/", "/snap/", "/lost+found/")


def _walk_zips(root: Path) -> list[Path]:
    """odwiedza drzewo z obsługą PermissionError zamiast rglob."""
    zips: list[Path] = []
    try:
        for entry in os.scandir(root):
            try:
                if entry.is_dir(follow_symlinks=False):
                    name = entry.name
                    if name in SKIP_DIRS:
                        continue
                    p = Path(entry.path).resolve()
                    sp = str(p)
                    if any(sp.startswith(pref) for pref in SKIP_PREFIXES):
                        continue
                    zips.extend(_walk_zips(p))
                elif entry.name.endswith(".zip"):
                    p = Path(entry.path)
                    if str(p).startswith("/dev/shm"):
                        continue
                    zips.append(p)
            except PermissionError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/catalog_zips_noema.py:67 quiet except scope=_walk_zips reason=continue")
                continue
            except OSError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/catalog_zips_noema.py:69 quiet except scope=_walk_zips reason=continue")
                continue
    except PermissionError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/catalog_zips_noema.py:71 quiet except scope=_walk_zips reason=pass")
        pass
    return zips


def find_zips(root: Path) -> list[Path]:
    """Znajdź wszystkie pliki .zip w drzewie z omijaniem systemowych ścieżek."""
    root = root.resolve()
    return sorted(set(_walk_zips(root)))


def catalog_zip(zip_path: Path) -> dict[str, Any]:
    """Wypisz zawartość ZIPa bez wypakowywania — zwraca metadane + spis plików."""
    info = {
        "zip_path": str(zip_path),
        "zip_size_mb": round(zip_path.stat().st_size / 1_048_576, 2),
        "zip_mtime": zip_path.stat().st_mtime,
        "entries": [],
        "total_files": 0,
        "total_dirs": 0,
        "total_size_uncompressed_mb": 0.0,
        "languages": {},
        "extensions": {},
        "error": None,
    }
    try:
        import zipfile
        with zipfile.ZipFile(zip_path, "r") as zf:
            for zi in zf.infolist():
                entry = {
                    "path": zi.filename,
                    "size": zi.file_size,
                    "compress_size": zi.compress_size,
                    "is_dir": zi.is_dir(),
                    "date": tuple(zi.date_time) if zi.date_time else None,
                }
                info["entries"].append(entry)
                if zi.is_dir():
                    info["total_dirs"] += 1
                else:
                    info["total_files"] += 1
                    info["total_size_uncompressed_mb"] += zi.file_size / 1_048_576
                    ext = Path(zi.filename).suffix.lower()
                    info["extensions"][ext] = info["extensions"].get(ext, 0) + 1
                    lang = _lang_from_ext(ext)
                    info["languages"][lang] = info["languages"].get(lang, 0) + 1
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/catalog_zips_noema.py:117 quiet except scope=catalog_zip reason=assign_fallback")
        info["error"] = str(e)

    info["total_size_uncompressed_mb"] = round(info["total_size_uncompressed_mb"], 2)
    info["languages"] = dict(sorted(info["languages"].items(), key=lambda x: -x[1]))
    info["extensions"] = dict(sorted(info["extensions"].items(), key=lambda x: -x[1]))
    return info


def _lang_from_ext(ext: str) -> str:
    return {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".md": "markdown", ".json": "json", ".yaml": "yaml", ".yml": "yaml",
        ".csv": "csv", ".txt": "text", ".html": "html", ".css": "css",
        ".sh": "shell", ".toml": "toml", ".cfg": "config", ".ini": "config",
        ".jpg": "image", ".png": "image", ".gif": "image", ".svg": "image",
        ".pdf": "pdf", ".zip": "archive", ".tar": "archive", ".gz": "archive",
        ".wav": "audio", ".mp3": "audio", ".flac": "audio",
        ".sql": "sql", ".db": "database", ".sqlite": "database",
    }.get(ext, "other")


def write_catalog(zip_infos: list[dict], dry_run: bool = False) -> Path:
    """Zapisz katalog do NOEMA z PhaseNav enrichment per entry."""
    if dry_run:
        print("[DRY-RUN] pomijam zapis")
        return CATALOG_DIR / "index.jsonl"

    CATALOG_DIR.mkdir(parents=True, exist_ok=True)

    # Główny indeks
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from ciel_geometry.phasenav.enrichment import phasenav_enrich
        HAVE_PN = True
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/catalog_zips_noema.py:152 quiet except scope=write_catalog reason=assign_fallback")
        HAVE_PN = False

    lines: list[str] = []
    for zi in zip_infos:
        # PhaseNav dla całego archiwum
        pn = {}
        if HAVE_PN:
            try:
                pn = phasenav_enrich(f"zip:{Path(zi['zip_path']).stem}", Path(zi['zip_path']).name)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/catalog_zips_noema.py:162 quiet except scope=write_catalog reason=assign_fallback")
                pn = {}

        record = {
            "zip_path": zi["zip_path"],
            "size_mb": zi["zip_size_mb"],
            "mtime": zi["zip_mtime"],
            "total_files": zi["total_files"],
            "total_dirs": zi["total_dirs"],
            "uncompressed_mb": zi["total_size_uncompressed_mb"],
            "languages": zi["languages"],
            "extensions": zi["extensions"],
            "phasenav": pn,
            "entries": zi["entries"],
            "error": zi["error"],
        }
        lines.append(json.dumps(record, default=str))

    index_path = CATALOG_DIR / "index.jsonl"
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Podsumowanie
    summary = {
        "total_zips": len(zip_infos),
        "total_files": sum(z["total_files"] for z in zip_infos),
        "total_size_mb": round(sum(z["zip_size_mb"] for z in zip_infos), 2),
        "total_uncompressed_mb": round(sum(z["total_size_uncompressed_mb"] for z in zip_infos), 2),
        "languages_aggregated": _merge_counts(zip_infos, "languages"),
        "extensions_aggregated": _merge_counts(zip_infos, "extensions"),
        "catalog_time": time.time(),
    }
    (CATALOG_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Manifest — ścieżki do plików w NOEMA
    manifest = {
        "index": str(index_path),
        "summary": str(CATALOG_DIR / "summary.json"),
        "time": time.time(),
    }
    (CATALOG_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return index_path


def _merge_counts(zip_infos: list[dict], key: str) -> dict:
    merged: dict[str, int] = {}
    for z in zip_infos:
        for k, v in z.get(key, {}).items():
            merged[k] = merged.get(k, 0) + v
    return dict(sorted(merged.items(), key=lambda x: -x[1]))


def main():
    import argparse
    ap = argparse.ArgumentParser(description="NOEMA ZIP Catalog")
    ap.add_argument("--dry-run", action="store_true", help="Tylko wypisz, nie zapisuj")
    ap.add_argument("--parallel", type=int, default=4, help="Maks. procesów równoległych")
    ap.add_argument("--root", type=str, default=str(ROOT), help="Katalog źródłowy")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    print(f"[ZIP Catalog] szukam ZIPów w {root}")
    zips = find_zips(root)
    print(f"[ZIP Catalog] znaleziono {len(zips)} archiwów")

    if not zips:
        print("[ZIP Catalog] brak ZIPów — nic do roboty")
        return

    # Katalogowanie
    zip_infos: list[dict] = []
    if args.parallel > 1 and len(zips) > 1:
        with ProcessPoolExecutor(max_workers=args.parallel) as pool:
            fut = {pool.submit(catalog_zip, zp): zp for zp in zips}
            for f in as_completed(fut):
                zp = fut[f]
                zi = f.result()
                zip_infos.append(zi)
                ok = "[OK]" if zi["error"] is None else f"[ERR] {zi['error']}"
                print(f"  {ok} {zp.name} ({zi['total_files']} plików, {zi['zip_size_mb']} MB)")
        zip_infos.sort(key=lambda x: x["zip_path"])
    else:
        for zp in zips:
            zi = catalog_zip(zp)
            zip_infos.append(zi)
            ok = "[OK]" if zi["error"] is None else f"[ERR] {zi['error']}"
            print(f"  {ok} {zp.name} ({zi['total_files']} plików, {zi['zip_size_mb']} MB)")

    # Podsumowanie
    total_files = sum(z["total_files"] for z in zip_infos)
    total_mb = sum(z["zip_size_mb"] for z in zip_infos)
    total_uncomp = sum(z["total_size_uncompressed_mb"] for z in zip_infos)
    print(f"\n  Razem: {len(zips)} archiwów, {total_files} plików, {total_mb:.1f} MB (skompresowane) / {total_uncomp:.1f} MB (surowy)")

    if args.dry_run:
        print("\n  [DRY-RUN] koniec — nic nie zapisano")
        return

    if not NOEMA.exists():
        print(f"\n  [WARN] {NOEMA} nie istnieje — katalog zapisany lokalnie")
        (ROOT / ".zip_catalog").mkdir(parents=True, exist_ok=True)
        (ROOT / ".zip_catalog" / "index.jsonl").write_text(
            "\n".join(json.dumps(z, default=str) for z in zip_infos) + "\n"
        )
        print(f"  Zapisano: {ROOT / '.zip_catalog' / 'index.jsonl'}")
        return

    index_path = write_catalog(zip_infos)
    print(f"\n  [OK] Katalog zapisany:")
    print(f"    indeks:  {index_path}")
    print(f"    summary: {CATALOG_DIR / 'summary.json'}")
    print(f"    manifest: {CATALOG_DIR / 'manifest.json'}")


if __name__ == "__main__":
    main()
