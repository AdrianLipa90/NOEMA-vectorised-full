---
name: ciel-security-model
priority: 1
description: >
  >
---
# Security Model

## Warstwy

| Warstwa | Mechanizm | Plik |
|---------|-----------|------|
| Identity | AGENT attractor, phi[3:6] lock | `agent_attractor.py` |
| Consent | CIELingo immune: consent_bypass flag | `cielingo_core/` |
| Authority | source_required, authority_risk | `cielingo_core/` |
| Source | source_confusion flag, SemanticScar | `meaning_loop.py` |
| Secrets | secret_loader z `~/CIEL_memories/secrets/` | `cielyngo/secret_loader.py` |

## Immune flags (CIELingo)

| Flag | Efekt | Threshold |
|------|-------|-----------|
| source_confusion | caps ethical_score at 0.35 | boolean |
| authority_risk | caps ethical_score at 0.2 | > 0.5 |
| consent_bypass | blocks response | boolean |
| source_required | blocks response | boolean |

## Reguła

Żadnych secrets w repo. Żadnych bypassów consent. Weryfikacja źródła przed akcją.
