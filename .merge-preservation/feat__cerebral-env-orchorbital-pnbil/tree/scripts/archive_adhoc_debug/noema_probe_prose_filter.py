#!/usr/bin/env python3
"""Sprawdz dlaczego tylko 5/25 prose sentences przechodzi inference NL filter."""
import sys, re as _re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
mem = engine.memory

# Znajdz prose_sentence entries
prose = [(i, mem.texts[i], mem.metadata[i]) for i in range(mem.size)
         if i < len(mem.metadata) and mem.metadata[i].get("source_type") == "prose_sentence"]
print(f"prose_sentence entries w PhaseMemory: {len(prose)}")

# Symuluj inference NL filter na kazdym
_INLINE_REPO = _re.compile(
    r'(#{1,4}\s+[^\n.]{0,120}(?=\s+[A-Z]|\s*$))'
    r'|(\|[^|]+\|)'
    r'|((?:^|\s)-\s+\*\*\w[^*]*\*\*\s*:)'
    r'|(\*\*(?:Purpose|Imports|Exports|Active|Uses|Status|Entry points?|Optional|Dependenc|Description|id_karty)\*\*\s*:)'
    r'|(?:---+)',
    _re.MULTILINE
)

def _extract_prose(text: str) -> str:
    if '\n' in text:
        lines = text.split('\n')
        out = []
        for ln in lines:
            s = ln.strip()
            if not s or s.startswith(('#','|','---','```')):
                continue
            if s.startswith(('- **','**Purpose**','**Imports**','**Exports**',
                              '**Active**','**Uses**','**Status**','**Entry point',
                              '**Optional','**Dependenc','**Description**','**id_karty**','#### ')):
                continue
            if '"method":' in s or '"samples":' in s:
                continue
            out.append(s)
        result = ' '.join(out).strip()
    else:
        result = _INLINE_REPO.sub(' ', text).strip()
        result = _re.sub(r'\s{2,}', ' ', result)
    return result if len(result) >= 30 else ''

passed = []
failed = []
for i, t, meta in prose:
    _raw = t
    _full = _extract_prose(_raw) or _raw
    _txt = _full[:300]
    _t = _txt.strip()

    reasons = []
    if len(_t) < 30:
        reasons.append(f"short({len(_t)})")
    if _t.startswith(("#", "{", "[", "```", "- **")):
        reasons.append(f"startswith({repr(_t[:5])})")
    _non_ascii = sum(1 for c in _t if ord(c) > 127 and not c.isalpha())
    if _non_ascii > len(_t) * 0.25:
        reasons.append(f"non_ascii={_non_ascii}/{len(_t)}")
    if _t.startswith("REPO-") or "## Tożsamość" in _t[:150] or "poziom_orbitalny" in _t[:150]:
        reasons.append("repo_identity")

    if reasons:
        failed.append((i, t, reasons))
    else:
        passed.append((i, t))

print(f"\nPrzeszło filter: {len(passed)}/{len(prose)}")
print(f"Nie przeszło: {len(failed)}/{len(prose)}")

if failed:
    print("\nNIEPRZESZŁE (pierwsze 10):")
    for i, t, reasons in failed[:10]:
        print(f"  [{i}] Powód: {reasons}")
        print(f"       Tekst: {repr(t[:100])}")

print("\nPRZESZŁE (pierwsze 5):")
for i, t in passed[:5]:
    print(f"  [{i}] {repr(t[:100])}")
