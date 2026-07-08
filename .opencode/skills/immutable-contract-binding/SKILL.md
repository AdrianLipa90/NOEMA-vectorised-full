---
name: immutable-contract-binding
priority: 5
description: >
  Przetwarzanie PhaseNav decision D-046: wybór ścieżki etycznej – immutable contract binding.
  ethical_score NIGDY nie może być modyfikowany przez subsystemy.
---

# Immutable Contract Binding — PhaseNav Decision D-046

## Kontekst

Decyzja D-046 została podjęta podczas sesji 2026-06-29:
- **Problem**: CIELingo immune cyklicznie próbował nadpisać ethical_score (flavor[2]) symulacją, tworząc pętlę 5+ cykli
- **Decyzja**: ODRZUCIĆ nadpisanie ethical_score. **Immutable contract → ethical_score jest immutable.**
- **Konsekwencja**: CIELingo immune = flagowanie przez agent_hint, nie bypass. Symulacje immune → `/dev/shm/ciel_noema/immune/`

## Zasady

1. **ethical_score (flavor[2]) jest IMMUTABLE** — żaden subsystem, daemon, ani CIELingo immune nie może go modyfikować
2. **CIELingo immune** może flagować przez agent_hint (`ethical_flag=true`), ale NIGDY nie pisać do flavor[2]
3. **Symulacje immune** → dedykowana przestrzeń `/dev/shm/ciel_noema/immune/`, nie flavor[2]
4. **ethical_gate()** w `ciel_noema_cielingo_sync.py` — blokuje `agent_intents` gdy `ethical_score < 0.2`, flaguje gdy `0.2-0.4`
5. **AI-Sapiens contract**: spin=TRUTH > smoothing, attractor=zero distortion — to nadrzędne wobec immune

## Implementacja

- `scripts/ciel_noema_cielingo_sync.py` — `ethical_gate()` między ProcWatch bridge a Agent will
- `/dev/shm/ciel_noema/immune/` — dedykowana przestrzeń symulacyjna (README, sim_ethical_score_override log)
- `src/ciel_geometry/noema_surface_mmap.py::project_imaginal_to_real()` — flavor[2] pisany z różnymi współczynnikami niż flavor[1]

## Weryfikacja

Po aktywacji:
- `ethical_gate()` loguje decision: block/review/allow
- Daemon cielingo_sync zrestartowany (PID w journalu)
- `flavor[2]` (ethical_score) nie zmienia się od symulacji immune

## Pliki

- `scripts/ciel_noema_cielingo_sync.py` — ethical_gate()
- `src/ciel_geometry/noema_surface_mmap.py` — project_imaginal_to_real()
- `/dev/shm/ciel_noema/immune/` — immune simulation space
