---
name: doc-setup
priority: 4
description: >
  >
---
# Doc: SETUP.md

**Plik**: `docs/SETUP.md` (267 linii)

Pokrywa:
- Prerequisites: Python 3.10+, numpy, (opcjonalnie scipy/h5py/cupy)
- Venv setup: `python3 -m venv .venv && pip install -e .`
- Systemd services: enable noema.target
- Konfiguracja: noema_config.json
- Pierwsze uruchomienie: `CIEL_CANON.py --up`
- Test: `CIEL_CANON.py --probe`

**Przeczytaj gdy**: nowa instalacja lub reinstalacja NOEMA.
