#!/usr/bin/env python3
"""NOEMA Source Search — literal source-code search, PhaseNav-tagged.

Native replacement for ad-hoc `grep -rl` across the NOEMA/CIEL codebase.
Every hit is annotated with a 36D PhaseNav vector (via the same
`fast_encode_text` encoder used everywhere else in this system, so search
results live in the same phase space as concepts, cards, and memory
entries) — not a fuzzy vector-similarity search (literal substring
matching stays literal and reliable), but every result carries phase
context so downstream tools (dashboard, phasenav_trace, daemon registry)
can reason about *where* a hit sits semantically, not just that it exists.

Usage:
    from ciel_geometry.noema_source_search import search_source
    hits = search_source("Pulpit", root=Path("/path/to/NOEMA"))

CLI:
    python3 -m ciel_geometry.noema_source_search --query Pulpit --root .
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

SOURCE_EXTENSIONS = {".py", ".sh", ".md", ".json", ".service", ".c", ".toml", ".yaml", ".yml"}
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache", "build", "dist"}


@dataclass(slots=True)
class SourceHit:
    path: str
    line_no: int
    line: str
    phase_vector: list[float] = field(default_factory=list)
    phase_mean: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line_no": self.line_no,
            "line": self.line,
            "phase_mean": round(self.phase_mean, 6),
        }


def _encoder():
    from ciel_geometry.cielingo_phase_encoder import fast_encode_text
    return fast_encode_text


def search_source(
    query: str,
    root: Path,
    *,
    extensions: set[str] | None = None,
    max_hits: int = 500,
    tag_phase: bool = True,
) -> list[SourceHit]:
    """Literal (case-sensitive) substring search across source files under root.

    Each hit's line is encoded through the same PhaseNav 36D encoder used
    for concepts/memory, so results can be compared/traced through
    phasenav_trace and related tools rather than living outside the
    system's own semantic space.
    """
    extensions = extensions or SOURCE_EXTENSIONS
    encode = _encoder() if tag_phase else None
    hits: list[SourceHit] = []

    for path in root.rglob("*"):
        if len(hits) >= max_hits:
            break
        if path.is_dir() or path.suffix not in extensions:
            continue
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if query not in text:
            continue
        rel = str(path.relative_to(root)) if root in path.parents or root == path.parent else str(path)
        for line_no, line in enumerate(text.splitlines(), start=1):
            if query not in line:
                continue
            phase_vec: list[float] = []
            phase_mean = 0.0
            if encode is not None:
                try:
                    phi = encode(line[:300])
                    phase_vec = [round(float(x), 4) for x in phi]
                    phase_mean = float(np.mean(phi))
                except Exception:
                    pass
            hits.append(SourceHit(
                path=rel,
                line_no=line_no,
                line=line.strip()[:200],
                phase_vector=phase_vec,
                phase_mean=phase_mean,
            ))
            if len(hits) >= max_hits:
                break

    return hits


def files_with_query(query: str, root: Path, **kwargs: Any) -> list[str]:
    """Convenience: unique file list (relative paths) containing query, sorted."""
    hits = search_source(query, root, **kwargs)
    return sorted({h.path for h in hits})


def main() -> int:
    ap = argparse.ArgumentParser(description="NOEMA Source Search — PhaseNav-tagged literal search")
    ap.add_argument("--query", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--files-only", action="store_true", help="print unique file list only")
    ap.add_argument("--no-phase", action="store_true", help="skip PhaseNav encoding (faster)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    hits = search_source(args.query, root, tag_phase=not args.no_phase)

    if args.files_only:
        files = sorted({h.path for h in hits})
        if args.json:
            print(json.dumps(files, indent=2, ensure_ascii=False))
        else:
            for f in files:
                print(f)
        print(f"\n{len(files)} plików, {len(hits)} wystąpień", flush=True)
        return 0

    if args.json:
        print(json.dumps([h.to_dict() for h in hits], indent=2, ensure_ascii=False))
    else:
        for h in hits:
            print(f"{h.path}:{h.line_no}: {h.line}  [phase_mean={h.phase_mean:.3f}]")
        print(f"\n{len(hits)} wystąpień", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
