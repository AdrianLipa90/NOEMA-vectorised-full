---
name: data-ingestion-pwn-oxford-open
priority: 3
description: >
  >
---
# 07. Data Ingestion: PWN, Oxford and Open Lexical Sources

## Contents

- **Rule zero**: Do not scrape or redistribute proprietary dictionary content unless the license explicitly permits i
- **PWN**: PWN dictionaries are high-quality Polish lexical sources, but their data should be treated as propri Use pattern: ```tex
- **Oxford**: Oxford Dictionaries data should be accessed through the official Oxford Dictionaries API or another  Use pattern: ```tex
- **Open bootstrap alternatives**: Recommended for first implementation: - Open English WordNet for English synsets and relations. - Princeton WordNet wher
- **Import target format**: Every lexical entry should normalize to: ```yaml id: string language: en|pl lemma: string surface_forms: [] pos: NOUN|VE
- **Derived features**: Do not assume derived vectors are legally safe. Some licenses treat derived databases as derivative 

## Key Points

- Open English WordNet for English synsets and relations.
- Princeton WordNet where compatible.
- plWordNet/Słowosieć for Polish synsets and relations.
- Universal Dependencies treebanks for POS/dependency calibration.
- Wiktionary dumps for multilingual lexical hints, with strict license handling.

## Code

```
## Oxford

Oxford Dictionaries data should be accessed through the official Oxford Dictionaries API or another licensed Oxford Languages/OUP channel.

Use pattern:
```

```
## Open bootstrap alternatives

Recommended for first implementation:

- Open English WordNet for English synsets and relations.
- Princeton WordNet where compatible.
- plWordNet/Słowosieć for Polish synsets and relations.
- Universal Dependencies treebanks for POS/dependency calibration.
- Wiktionary dumps for multilingual lexical hints, with strict license handling.

## Import target format

Every lexical entry should normalize to:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/07_DATA_INGESTION_PWN_OXFORD_OPEN.md` (64 lines, 1740B)*