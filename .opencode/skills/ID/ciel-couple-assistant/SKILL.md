---
name: ciel-couple-assistant
priority: 2
description: >
  >
---
# Couple Assistant — CIEL Coupling Hub

## Runtime

```bash
.venv/bin/python3 scripts/couple_assistant.py
```

## Module: `src/ciel_coupling.py`

Główny integrator agent ↔ CIELingo ↔ Omega Memory ↔ State DB.
Utworzony 2026-06-29 jako brakujący element architektury.

**API publiczne:**
- `build_lingo_frame(text)` — enrichment semantyczne przez CIELingo
- `process_user_input(text)` — pełny pipeline: CIELingo → Omega Memory → PhaseNav
- `remember_exchange(user_msg, assistant_msg)` — zapis wymiany do TSM ledger
- `memory_stats()` — statystyki pamięci Omega (645+ entries)
- `health()` — status integracji wszystkich komponentów

**Crossref:** [`FUNCTIONS.md → ciel_coupling.py`](../../FUNCTIONS.md)

## Use

Interaktywnie lub jako daemon: wstrzykuje coupling między AGENT (M1) a assistant przez Omega Memory Bridge.

## Zrodlo

- `src/ciel_coupling.py`
- `src/ciel_geometry/omega_memory_bridge.py`
- `src/ciel_sot_agent/cielingo_bridge.py`
- `src/CIEL_Orbital_Foundation_Packk/CIEL_NATIVE_SYSTEM_BLUEPRINT_v0.md`
- `src/CIEL_Orbital_Foundation_Packk/01_CIEL_Orbital_Master_Plan.md`
- `src/CIEL_Orbital_Foundation_Packk/CIEL_ETHICS_AND_SEMANTIC_ACTION_ALGORITHM.md`
