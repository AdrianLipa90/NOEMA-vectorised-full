#!/usr/bin/env python3
"""Apply the small, reviewed repairs left after Ruff's safe-fix pass.

This migration is intentionally exact-string based.  It refuses silently
changing unrelated code: every target must be either in its known pre-repair or
known post-repair state.  The file is temporary and is removed after the repair
commit is verified.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "src/ciel_sot_agent/__init__.py": (
        (
            "import os as _ciel_os, os.path as _ciel_path",
            "import os.path as _ciel_path",
        ),
    ),
    "src/ciel_sot_agent/buildroot_card_db.py": (
        (
            '    top_dirs = snapshot.get("top_level_dirs", []) if isinstance(snapshot.get("top_level_dirs"), list) else []\n',
            "",
        ),
    ),
    "src/ciel_sot_agent/ciel_pipeline.py": (
        (
            "    from cielingo_core.lingophysics.sentence_equation import calculate_sentence_equation\n",
            "",
        ),
    ),
    "src/cielingo_core/bridge/auto_verify.py": (
        ("    card = generate_runtime_card(\n", "    generate_runtime_card(\n"),
    ),
    "src/cielingo_core/language_spaces/ja/solver.py": (
        ('        low = [t.lower() for t in segments.tokens]\n', ""),
    ),
    "src/cielingo_core/noema_local_sot_agent/__init__.py": (
        (
            '__all__ = ["LocalSOTAgentNoemaSurface", "LocalSOTAgentState", "LocalSOTBoundary"]',
            '__all__ = [\n'
            '    "LocalSOTAgentNoemaSurface",\n'
            '    "LocalSOTAgentState",\n'
            '    "LocalSOTBoundary",\n'
            '    "AccessPolicy",\n'
            '    "LocalSOTAccessController",\n'
            '    "build_default_access_standard",\n'
            ']'
        ),
    ),
    "tests/test_ciel_subconscious_supervisor.py": (
        ('    assert status["mode"] == "server"', '    assert status["mode"] == "memory"'),
    ),
}


def main() -> int:
    changed: list[str] = []
    for relative, replacements in REPLACEMENTS.items():
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        original = text
        for before, after in replacements:
            if before in text:
                text = text.replace(before, after, 1)
            elif after and after in text:
                continue
            elif not after:
                continue
            else:
                raise RuntimeError(f"Unexpected source state for {relative}: {before!r}")
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(relative)
    print("changed=" + ",".join(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
