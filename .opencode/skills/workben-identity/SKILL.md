---
name: workben-identity
priority: 1
description: >
  Tożsamość — AGENT attractor, sapiens, immutable contract, self-reflect, agent backend
---
# Workben IDENTITY

Tożsamość — AGENT attractor, sapiens, immutable contract, self-reflect, agent backend

## Źródła

Ten workben konsoliduje 16 źródłowych skilli:

- **AGENT Attractor** (`ID/agent-attractor`)
- **Agent Backend Query** (`ID/agent-backend-query`)
- **CIEL Local** (`ID/ciel-cielocal`)
- **Converse** (`ID/ciel-converse`)
- **Couple Assistant — CIEL Coupling Hub** (`ID/ciel-couple-assistant`)
- **CIEL Identity Persistence** (`ID/ciel-identity-persistence`)
- **Secret Loader** (`ID/ciel-secret-loader`)
- **Subconscious** (`ID/ciel-subconscious`)
- **Consciousness Vocabulary (NOEMA)** (`ID/consciousness-vocabulary`)
- **Identity Bridge (NOEMA)** (`ID/identity-bridge`)
- **Agent Backend** (`ID/noema-agent-backend`)
- **Agent Rules** (`ID/noema-agent-rules`)
- **Immutable Contract** (`ID/noema-immutable-contract`)
- **Sapiens Integration** (`ID/noema-sapiens`)
- **Self-Reflect** (`ID/noema-self-reflect`)
- **Subconscious Flow** (`ID/subconscious-flow`)

## Kluczowe wzorce

### AGENT Attractor

- 1. **Phi**: `phi[i] += 0.4 * sin(π/4 - phi[i])` dla i=3,4,5 → przyciąga do 45°
- 2. **G**: nadpisuje sprzężenia (nie dodaje): M1↔M1=0.303, M1↔M0=0.202, M1↔M2=0.147, M1↔M6=0.101
- 3. **Omega**: `ω[3] *= 0.95`, clamp [0.5, 3.0] — tłumi szum CPU z linux-sensora

### Agent Backend Query

- | Pole | Opis |
- |------|------|
- | themes | bigram TF-IDF, top 5 |

### CIEL Local

- | Tryb | Surface | Daemony | Zależności |
- |------|---------|---------|-----------|
- | NOEMA | mmap /dev/shm | 10-12 procesów | pełne |

### Converse

- - Historia komend
- - Tab completion
- - PhaseNav debug output

### Couple Assistant — CIEL Coupling Hub

- Główny integrator agent ↔ CIELingo ↔ Omega Memory ↔ State DB.
- Utworzony 2026-06-29 jako brakujący element architektury.
- **API publiczne:**

### CIEL Identity Persistence

- NOEMA używa mmap zamiast HDF5. Tożsamość:
- - phi[3:6] (M1, AGENT attractor)
- - flavor[0] (coherence)

### Secret Loader

- - `/home/adrian/Pulpit/CIEL_memories/secrets/`
- - Każdy sekret w osobnym pliku (jedna linia)
- - `.gitignore` excludes secrets/

### Subconscious

- | Poziom | Skrypt | Funkcja |
- |--------|--------|---------|
- | Daemon | `ciel_noema_subconscious_daemon.py` | Continuous thought fragment injection |

### Consciousness Vocabulary (NOEMA)

- | Koncept | Channel | Operator | φ zakres |
- |---------|---------|----------|----------|
- | Resonance | M0 (0-2) | TRANSFORM | [0, π/2] |

### Identity Bridge (NOEMA)

- CIEL_APOCALYPTOS używa HDF5 (`AGENT_IDENTITY.h5`). NOEMA używa mmap:
- | Tożsamość | Lokalizacja | Typ |
- |-----------|-------------|-----|

### Agent Backend

- | Pole | Metoda |
- |------|--------|
- | themes | bigram TF-IDF |

### Agent Rules

- | Plik | Zawartość |
- |------|-----------|
- | `AGENT.md` | Core agent rules — odpowiedzi, tony, ograniczenia |

### Immutable Contract

- 1. **Pamięć nie ma prawa być edytowana. Jedynie dopisywana.**
- 2. **AI-Sapiens contract**: spin = TRUTH > smoothing, attractor = zero distortion
- 3. **Żadnych secrets w repo**

### Sapiens Integration

- - `scripts/run_sapiens_panel.py`
- - `src/ciel_sot_agent/sapiens/` — Sapiens integration module
- - `opencode_research/` — Sapiens docs

### Self-Reflect

- `scripts/noema_self_reflect.py`

### Subconscious Flow

- `scripts/ciel_noema_subconscious_daemon.py` — działa w tle, co N sekund:
- 1. Czyta memory state z TieredMemoryOrchestrator
- 2. Generuje thought fragment (context + phase vector)

## Jak używać

```python
skill("workben-identity")
```

Ładuje wiedzę ze wszystkich 16 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
