---
name: doc-security
priority: 4
description: >
  >
---
# Doc: SECURITY.md

**Plik**: `SECURITY.md` (47 linii)

Zasady:
- Żadnych API keys, tokens, passwords w repo
- Secrets w `~/Pulpit/CIEL_memories/secrets/`
- `.gitignore` wyklucza secrets/
- Secret loader: `cielyngo.secret_loader.load_secret()`

## Zrodlo

- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/vocabulary/COMPLETE_DOCUMENTATION.md`
- `src/ciel-omega-demo-main/docs/Studies/Metatime-main/Docs.md`
- `src/ciel-omega-demo-main/docs/Studies/Metatime-main/documents/Docs.md`
