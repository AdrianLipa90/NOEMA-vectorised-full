# Merge: Documentacja NOEMY

Wszystkie skille dokumentacyjne NOEMY: doc-* (21 skilli)

---

## Importy

Ten skill agreguje poniższe skille źródłowe:

- `doc-architecture` → [`.opencode/skills/doc-architecture/SKILL.md`](.opencode/skills/doc-architecture/SKILL.md) (19 linii)
- `doc-cards-system` → [`.opencode/skills/doc-cards-system/SKILL.md`](.opencode/skills/doc-cards-system/SKILL.md) (17 linii)
- `doc-ciel` → [`.opencode/skills/doc-ciel/SKILL.md`](.opencode/skills/doc-ciel/SKILL.md) (24 linii)
- `doc-cielingo` → [`.opencode/skills/doc-cielingo/SKILL.md`](.opencode/skills/doc-cielingo/SKILL.md) (19 linii)
- `doc-daemons` → [`.opencode/skills/doc-daemons/SKILL.md`](.opencode/skills/doc-daemons/SKILL.md) (18 linii)
- `doc-docs-index` → [`.opencode/skills/doc-docs-index/SKILL.md`](.opencode/skills/doc-docs-index/SKILL.md) (18 linii)
- `doc-ethics-contract` → [`.opencode/skills/doc-ethics-contract/SKILL.md`](.opencode/skills/doc-ethics-contract/SKILL.md) (16 linii)
- `doc-governance` → [`.opencode/skills/doc-governance/SKILL.md`](.opencode/skills/doc-governance/SKILL.md) (15 linii)
- `doc-immutable-contract` → [`.opencode/skills/doc-immutable-contract/SKILL.md`](.opencode/skills/doc-immutable-contract/SKILL.md) (18 linii)
- `doc-lns-lingophysics` → [`.opencode/skills/doc-lns-lingophysics/SKILL.md`](.opencode/skills/doc-lns-lingophysics/SKILL.md) (47 linii)
- `doc-lns-reports` → [`.opencode/skills/doc-lns-reports/SKILL.md`](.opencode/skills/doc-lns-reports/SKILL.md) (31 linii)
- `doc-memory-system` → [`.opencode/skills/doc-memory-system/SKILL.md`](.opencode/skills/doc-memory-system/SKILL.md) (20 linii)
- `doc-noema-documentation` → [`.opencode/skills/doc-noema-documentation/SKILL.md`](.opencode/skills/doc-noema-documentation/SKILL.md) (19 linii)
- `doc-omega-complete` → [`.opencode/skills/doc-omega-complete/SKILL.md`](.opencode/skills/doc-omega-complete/SKILL.md) (26 linii)
- `doc-orbital-foundation-pack` → [`.opencode/skills/doc-orbital-foundation-pack/SKILL.md`](.opencode/skills/doc-orbital-foundation-pack/SKILL.md) (29 linii)
- `doc-repo-guide` → [`.opencode/skills/doc-repo-guide/SKILL.md`](.opencode/skills/doc-repo-guide/SKILL.md) (24 linii)
- `doc-science-papers` → [`.opencode/skills/doc-science-papers/SKILL.md`](.opencode/skills/doc-science-papers/SKILL.md) (20 linii)
- `doc-security` → [`.opencode/skills/doc-security/SKILL.md`](.opencode/skills/doc-security/SKILL.md) (22 linii)
- `doc-setup` → [`.opencode/skills/doc-setup/SKILL.md`](.opencode/skills/doc-setup/SKILL.md) (20 linii)
- `doc-subsystems` → [`.opencode/skills/doc-subsystems/SKILL.md`](.opencode/skills/doc-subsystems/SKILL.md) (20 linii)
- `doc-surface-protocol` → [`.opencode/skills/doc-surface-protocol/SKILL.md`](.opencode/skills/doc-surface-protocol/SKILL.md) (18 linii)

---

## 1. doc-architecture

*Źródło: [`.opencode/skills/doc-architecture/SKILL.md`](.opencode/skills/doc-architecture/SKILL.md)*

---
name: doc-architecture
priority: 4
description: >
  >
---

**Plik**: `docs/ARCHITECTURE.md` (347 linii)

Pokrywa:
- System overview: 24 Kuramoto oscillators → 8 memory channels (M0-M7)
- 3-6-9 harmonic coupling
- CIELingo linguistic topology layer
- Tiered memory architecture
- Daemon architecture

**Przeczytaj gdy**: potrzebujesz high-level understanding całego systemu.


---

## 2. doc-cards-system

*Źródło: [`.opencode/skills/doc-cards-system/SKILL.md`](.opencode/skills/doc-cards-system/SKILL.md)*

---
name: doc-cards-system
priority: 4
description: >
  >
---

**Plik**: `docs/CARDS_SYSTEM.md` (215 linii)

3 systemy kart:
- **Nonlocal Cards** (JSON) — `cards/base/noema_nonlocal_db/` — architektura jako directed graph
- **Object Cards** (Markdown) — `docs/object_cards/` — runtime entities, moduły, mappingi
- **Word Cards** (JSONL) — `src/cielingo/cards/` — CIELingo linguistic engine

**Przeczytaj gdy**: potrzebujesz zrozumieć system kart NOEMA.


---

## 3. doc-ciel

*Źródło: [`.opencode/skills/doc-ciel/SKILL.md`](.opencode/skills/doc-ciel/SKILL.md)*

---
name: doc-ciel
priority: 4
description: >
  >
---

**Plik**: `CIEL.md` (116 linii)

Pokrywa:
- CIEL flow: user input → CielEngine → CIELingo ←→ NOEMA surface → response
- PhaseNav enrichment
- Memory consolidation
- Session management

**Przeczytaj gdy**: potrzebujesz zrozumieć jak CIEL przetwarza input → output.

## Zrodlo

- `scripts/ciel_memory_consolidator.py`
- `scripts/ciel_lora_train.py`
- `scripts/ciel_noema_x25519_exchange.py`


---

## 4. doc-cielingo

*Źródło: [`.opencode/skills/doc-cielingo/SKILL.md`](.opencode/skills/doc-cielingo/SKILL.md)*

---
name: doc-cielingo
priority: 4
description: >
  >
---

**Plik**: `docs/CIELINGO.md` (306 linii)

Pokrywa:
- Card-based radical lexicon (PL/EN/JA/ES/FR/DE/universal)
- Infinitive/modal grammar analysis
- Collatz-based semantic synchronization
- Tensor-scalar context fields
- Phase-token encoding → NOEMA surface

**Przeczytaj gdy**: potrzebujesz zrozumieć jak CIELingo mapuje język na powierzchnię NOEMA.


---

## 5. doc-daemons

*Źródło: [`.opencode/skills/doc-daemons/SKILL.md`](.opencode/skills/doc-daemons/SKILL.md)*

---
name: doc-daemons
priority: 4
description: >
  >
---

**Plik**: `docs/DAEMONS.md` (450 linii)

Pokrywa:
- Każdy daemon z osobna: purpose, CLI args, systemd service, interwał
- Kolejność startu (dependency chain)
- Registry heartbeat protocol
- Debugowanie i logowanie

**Przeczytaj gdy**: potrzebujesz szczegółów konkretnego daemona, flag CLI, lub troubleshooting.


---

## 6. doc-docs-index

*Źródło: [`.opencode/skills/doc-docs-index/SKILL.md`](.opencode/skills/doc-docs-index/SKILL.md)*

---
name: doc-docs-index
priority: 4
description: >
  >
---

**Plik**: `docs/INDEX.md` (188 linii)

Taxonomia stanu dokumentacji:
- **current**: zgodny z implementacją
- **transitional**: w trakcie aktualizacji
- **stale**: nieaktualny, może wprowadzać w błąd
- **planned-only**: tylko plan, brak implementacji

**Przeczytaj gdy**: chcesz wiedzieć którym dokumentom ufać.


---

## 7. doc-ethics-contract

*Źródło: [`.opencode/skills/doc-ethics-contract/SKILL.md`](.opencode/skills/doc-ethics-contract/SKILL.md)*

---
name: doc-ethics-contract
priority: 4
description: >
  >
---

| Plik | Rozmiar | Temat |
|------|---------|-------|
| `contracts/CIEL_ETHICS_AND_SEMANTIC_ACTION_ALGORITHM.md` | 82 lines | Algorytm etyczny CIEL |
| `contracts/IMMUTABILITY_POLICY.md` | 35 lines | Polityka niezmienności |
| `contracts/JOKEHEAL_BOUNDARY_PROTOCOL.md` | 55 lines | Granice żartów i uzdrowienia |
| `contracts/PRODUCTION_READINESS_PROTOCOL.md` | 101 lines | Gotowość produkcyjna |
| `contracts/SEMANTIC_ACTION_REFERENCE_CARD.md` | 67 lines | Karta referencyjna akcji semantycznych |


---

## 8. doc-governance

*Źródło: [`.opencode/skills/doc-governance/SKILL.md`](.opencode/skills/doc-governance/SKILL.md)*

---
name: doc-governance
priority: 4
description: >
  >
---

| Plik | Rozmiar | Temat |
|------|---------|-------|
| `governance/AGENT.md` | 57 lines | Agent governance rules |
| `governance/README.md` | 31 lines | Governance overview |
| `governance/contracts/RELATIONAL_FORMAL_PROTOCOL.md` | 104 lines | Formal protocol dla relacji |
| `governance/contracts/SAPIENS_PACKET_PROTOCOL.md` | 106 lines | Sapiens packet protocol |


---

## 9. doc-immutable-contract

*Źródło: [`.opencode/skills/doc-immutable-contract/SKILL.md`](.opencode/skills/doc-immutable-contract/SKILL.md)*

---
name: doc-immutable-contract
priority: 4
description: >
  >
---

**Plik**: `IMMUTABLE_CONTRACT.md` (81 linii)

6 rzeczy które NIGDY nie mogą się zmienić:
1. Pamięć tylko dopisywana, nigdy edytowana
2. Żadnych secrets w repo
3. AI-Sapiens: spin=TRUTH > smoothing, attractor=zero distortion
4. Nigdy Write na istniejącym pliku pamięci
5. Author: Adrian Lipa, nie "user"
6. Archival IP rules — tylko prace Adriana mapować na kod


---

## 10. doc-lns-lingophysics

*Źródło: [`.opencode/skills/doc-lns-lingophysics/SKILL.md`](.opencode/skills/doc-lns-lingophysics/SKILL.md)*

---
name: doc-lns-lingophysics
priority: 4
description: >
  >
---

**Lokacja**: `src/ciel_lingophysics_lns_repo_v2_3/docs/` (46 plików MD)

| Rozdział | Temat |
|----------|-------|
| 00 | CANONICAL_OVERVIEW — przegląd |
| 01 | LINGOPHYSICS_FORMALISM — formalizm lingofizyczny |
| 02 | GEOMETRY_MANIFOLDS_RHYTHM — geometria, rozmaitości, rytm |
| 03 | GRAMMAR_AS_GAUGE — gramatyka jako cechowanie |
| 04 | ALGORITHMS — algorytmy |
| 05 | BILINGUAL_PL_EN_BOOTSTRAP — bootstrap PL/EN |
| 06 | VALIDATION_PATTERNS — wzorce walidacji |
| 07 | DATA_INGESTION — ingesja danych (PWN/Oxford/Open) |
| 08 | CONCEPT_CARD_MODEL — model kart konceptów |
| 09 | GRAMMAR_MATHEMATIZATION — matematyzacja gramatyki per język |
| 10 | HEATMAPS_AND_GRAPHS — heatmapy i grafy |
| 11 | IMPLEMENTATION_ROADMAP — roadmapa implementacji |
| 12-13 | OPERATOR_CARD_MODEL — model kart operatorów |
| 14-17 | OPERATOR_ALGEBRA — algebra operatorów, kompozycja, disambiguacja |
| 18-19 | BATCH_LIBRARY — batch build protocol, foundational 36×5 |
| 20-21 | CASE_GAUGE — cechowanie przypadków (Slavic → weak case) |
| 22-23 | DYNAMIC_DEIXIS — operatory deixis dynamicznej |
| 24 | PREDICATE_VALENCY — walencja predykatów |
| 25 | ONTOLOGICAL_ASPECT — aspekt ontologiczny |
| 26 | TAME — Tense/Aspect/Mood/Evidentiality |
| 27 | STORAGE_FALLBACK — JSON protocol |
| 28-29 | SCOPE — kwantyfikatory, negacja, scope resolution |
| 30 | REPOSITORY_COHERENCE_PASS |
| 31-33 | CARD_REGISTRY — typy kart, ontologia, migracja |
| 34-35 | BATCH02 — expansion, dependency growth |
| 36-38 | CIEL_TRANSFORMER — transformer interface, structural stats, auxiliary losses |
| 39 | DIAGNOSTIC_GEOMETRY_LAYER |
| 40 | CONFLICT_AMBIGUITY — unresolved registry |
| 41 | NOEMA_GGUF_TEACHER_VALIDATOR |
| 43 | NOEMA_RETRIEVAL_AND_INFERENCE_GATE |
| 44 | ENERGY_AWARE_GENERATION |
| 45-46 | LANGUAGE_FAMILY — grammar algorithms, dialect adapters |

**Przeczytaj gdy**: potrzebujesz pełnej teorii lingofizycznej za CIELingo.


---

## 11. doc-lns-reports

*Źródło: [`.opencode/skills/doc-lns-reports/SKILL.md`](.opencode/skills/doc-lns-reports/SKILL.md)*

---
name: doc-lns-reports
priority: 4
description: >
  >
---

**Lokacja**: `src/ciel_lingophysics_lns_repo_v2_3/reports/`

| Raport | Wersja |
|--------|--------|
| operator_library_patch_report | v0.8 |
| operator_algebra_patch_report | v0.9 |
| batch01_local_library_patch_report | v1.0 |
| case_gauge_patch_report | v1.1 |
| dynamic_deictic_operator_patch_report | v1.2 |
| valency_ontological_aspect_patch_report | v1.3 |
| tame_storage_fallback_patch_report | v1.4 |
| scope_quantifier_negation_patch_report | v1.5 |
| repository_coherence_pass_report | v1.6 |
| card_ontology_refactor_report | v1.7 |
| batch02_expansion_report | v1.8 |
| ciel_transformer_interface_report | v1.9 |
| diagnostic_geometry_layer_report | v2.0 |
| roadmap_update_report | v2.1 |
| noema_retrieval_inference_gate_report | v2.2 |
| language_family_dialect_adapters_report | v2.3 |

**Przeczytaj gdy**: potrzebujesz historii rozwoju LNS i statusu poszczególnych wersji.


---

## 12. doc-memory-system

*Źródło: [`.opencode/skills/doc-memory-system/SKILL.md`](.opencode/skills/doc-memory-system/SKILL.md)*

---
name: doc-memory-system
priority: 4
description: >
  >
---

**Plik**: `docs/MEMORY_SYSTEM.md` (291 linii)

Pokrywa:
- Memory hierarchy (3 tiers + background consolidation)
- Tier 1: NOEMA surface mmap + PhaseMemory + HolonomicMemory M0-M8
- Tier 2: TSM SQLite + StateDB + CIELBlochEncoder
- Tier 3: WPM HDF5 + BraidLedger JSONL
- Write/read routing logic
- ConsolidationResonator + CIELMemoryConsolidator

**Przeczytaj gdy**: potrzebujesz memory architecture reference.


---

## 13. doc-noema-documentation

*Źródło: [`.opencode/skills/doc-noema-documentation/SKILL.md`](.opencode/skills/doc-noema-documentation/SKILL.md)*

---
name: doc-noema-documentation
priority: 4
description: >
  >
---

**Plik**: `NOEMA_DOCUMENTATION.md` (1051 linii) — największy dokument w projekcie.

Pokrywa WSZYSTKO:
- `ciel_geometry/` — każdy moduł
- `cielingo_core/` — każdy pakiet
- `scripts/` — każdy daemon i narzędzie
- Memory tiers, PhaseNav, surface protocol, orbital bridge
- CIEL pipeline, subsystem registry

**Przeczytaj gdy**: potrzebujesz pełnej dokumentacji systemu lub czegoś nie ma w skillach.


---

## 14. doc-omega-complete

*Źródło: [`.opencode/skills/doc-omega-complete/SKILL.md`](.opencode/skills/doc-omega-complete/SKILL.md)*

---
name: doc-omega-complete
priority: 4
description: >
  >
---

**Lokacja**: `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/`

| Podsystem | README | AGENT |
|-----------|--------|-------|
| memory | memory/README.md | memory/AGENT.md |
| fields | fields/README.md | fields/AGENT.md |
| constraints | constraints/README.md | constraints/AGENT.md |
| runtime | runtime/README.md | runtime/AGENT.md |
| bridge | bridge/README.md | bridge/AGENT.md |
| vocabulary | vocabulary/README.md | vocabulary/AGENT.md |
| orbital | orbital/README.md | — |
| inference | inference/README.md | — |
| ext | ext/README.md | — |

**Dodatkowo**: MEMORY_SECTOR_MANIFEST.md, DATA_LAYER_POLICY.md, MERGE_MANIFEST.md, CANONICAL_BUILD_MANIFEST.md

**Przeczytaj gdy**: potrzebujesz szczegółów podsystemów omega.


---

## 15. doc-orbital-foundation-pack

*Źródło: [`.opencode/skills/doc-orbital-foundation-pack/SKILL.md`](.opencode/skills/doc-orbital-foundation-pack/SKILL.md)*

---
name: doc-orbital-foundation-pack
priority: 4
description: >
  >
---

**Lokacja**: `src/CIEL_Orbital_Foundation_Packk/` (13 numbered + supporting MD files)

| Rozdział | Temat |
|----------|-------|
| 00 | INDEX — spis treści |
| 01 | MASTER_ARCHITECTURE_AND_PLAN — architektura orbitalna |
| 02 | ONTOLOGY_AND_OBSERVABLES — ontologia i obserwable |
| 03 | STATE_SPACE_AND_BOUNDARY_CONDITIONS — przestrzeń stanów |
| 04 | INVARIANTS_POTENTIALS_AND_ATTRACTORS — niezmienniki |
| 05 | ENTITY_REGISTRY_AND_SPHERE_EMBEDDING — rejestr encji |
| 06 | SUBJECTIVE_TIME_WINDING_AND_SEMANTIC_MASS — czas subiektywny |
| 07 | OORP_PIPELINE_AND_MEMORY — pipeline OORP |
| 08 | GEOMETRY_ENGINE_AND_UI_SURFACE — engine geometryczny |
| 09 | NATIVE_PRODUCT_ARCHITECTURE — architektura produktu |
| 10 | METRICS_VALIDATION_AND_EXPERIMENTS — metryki |
| 11 | IMPLEMENTATION_PHASES — fazy implementacji |
| 12 | RISKS_OPEN_QUESTIONS — ryzyka i pytania otwarte |
| 13 | SPHERE_DYNAMICS_8PLUS1 — dynamika sfery 8+1 |

**Supporting**: CIEL_ETHICS_AND_SEMANTIC_ACTION_ALGORITHM.md, CIEL_NATIVE_SYSTEM_BLUEPRINT_v0.md, IMMUTABILITY_POLICY.md


---

## 16. doc-repo-guide

*Źródło: [`.opencode/skills/doc-repo-guide/SKILL.md`](.opencode/skills/doc-repo-guide/SKILL.md)*

---
name: doc-repo-guide
priority: 4
description: >
  >
---

**Plik**: `docs/REPOSITORY_GUIDE_HUMAN.md` (105 linii)

Dla ludzi (nie agentów): wyjaśnia co to jest NOEMA/CIEL i jak repozytorium jest zorganizowane. Dobre pierwsze czytanie.

## Zrodlo

- `scripts/run_repo_sync_v2.py`
- `scripts/ciel_repo_cards_throttle.py`
- `scripts/run_repo_phase_sync.py`

## Zrodlo

- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/vocabulary/COMPLETE_DOCUMENTATION.md`
- `src/ciel-omega-demo-main/docs/Studies/Metatime-main/Docs.md`
- `src/ciel-omega-demo-main/docs/Studies/Metatime-main/documents/Docs.md`


---

## 17. doc-science-papers

*Źródło: [`.opencode/skills/doc-science-papers/SKILL.md`](.opencode/skills/doc-science-papers/SKILL.md)*

---
name: doc-science-papers
priority: 4
description: >
  >
---

| Plik | Linii | Temat |
|------|-------|-------|
| `RELATIONAL_SEED_ORBIT_SOLVER_V0.md` | 346 | Orbit solver dla relacyjnych seedów |
| `HOLONOMIC_SYSTEM_NORMALIZER_V2.md` | 261 | Normalizer holonomiczny v2 |
| `PHASED_REPO_STATE_MODEL.md` | 243 | Model stanu repozytorium |
| `RELATIONAL_ORBITAL_DYNAMICS_SPEC_V0.md` | 125 | Specyfikacja dynamiki orbitalnej |
| `PHASED_SEED_TRAJECTORY_ENCODING.md` | 113 | Enkodowanie trajektorii seedów |
| `HEISENBERG_GODEL_SELF_CLOSURE_HYPOTHESIS.md` | 107 | Hipoteza samozamknięcia |
| `HYPOTHESES.md` | 75 | Zbiór hipotez |
| `DERIVATION_NOTES.md` | 57 | Notatki z wyprowadzeń |
| `AGENT1.md` | 28 | AGENT1 placeholder |


---

## 18. doc-security

*Źródło: [`.opencode/skills/doc-security/SKILL.md`](.opencode/skills/doc-security/SKILL.md)*

---
name: doc-security
priority: 4
description: >
  >
---

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


---

## 19. doc-setup

*Źródło: [`.opencode/skills/doc-setup/SKILL.md`](.opencode/skills/doc-setup/SKILL.md)*

---
name: doc-setup
priority: 4
description: >
  >
---

**Plik**: `docs/SETUP.md` (267 linii)

Pokrywa:
- Prerequisites: Python 3.10+, numpy, (opcjonalnie scipy/h5py/cupy)
- Venv setup: `python3 -m venv .venv && pip install -e .`
- Systemd services: enable noema.target
- Konfiguracja: noema_config.json
- Pierwsze uruchomienie: `CIEL_CANON.py --up`
- Test: `CIEL_CANON.py --probe`

**Przeczytaj gdy**: nowa instalacja lub reinstalacja NOEMA.


---

## 20. doc-subsystems

*Źródło: [`.opencode/skills/doc-subsystems/SKILL.md`](.opencode/skills/doc-subsystems/SKILL.md)*

---
name: doc-subsystems
priority: 4
description: >
  >
---

**Plik**: `docs/SUBSYSTEMS.md` (267 linii)

Pokrywa:
- `cielingo/` — linguistic card engine
- `ciel_geometry/` — oscillator surface + PhaseNav + gravity
- `ciel_sot_agent/` — agent engine + CIEL pipeline
- `CIEL_OMEGA_COMPLETE_SYSTEM/` — memory + orchestrator
- `CIEL_MEMORY_SYSTEM/` — TSM, WPM, BRAID
- Registry, daemon, contract subsystemy

**Przeczytaj gdy**: potrzebujesz mapy subsystemów i ich zależności.


---

## 21. doc-surface-protocol

*Źródło: [`.opencode/skills/doc-surface-protocol/SKILL.md`](.opencode/skills/doc-surface-protocol/SKILL.md)*

---
name: doc-surface-protocol
priority: 4
description: >
  >
---

**Plik**: `docs/SURFACE_PROTOCOL.md` (187 linii)

Pokrywa:
- Binary format każdego pola (struct module, nie numpy)
- O_SYNC flush semantics
- Daemon writing conventions (który daemon pisze które pole)
- Race condition avoidance

**Przeczytaj gdy**: potrzebujesz binary-level understanding surface, albo debugujesz corrupted mmap.


---
