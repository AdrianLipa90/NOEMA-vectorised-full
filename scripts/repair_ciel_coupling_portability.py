#!/usr/bin/env python3
"""Replace host-specific binding paths with the current repository root."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "ciel_coupling.py"

REPLACEMENTS = (
    (
        '_CIEL_BINDING_LOG = Path("/tmp/ciel_hardbinding.jsonl")\n',
        '_CIEL_BINDING_LOG = Path("/tmp/ciel_hardbinding.jsonl")\n'
        '_PROJECT_ROOT = Path(__file__).resolve().parent.parent\n',
    ),
    (
        '    agents_path = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/AGENTS.md")',
        '    agents_path = _PROJECT_ROOT / "AGENTS.md"',
    ),
    (
        '    ll_path = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/LEARNED_LESSONS.md")',
        '    ll_path = _PROJECT_ROOT / "LEARNED_LESSONS.md"',
    ),
    (
        '            Path(f"/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/.opencode/skills/{skill}/SKILL.md"),\n'
        '            Path(f"/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/.opencode/skills/{skill}"),',
        '            _PROJECT_ROOT / ".opencode" / "skills" / skill / "SKILL.md",\n'
        '            _PROJECT_ROOT / ".opencode" / "skills" / skill,',
    ),
    (
        '        sys.path.insert(0, "/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/src")\n'
        '        from ciel_geometry.noema_surface_mmap import ensure_surface, read_surface_state',
        '        from ciel_geometry.noema_surface_mmap import ensure_surface, read_surface_state',
    ),
)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    for before, after in REPLACEMENTS:
        if before in text:
            text = text.replace(before, after, 1)
        elif after in text:
            continue
        else:
            raise RuntimeError(f"Unexpected source state: {before!r}")
    TARGET.write_text(text, encoding="utf-8")

    print("workflow_files=")
    for path in sorted((ROOT / ".github" / "workflows").iterdir()):
        print(path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
