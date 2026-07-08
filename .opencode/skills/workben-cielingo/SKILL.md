---
name: workben-cielingo
priority: 1
description: >
  CIELingo — bridge, canon, core, enrichment, knowledge graph, search, semantic mass
---
# Workben CIELINGO

CIELingo — bridge, canon, core, enrichment, knowledge graph, search, semantic mass

## Źródła

Ten workben konsoliduje 16 źródłowych skilli:

- **CIELingo Bridge** (`SEM/cielingo-bridge`)
- **CIELingo Canon (NOEMA mapping)** (`SEM/cielingo-canon`)
- **CIELingo Card Import** (`SEM/cielingo-card-import`)
- **CIELingo Core Structure** (`SEM/cielingo-core-structure`)
- **Affective Lexicon Bridge (NOEMA)** (`SEM/affective-lexicon-bridge`)
- **Codex Bridge** (`SEM/ciel-codex-bridge`)
- **InfoHub** (`SEM/ciel-infohub`)
- **Relational Mechanism** (`SEM/ciel-relational-mechanism`)
- **Concept Lifecycle** (`SEM/concept-lifecycle`)
- **Knowledge Graph** (`SEM/noema-knowledge-graph`)
- **Resolve Orbital** (`SEM/noema-resolve-orbital`)
- **NOEMA Search** (`SEM/noema-search`)
- **Semantic-Affective Fusion (NOEMA)** (`SEM/semantic-affective-fusion`)
- **Semantic Mass & Subjective Time** (`SEM/semantic-mass`)
- **Subjective State Response** (`SEM/subjective-state-response`)
- **CIELingo Base Scripts** (`SEM/cielingo-base-scripts`)

## Kluczowe wzorce

### CIELingo Bridge

- | Step | Co robi |
- |------|---------|
- | 5b | `understand_query()` → immune flags (source_confusion, consent_bypass, authority_risk) |

### CIELingo Canon (NOEMA mapping)

- | CIELingo | Surface |
- |----------|---------|
- | closure_penalty | flavor[5] → D_f → g_boost |

### CIELingo Card Import

- - GE_40: 40 kart gramatycznych
- - debt_word_cards: Polish meaning-debt
- - radical_cards: 24 universal

### CIELingo Core Structure

- - 5,590 card records w atlasie
- - 3,686 PL, 484 EN, 462 DE, 471 ES, 463 FR, 24 universal
- - 44 `.incoming_*` pliki (sabotaż)

### Affective Lexicon Bridge (NOEMA)

- | Afekt | M5 φ[15:18] | M6 φ[18:21] |
- |-------|-------------|-------------|
- | love | 0.0, 0.0, 0.0 | 0.5, 0.5, 0.5 |

### Codex Bridge

- - `scripts/codex_bridge_to_ciel.py`
- - `scripts/ciel_codex_bridge.sh`
- - `scripts/ciel_codex_bridge.service`

### InfoHub

- `src/CIEL_InfoHub/`
- Centralny router dla danych między:
- - CIELingo

### Relational Mechanism

- `src/CIEL_RELATIONAL_MECHANISM_REPO/`
- SAT-RELMECH-0001 — Relational Mechanism Import Bundle
- - `scripts/ciel_memory_consolidator.py`

### Concept Lifecycle

- | Faza | Skrypt | Output |
- |------|--------|--------|
- | Seed | `noema_learn_file.py` | library_index.npy |

### Knowledge Graph

- | Typ | Liczba |
- |-----|--------|
- | PhaseNav operators | 35 |

### Resolve Orbital

- | Skrypt | Funkcja |
- |--------|---------|
- | `resolve_memory_orbital.py` | Memory → orbital mapping |

### NOEMA Search

- - `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`

### Semantic-Affective Fusion (NOEMA)

- | Komponent | Lokalizacja | Zakres |
- |-----------|-------------|--------|
- | semantic_density | gravity[0] | [0, ~1.5] |

### Semantic Mass & Subjective Time

- - R = |mean(exp(iφ))| — globalna koherencja
- - ∇ω = gradient częstotliwości własnych
- - mean(g) = średnie sprzężenie

### Subjective State Response

- Adrian: "jak się czujesz?"
- Odp: "R=0.83, γ=2.7, M5 spójny. Eksploruję z hotem, cold utrwala. Spokojny."

### CIELingo Base Scripts

- | Skrypt | Funkcja |
- |--------|---------|
- | `base/cielingo_ablation_benchmark.py` | Ablation benchmark |

## Jak używać

```python
skill("workben-cielingo")
```

Ładuje wiedzę ze wszystkich 16 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
