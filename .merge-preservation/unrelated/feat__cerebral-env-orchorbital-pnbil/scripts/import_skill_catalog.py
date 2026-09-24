#!/usr/bin/env python3
"""Snapshot and digest skill directories from named local skill sources.

Only actual directories containing ``SKILL.md`` are copied.  Alias symlinks
are resolved and deduplicated so the snapshot is reviewable rather than a
second, ambiguous runtime skill registry.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from typing import Iterable


@dataclass(frozen=True)
class SkillSnapshot:
    source_name: str
    source_path: str
    relative_path: str
    destination: str
    sha256: str
    title: str


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("#"):
            return line.lstrip("# ").strip()
    return path.parent.name


def _actual_skill_directories(source: Path) -> Iterable[Path]:
    seen: set[Path] = set()
    for skill_file in sorted(source.rglob("SKILL.md")):
        resolved = skill_file.resolve()
        try:
            resolved.relative_to(source.resolve())
        except ValueError:
            continue
        directory = resolved.parent
        if directory not in seen:
            seen.add(directory)
            yield directory


def snapshot_source(source_name: str, source: Path, destination_root: Path) -> list[SkillSnapshot]:
    if not source.exists():
        return []
    snapshots: list[SkillSnapshot] = []
    for directory in _actual_skill_directories(source):
        skill_file = directory / "SKILL.md"
        relative = directory.relative_to(source.resolve())
        destination = destination_root / source_name / relative
        if destination.exists():
            shutil.rmtree(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(directory, destination, symlinks=False)
        snapshots.append(
            SkillSnapshot(
                source_name=source_name,
                source_path=str(source.resolve()),
                relative_path=relative.as_posix(),
                destination=str(destination),
                sha256=_sha256(skill_file),
                title=_title(skill_file),
            )
        )
    return snapshots


def write_digest(destination_root: Path, snapshots: list[SkillSnapshot]) -> None:
    manifest = {
        "schema": "CIEL_SKILL_IMPORT_V0_1",
        "created_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "skill_count": len(snapshots),
        "skills": [asdict(snapshot) for snapshot in snapshots],
    }
    (destination_root / "SKILL_IMPORT_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Imported Skill Digest",
        "",
        "This is a read-only snapshot for review and provenance. It is not an active runtime registry.",
        "",
        f"- Skills copied: {len(snapshots)}",
        "- Alias symlinks: resolved and deduplicated",
        "- Secret/config files: not copied; only skill directories rooted at SKILL.md are included",
        "",
        "| Source | Skill | Title | SHA-256 |",
        "|---|---|---|---|",
    ]
    lines.extend(
        f"| {item.source_name} | `{item.relative_path}` | {item.title} | `{item.sha256}` |"
        for item in snapshots
    )
    (destination_root / "SKILL_IMPORT_DIGEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--source", action="append", default=[], metavar="NAME=PATH")
    args = parser.parse_args()
    sources: list[tuple[str, Path]] = []
    for value in args.source:
        name, separator, raw_path = value.partition("=")
        if not separator or not name or not raw_path:
            parser.error("--source must use NAME=PATH")
        sources.append((name, Path(raw_path).expanduser()))
    if not sources:
        parser.error("at least one --source is required")
    args.target.mkdir(parents=True, exist_ok=True)
    snapshots = [item for name, path in sources for item in snapshot_source(name, path, args.target)]
    write_digest(args.target, snapshots)
    print(json.dumps({"target": str(args.target), "skill_count": len(snapshots)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
