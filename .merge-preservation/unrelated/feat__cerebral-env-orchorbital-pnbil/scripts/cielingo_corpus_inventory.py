#!/usr/bin/env python3
"""Produce a provenance-first CIEL corpus inventory without ingesting content.

This implementation remains under its historical filename for compatibility;
the public generic command is ``ciel_corpus_inventory.py``. It inventories
source trees, ZIPs, code, documents and data by hash and policy signal.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re
import zipfile


PRIVATE = re.compile(r"chat|conversation|transcript|raw[_ -]?log|personal|private|secret|credential|key", re.I)
RESTRICTED = re.compile(r"restricted|pferl|evaluation|no[_ -]?ai|do[_ -]?not[_ -]?train", re.I)
PUBLIC_HINT = re.compile(r"publication|public|open[_ -]?protocol|reproduc|docs?|tests?|source", re.I)


@dataclass(frozen=True)
class InventoryEntry:
    path: str
    sha256: str
    size: int
    kind: str
    lane: str
    reason: str
    archive_members: int = 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def classify(path: Path, members: tuple[str, ...] = ()) -> tuple[str, str]:
    text = "\n".join((str(path), *members))
    if RESTRICTED.search(text):
        return "quarantine", "restricted-or-ai-prohibited material"
    if PRIVATE.search(text):
        return "private", "personal or sensitive-name signal; owner review required"
    if PUBLIC_HINT.search(text):
        return "public", "public/reproducibility-name signal; license review still required"
    return "quarantine", "no reliable publication or license signal"


def inspect(path: Path) -> InventoryEntry:
    members: tuple[str, ...] = ()
    kind = path.suffix.casefold().lstrip(".") or "file"
    if path.suffix.casefold() == ".zip":
        try:
            with zipfile.ZipFile(path) as archive:
                members = tuple(info.filename for info in archive.infolist() if not info.is_dir())
        except zipfile.BadZipFile:
            return InventoryEntry(str(path), sha256_file(path), path.stat().st_size, "zip", "quarantine", "invalid zip")
    lane, reason = classify(path, members)
    return InventoryEntry(str(path), sha256_file(path), path.stat().st_size, kind, lane, reason, len(members))


def scan(root: Path) -> list[InventoryEntry]:
    entries: list[InventoryEntry] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        entries.append(inspect(path))
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--zip-only", action="store_true")
    args = parser.parse_args()
    entries = scan(args.root)
    if args.zip_only:
        entries = [entry for entry in entries if entry.kind == "zip"]
    payload = {"schema": "CIEL_CORPUS_INVENTORY_V0_1", "root": str(args.root), "entries": [asdict(entry) for entry in entries]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"entries": len(entries), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
