---
name: session-lifecycle
priority: 1
description: >
  >
---
# Session Lifecycle

## Start sesji

```bash
python3 scripts/ciel_session_hook.py start
```

1. Sprawdza daemony (registry)
2. Czyta surface state (phi, flavor, tick)
3. Czyta handoff.md (ostatni kontekst)
4. Inicjalizuje raw_logs dla tej sesji
5. Zapisuje timestamp + CIEL state

## Każdy prompt

Automatycznie przez CIEL system:
1. `process_user_input(text)` — enrichment
2. CIELingo immune check
3. MeaningLoop (scar detection)
4. PhaseNav enrichment

## Koniec sesji

```bash
python3 scripts/ciel_session_hook.py end
```

1. Konsolidacja raw_logs → memories_index.db
2. Phase memory save: `ciel_phase_memory.py save`
3. Status summary
4. Update handoff.md

## Plik

`scripts/ciel_session_hook.py`
