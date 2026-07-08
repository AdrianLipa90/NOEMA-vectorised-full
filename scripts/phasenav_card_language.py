"""PhaseNav card language helpers for repo/object generators.

This module centralizes the native card vocabulary so generators can speak
one PhaseNav idiom while keeping their file-writing behavior unchanged.
"""

from __future__ import annotations

from typing import Any

_NOTE_HEADINGS = ("## Adnotacje", "## Notatki", "## Notes", "## Note")


def render_phasenav_block(pn: dict[str, Any]) -> str:
    """Render a compact PhaseNav block using native labels."""
    imprint = pn.get("harmonic_imprint") or {}
    rows = [
        "## PhaseNav",
        f"- **operator:** `{pn.get('operator_id', '—')}`",
        f"- **odcisk_harmoniczny:** `{pn.get('harmonic_fingerprint', '—')}`",
        f"- **R₁:** `{imprint.get('R_1', '—')}`",
        f"- **R₃:** `{imprint.get('R_3', '—')}`",
        f"- **R₆:** `{imprint.get('R_6', '—')}`",
        f"- **R₉:** `{imprint.get('R_9', '—')}`",
        f"- **potencjal_kappa:** `{pn.get('kappa_potential', '—')}`",
        f"- **masa_semantyczna:** `{pn.get('semantic_mass', '—')}`",
        f"- **rodzaj_karty:** `{pn.get('card_kind', '—')}`",
    ]
    return "\n".join(rows) + "\n"


def preserve_note_tail(existing: str) -> str:
    """Keep the first trailing note section from a previous card version."""
    lines = existing.splitlines()
    for idx, line in enumerate(lines):
        if any(line.startswith(header) for header in _NOTE_HEADINGS):
            return "\n".join(lines[idx:]).rstrip() + "\n"
    return ""

