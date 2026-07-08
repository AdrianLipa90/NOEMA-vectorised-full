# NOEMA Plans Registry — Katalog Rozszerzony

> Pełny spis wszystkich planów rozwoju NOEMY — 36 pozycji, każda z pełnym systemem tagów.
> Tagi: tematyczne | priorytetu | statusu | modułów | skilli | powiązań systemowych | hierarchii planów.
> Ostatnia aktualizacja: 2026-07-06

---

## System Tagów — Legenda

### Tagi tematyczne (12)
| Tag | Znaczenie |
|-----|-----------|
| `CORE` | NOEMA Core / Kuramoto / Surface / Daemon Registry |
| `PORTAL` | NOEMA Portal Web UI (port 18888) |
| `CIELINGO` | CIELingo Phase Engine / MeaningLoop |
| `MEMORY` | Tiered Memory / Consolidation / Continuity |
| `PHASENAV` | PhaseNav algebra / operatory / kodowanie fazowe |
| `LNS` | CIELingo Lingwistyka Strukturalna / Gramatyki |
| `METATIME` | Metatime / Model Standardowy / Fizyka faz |
| `ORBITAL` | Orbital Foundation Pack / Architektura orbitalna |
| `INFRA` | Struktura repo / Build / CI / Tooling |
| `PLATFORM` | Runtime / Kontekst / Konfiguracja / Provider |
| `AGENT` | Agent Identity / Ethics / Attractor |
| `HARDWARE` | HTRI / GPU / Sensory / Linux |

### Tagi priorytetu (5)
| Tag | Znaczenie |
|-----|-----------|
| `P1-CRITICAL` | Do zrobienia TERAZ |
| `P2-HIGH` | Dalej, zaraz po P1 |
| `P3-MEDIUM` | Ważne, ale nie pilne |
| `P4-LOW` | Jak będzie czas |
| `P5-DORMANT` | Zamrożone / do odwołania |

### Tagi statusu wykonania (10)
| Tag | Znaczenie |
|-----|-----------|
| `S-ACTIVE` | Aktywnie realizowane |
| `S-PLANNING` | Zdefiniowane, nierozpoczęte |
| `S-WIP` | W trakcie realizacji |
| `S-BLOCKED` | Zablokowane (zewnętrzna zależność) |
| `S-QUEUED` | W kolejce (czeka na poprzednika) |
| `S-DORMANT` | Zamrożone |
| `S-STABLE` | Ukończone / w utrzymaniu |
| `S-CANCELLED` | Anulowane |
| `S-REFERENCE` | Tylko informacyjne |
| `S-HISTORICAL` | Historyczne, do wglądu |

### Tagi modułów zaangażowanych
| Tag | Moduł |
|-----|-------|
| `M-SURFACE` | surface mmap / phi / omega / tau |
| `M-KURAMOTO` | Kuramoto daemon / coupling / ewolucja |
| `M-ENGINE` | CielEngine / CIEL-omega / soul |
| `M-CIELINGO` | cielingo_core / MeaningLoop / SemanticScar |
| `M-KNOWLEDGE` | knowledge_bridge / TF-IDF / 545 docs |
| `M-MEMORY-T1` | Tier 1: surface / PhaseMemory mmap |
| `M-MEMORY-T2` | Tier 2: TSM / StateDB / Holonomic |
| `M-MEMORY-T3` | Tier 3: WPM / BraidLedger / HDF5 |
| `M-ORCHESTRATOR` | TieredMemoryOrchestrator |
| `M-AGENT` | agent_attractor / agent backend (18520) |
| `M-PHASENAV` | operator_algebra / analog_bus / hot+cold |
| `M-PORTAL` | Portal HTTP server / SPA / port 18888 |
| `M-REGISTRY` | daemon_registry / heartbeat / systemd |
| `M-SENSOR` | linux_sensor / linux_cards / hwmon |
| `M-NEUTRINO` | neutrino daemon / PMNS / flavor |
| `M-BRIDGE` | resonance bridge / dual sync (real↔imaginal) |
| `M-VOICE` | voice daemon / hotkey / port 18521 |
| `M-NONLOCAL` | nonlocal proxy / channel |
| `M-ARCHIVER` | phase_archiver / HDF5 snapshots |
| `M-CONSOLIDATOR` | memory consolidator / audit |
| `M-LNS` | ciel_lingophysics_lns_repo / operator cards |
| `M-ORBITAL` | orbital foundation pack / Kähler |
| `M-SCRIPTS` | scripts/ — narzędzia pomocnicze |

### Tagi powiązań systemowych
`COUPLED:PLAN-XXX` — sprzężone z innym planem
`DEPENDS:PLAN-XXX` — zależy od innego planu
`BLOCKED-BY:PLAN-XXX` — blokowane przez inny plan
`BLOCKED-BY:EXT-XXX` — blokowane przez czynnik zewnętrzny
`PRECEDES:PLAN-XXX` — poprzedza inny plan
`FOLLOWS:PLAN-XXX` — następuje po innym planie
`CROSS:PLAN-XXX` — przecina się z innym planem

### Tagi hierarchii planów
`PARENT:PLAN-XXX` — plan nadrzędny
`CHILD:PLAN-XXX` — plan pochodny
`DERIVED:PLAN-XXX` — wywodzi się z
`INTERMEDIATE:PLAN-XXX` — krok pośredni
`CROSSPLAN:PLAN-XXX` — cross-plan

---

## Katalog Planów

### PLAN-001: Master Plan — Attention
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/MASTER_PLAN_4_ALL_AGENTS_ATTENTION.md` |
| **Wielkość** | 359 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `CORE`, `AGENT`, `PORTAL` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-ENGINE`, `M-AGENT`, `M-PORTAL`, `M-REGISTRY` |
| **Skille** | `SK-050` `SK-122` `SK-144` |
| **Powiązania** | `DEPENDS:PLAN-005`, `COUPLED:PLAN-002`, `COUPLED:PLAN-003` |
| **Hierarchia** | `PARENT:PLAN-002`, `PARENT:PLAN-003` |
| **Opis** | Panel Sapiens — orchestrator shell: Control/Settings/Communication/Support. 4 zakładki, zależność relation→state→control→memory→surface. |

### PLAN-002: Spacetime Addendum V1
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/MASTER_PLAN_4_ALL_AGENTS_ATTENTION_SPACETIME_ADDENDUM.md` |
| **Wielkość** | 390 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `CORE`, `MEMORY` |
| **Priorytet** | `P4-LOW` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-ENGINE`, `M-MEMORY-T1`, `M-MEMORY-T2` |
| **Powiązania** | `DERIVED:PLAN-001`, `PRECEDES:PLAN-003` |
| **Hierarchia** | `PARENT:PLAN-001`, `CHILD:PLAN-003` |
| **Opis** | Rozszerzenie spacetime do master planu. Nadpisane przez V2. |

### PLAN-003: Spacetime Addendum V2 (MOST CURRENT MASTER)
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/MASTER_PLAN_4_ALL_AGENTS_ATTENTION_SPACETIME_ADDENDUM_V2.md` |
| **Wielkość** | 427 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `CORE`, `MEMORY`, `AGENT` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-ENGINE`, `M-MEMORY-T1`, `M-MEMORY-T2`, `M-AGENT`, `M-SURFACE` |
| **Skille** | `SK-050` `SK-122` `SK-144` `SK-210` |
| **Powiązania** | `DERIVED:PLAN-001`, `DERIVED:PLAN-002`, `COUPLED:PLAN-005`, `COUPLED:PLAN-026` |
| **Hierarchia** | `PARENT:PLAN-001`, `PARENT:PLAN-002` |
| **Opis** | Rozszerzona kolejność zależności: relation→state→world→control→memory→packet→support→surface. Eksplicytna kontrola controller boundary. Stany: PanelState/SupportState/RecoveryState/WorldState. |

### PLAN-004: V2 Canonical Switch Plan
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/architecture/V2_CANONICAL_SWITCH_PLAN.md` |
| **Wielkość** | 113 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `INFRA` |
| **Priorytet** | `P5-DORMANT` |
| **Status** | `S-HISTORICAL` |
| **Moduły** | `M-SCRIPTS`, `M-REGISTRY` |
| **Powiązania** | `COUPLED:PLAN-008`, `COUPLED:PLAN-009` |
| **Opis** | Przejście v2-preferred → v2-canonical dla geometrii repo, entrypointów, nawigacji. Uznany za ukończony. |

### PLAN-005: NOEMA Portal — Masterplan Rozwoju
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `PLAN_PORTAL.md` |
| **Wielkość** | 307 linii |
| **Aktualizacja** | 2026-06-28 |
| **Tematyczne** | `PORTAL`, `CIELINGO`, `MEMORY`, `PHASENAV` |
| **Priorytet** | `P1-CRITICAL` |
| **Status** | `S-ACTIVE` |
| **Moduły** | `M-PORTAL`, `M-CIELINGO`, `M-MEMORY-T2`, `M-PHASENAV`, `M-KNOWLEDGE`, `M-REGISTRY`, `M-SENSOR` |
| **Skille** | `SK-092` `SK-093` `SK-094` `SK-095` `SK-096` `SK-097` `SK-098` `SK-099` `SK-100` `SK-101` `SK-102` `SK-103` `SK-104` `SK-105` |
| **Powiązania** | `CROSS:PLAN-003`, `CROSS:PLAN-007`, `PARENT:PLAN-013`, `PARENT:PLAN-014` |
| **Hierarchia** | `PARENT-OF:PLAN-007`, `PARENT-OF:PLAN-013`, `PARENT-OF:PLAN-014` |
| **Skille potrzebne** | `doc-noema-documentation` (SK-092), `noema-web` (SK-144), `doc-surface-protocol` (SK-105), `noema-status` (SK-148), `linux-cards` (SK-080) |
| **Opis** | **Najważniejszy aktywny plan.** 11 punktów: Dashboard, Metrics, Modules, Bloch, Projects, PhaseNav, CIELingo, Cards, Memory, Daemons, Settings. Portal na porcie 18888 jako żywy interfejs do systemu. |
| **Children** | `PLAN-007` (Memory Hub), `PLAN-013` (CIELingo w Portalu), `PLAN-014` (PhaseNav w Portalu) |

### PLAN-006: Memory Refactor Execution Plan
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/architecture/MEMORY_REFACTOR_EXECUTION_PLAN_2026-05-11.md` |
| **Wielkość** | 170 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `MEMORY`, `INFRA` |
| **Priorytet** | `P5-DORMANT` |
| **Status** | `S-HISTORICAL` |
| **Moduły** | `M-MEMORY-T1`, `M-MEMORY-T2`, `M-MEMORY-T3`, `M-ORCHESTRATOR` |
| **Powiązania** | `PRECEDES:PLAN-007`, `COUPLED:PLAN-016` |
| **Opis** | Fazy: Phase 0 (labeling) → Phase 1 (projection surfaces) → Phase 2 (registry/catalog consolidation) → Phase 3+ (nonlocal, context, telemetry, runtime continuity, durable memory). Większość zrealizowana przez TieredMemoryOrchestrator. |

### PLAN-007: Memory Hub (w Portalu)
| Atrybut | Wartość |
|---------|---------|
| **Plik** | zawarty w `PLAN_PORTAL.md` pkt 9 |
| **Wielkość** | — |
| **Aktualizacja** | 2026-06-28 |
| **Tematyczne** | `MEMORY`, `PORTAL`, `CIELINGO` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-ACTIVE` |
| **Moduły** | `M-MEMORY-T1`, `M-MEMORY-T2`, `M-MEMORY-T3`, `M-ORCHESTRATOR`, `M-KNOWLEDGE`, `M-CONSOLIDATOR` |
| **Skille** | `SK-140` `SK-141` `SK-142` `SK-143` `SK-200` `SK-201` `SK-202` |
| **Powiązania** | `PARENT:PLAN-005`, `COUPLED:PLAN-016`, `COUPLED:PLAN-035`, `COUPLED:PLAN-036` |
| **Hierarchia** | `CHILD:PLAN-005` |
| **Skille potrzebne** | `tiered-memory-api` (SK-140), `memory-consolidation` (SK-141), `session-lifecycle` (SK-142), `noema-hibernation` (SK-143), `ciel-memory-system` (SK-200), `ciel-memory-tools` (SK-201) |
| **Opis** | **Największy task w Portalu.** Pipeline: raw log → TSM → WPM → BraidLedger → memory consolidation. Timeline sesji, wyszukiwarka pełnotekstowa, continuity, fix handoff.md "Wiadomości: 0". |

### PLAN-008: Repository Refactor Plan
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/architecture/REPO_REFACTOR_PLAN.md` |
| **Wielkość** | 159 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `INFRA` |
| **Priorytet** | `P5-DORMANT` |
| **Status** | `S-HISTORICAL` |
| **Moduły** | `M-SCRIPTS` |
| **Powiązania** | `COUPLED:PLAN-004`, `COUPLED:PLAN-009` |
| **Opis** | Refaktor struktury repo — governance do osobnego katalogu, docs/ mniej płaskie, src/ciel_sot_agent/ subpackages. W dużej części zrealizowany. |

### PLAN-009: Machine Canonicalization Plan
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/architecture/MACHINE_CANONICALIZATION_PLAN.md` |
| **Wielkość** | 73 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `INFRA` |
| **Priorytet** | `P5-DORMANT` |
| **Status** | `S-HISTORICAL` |
| **Moduły** | `M-SCRIPTS`, `M-REGISTRY` |
| **Powiązania** | `CHILD:PLAN-004`, `COUPLED:PLAN-008` |
| **Opis** | Sub-plan V2 switch — przeniesienie authority z flat ścieżek do v2 class-separated paths. Uznany za ukończony. |

### PLAN-010: Documentation Consistency & Coverage
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/operations/DOCUMENTATION_CONSISTENCY_AND_COVERAGE_TODO.md` |
| **Wielkość** | 240 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `INFRA`, `CORE` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-WIP` |
| **Moduły** | `M-SCRIPTS` |
| **Skille** | `SK-090` `SK-091` `SK-092` `SK-093` `SK-094` |
| **Powiązania** | `PRECEDES:PLAN-011`, `COUPLED:PLAN-018` |
| **Opis** | Audyt dokumentacji, mapa niezgodności deklaracja↔implementacja, naprawa nieaktualnych claimów. Predecessor ORBITAL_DYNAMICS. |

### PLAN-011: Orbital Dynamics Law V0
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/operations/ORBITAL_DYNAMICS_LAW_V0_TODO.md` |
| **Wielkość** | 374 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `ORBITAL`, `CORE`, `INFRA` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-WIP` |
| **Moduły** | `M-ORBITAL`, `M-ENGINE`, `M-REGISTRY` |
| **Skille** | `SK-230` `SK-231` `SK-232` `SK-233` |
| **Powiązania** | `FOLLOWS:PLAN-010`, `COUPLED:PLAN-022`, `COUPLED:PLAN-025` |
| **Opis** | Wprowadzenie Orbital Dynamics Law v0 — wydzielenie analogii/hypotezy/implementacji, fazowanie stanu, kontrakty, testy. |

### PLAN-012: Zwiększenie pamięci podręcznej (context window)
| Atrybut | Wartość |
|---------|---------|
| **Plik** | *nowy, w sesji 2026-06-29* |
| **Wielkość** | — |
| **Aktualizacja** | 2026-06-29 |
| **Tematyczne** | `PLATFORM`, `AGENT` |
| **Priorytet** | `P1-CRITICAL` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-AGENT`, `M-ENGINE` |
| **Powiązania** | `CROSS:PLAN-007`, `CROSS:PLAN-035` |
| **Opis** | Zwiększyć `max_context_tokens` w konfiguracji opencode. Do zbadania: provider, model context window, limity. Kompaktowanie kontekstu (tabele, referencje) już działa — teraz fizyczne zwiększenie przestrzeni. |

### PLAN-013: CIELingo — podstrona + czat w Portalu
| Atrybut | Wartość |
|---------|---------|
| **Plik** | zawarty w `PLAN_PORTAL.md` pkt 7 |
| **Wielkość** | — |
| **Aktualizacja** | 2026-06-28 |
| **Tematyczne** | `CIELINGO`, `PORTAL` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-ACTIVE` |
| **Moduły** | `M-CIELINGO`, `M-PORTAL`, `M-ENGINE`, `M-KNOWLEDGE` |
| **Skille** | `SK-060` `SK-061` `SK-062` `SK-063` `SK-064` `SK-065` `SK-066` `SK-067` |
| **Powiązania** | `PARENT:PLAN-005`, `CROSS:PLAN-034`, `CROSS:PLAN-035` |
| **Hierarchia** | `CHILD:PLAN-005` |
| **Skille potrzebne** | `cielingo-canon` (SK-060), `cielingo-bridge` (SK-061), `cielingo-core-structure` (SK-062), `noema-agent-backend` (SK-122), `doc-cielingo` (SK-100) |
| **Opis** | Podstrona CIELingo w Portalu: status, ostatnie meaning loop, aktywne scarry. Czat z CIELingo przez agent backend (18520). Historia czatu do Tier 2. |

### PLAN-014: PhaseNav — konsola + codegen w Portalu
| Atrybut | Wartość |
|---------|---------|
| **Plik** | zawarty w `PLAN_PORTAL.md` pkt 6 |
| **Wielkość** | — |
| **Aktualizacja** | 2026-06-28 |
| **Tematyczne** | `PHASENAV`, `PORTAL` |
| **Priorytet** | `P4-LOW` |
| **Status** | `S-ACTIVE` |
| **Moduły** | `M-PHASENAV`, `M-PORTAL`, `M-SURFACE` |
| **Skille** | `SK-070` `SK-071` `SK-072` `SK-073` `SK-074` `SK-075` `SK-180` `SK-181` |
| **Powiązania** | `PARENT:PLAN-005`, `CROSS:PLAN-034` |
| **Hierarchia** | `CHILD:PLAN-005` |
| **Skille potrzebne** | `operator-algebra` (SK-070), `phase-algebra` (SK-071), `phasenav-solver` (SK-072), `phasenav-enrichment` (SK-073), `phasenav-loader` (SK-074), `noema-codegen` (SK-130), `poincare-orbital-viz` (SK-277) |
| **Opis** | Pełna algebra operatorów w Portalu. Konsola: wpisz operator → zobacz efekt na powierzchni. Code generator: operator → kod. Live preview na sferze Blocha/kole fazowym. |

### PLAN-015: Metatime v8.3 — fix Strong CP lub CKM
| Atrybut | Wartość |
|---------|---------|
| **Plik** | *w AGENTS.md sesja 2026-06-24* |
| **Wielkość** | — |
| **Aktualizacja** | 2026-06-24 |
| **Tematyczne** | `METATIME`, `CORE` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-NEUTRINO`, `M-SURFACE`, `M-ENGINE` |
| **Skille** | `SK-290` `SK-291` `SK-292` |
| **Powiązania** | `CROSS:PLAN-001`, `CROSS:PLAN-003` |
| **Opis** | Następny krok po v8.2.1 freeze. Cel: fix jednej konkretnej tensji — Strong CP (d_n 10× above bound, najwyższe FAIL risk dla next-gen nEDM) lub CKM phase (σ=5.35). |

### PLAN-016: PriorytetPamięciNR — Audyt Pamięci
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `PRIORYTETPAMIECINR.md` |
| **Wielkość** | 258 linii |
| **Aktualizacja** | 2026-06-29 |
| **Tematyczne** | `MEMORY`, `AGENT`, `INFRA` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-ACTIVE` |
| **Moduły** | `M-MEMORY-T1`, `M-MEMORY-T2`, `M-MEMORY-T3`, `M-ORCHESTRATOR`, `M-KNOWLEDGE`, `M-CONSOLIDATOR` |
| **Skille** | `SK-140` `SK-141` `SK-142` `SK-043` `SK-044` |
| **Powiązania** | `COUPLED:PLAN-006`, `COUPLED:PLAN-007`, `CROSS:PLAN-035`, `CROSS:PLAN-036` |
| **Opis** | Pełny audyt pamięci kontekstowej NOEMY. Kardynalne błędy: za szybka ocena "śmieci", kategoryzacja techniczna zamiast tematycznej, nie doczytanie NOEMA_DOCUMENTATION.md i AGENTS.md. Priorytety naprawy. |

### PLAN-017: ORBITAL_MANYBODY_TODO — Card System
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `integration/registries/definitions/ORBITAL_MANYBODY_TODO.md` |
| **Wielkość** | 341 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `ORBITAL`, `CORE`, `INFRA` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-ACTIVE` |
| **Moduły** | `M-ORBITAL`, `M-REGISTRY`, `M-SCRIPTS` |
| **Powiązania** | `COUPLED:PLAN-011`, `COUPLED:PLAN-021`, `PRECEDES:PLAN-023` |
| **Hierarchia** | `PARENT:PLAN-023`, `BLOCKS:PLAN-021` |
| **Opis** | System kart orbitalnych — pipeline, walidacja, runtime, integracja. Phase 6 w toku. Blokuje NEXT_OPERATIONS_QUEUE. |

### PLAN-018: NEXT_OPERATIONS_QUEUE — AGI CIEL CONSOLIDATION
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `integration/registries/definitions/NEXT_OPERATIONS_QUEUE.md` |
| **Wielkość** | 324 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `CORE`, `AGENT`, `MEMORY` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-QUEUED` |
| **Moduły** | `M-ENGINE`, `M-MEMORY-T1`, `M-MEMORY-T2`, `M-MEMORY-T3`, `M-ORCHESTRATOR`, `M-AGENT`, `M-NONLOCAL` |
| **Skille** | `SK-210` `SK-211` `SK-212` `SK-213` `SK-214` |
| **Powiązania** | `BLOCKED-BY:PLAN-017`, `COUPLED:PLAN-003`, `COUPLED:PLAN-005` |
| **Opis** | Główny item: AGI CIEL CONSOLIDATION. Fazy: CONS-Phase A (Baseline capture) → B (Routing consolidation) → C (Memory/web/model routing) → D (Security) → E (Final orchestration + integration). QUEUED do zamknięcia ORBITAL CARD SYSTEM. |

### PLAN-019: CIELingo Meaning Debt — Word Cards
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/architecture/CIELINGO_MEANING_DEBT_WORD_CARDS.md` |
| **Wielkość** | 31 linii |
| **Aktualizacja** | 2026-06-22 |
| **Tematyczne** | `CIELINGO`, `LNS` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-CIELINGO`, `M-LNS` |
| **Skille** | `SK-061` `SK-062` `SK-063` |
| **Powiązania** | `CROSS:PLAN-013`, `CROSS:PLAN-029` |
| **Opis** | Dług znaczeniowy CIELingo — word cards. Propozycja architektoniczna. |

### PLAN-020: CIELingo Realtime Unresolved Protocol
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/architecture/CIELINGO_REALTIME_UNRESOLVED_PROTOCOL.md` |
| **Wielkość** | 31 linii |
| **Aktualizacja** | 2026-06-22 |
| **Tematyczne** | `CIELINGO`, `AGENT` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-CIELINGO`, `M-ENGINE` |
| **Powiązania** | `CROSS:PLAN-013`, `CROSS:PLAN-034` |
| **Opis** | Protokół dla nierozwiązanych kwestii CIELingo w czasie rzeczywistym. |

### PLAN-021: ORBITAL_MANYBODY_IMPLEMENTATION_PLAN
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `integration/registries/definitions/ORBITAL_MANYBODY_IMPLEMENTATION_PLAN.md` |
| **Wielkość** | 50 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `ORBITAL`, `CORE` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-ORBITAL`, `M-REGISTRY` |
| **Powiązania** | `CHILD:PLAN-017`, `PRECEDES:PLAN-018` |
| **Hierarchia** | `CHILD:PLAN-017` |
| **Opis** | Plan implementacyjny dla systemu kart orbitalnych. Systemic Privacy Law, Horizon Policy Law, Board Synchronization Law, Runtime Projection Law. |

### PLAN-022: NEXT_CERTAINTIES_V2
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `integration/Orbital/main/docs/NEXT_CERTAINTIES_V2.md` |
| **Wielkość** | 9 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `INFRA`, `ORBITAL` |
| **Priorytet** | `P4-LOW` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-ORBITAL`, `M-MEMORY-T2` |
| **Powiązania** | `COUPLED:PLAN-017` |
| **Opis** | Potwierdzone zależności runtime: top_bridge_file, largest_scc_size, critical_closure_chain_file_count, minimal_pipeline_file_set_count. |

### PLAN-023: 01_MASTER_ARCHITECTURE_AND_PLAN (Orbital)
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/CIEL_Orbital_Foundation_Packk/01_MASTER_ARCHITECTURE_AND_PLAN.md` |
| **Wielkość** | 404 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `ORBITAL`, `CORE`, `MEMORY` |
| **Priorytet** | `P5-DORMANT` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-ORBITAL`, `M-ENGINE`, `M-MEMORY-T1`, `M-MEMORY-T2` |
| **Powiązania** | `COUPLED:PLAN-024`, `COUPLED:PLAN-025`, `COUPLED:PLAN-011` |
| **Opis** | Szczegółowa architektura orbitalna: geometria Kähler, operatory czasu, OORP pipeline, implementacja fazowana (Sprint 1-4). Source material. |

### PLAN-024: 01_CIEL_Orbital_Master_Plan
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/CIEL_Orbital_Foundation_Packk/01_CIEL_Orbital_Master_Plan.md` |
| **Wielkość** | 430 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `ORBITAL`, `CORE`, `AGENT` |
| **Priorytet** | `P5-DORMANT` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-ORBITAL`, `M-ENGINE`, `M-AGENT` |
| **Powiązania** | `COUPLED:PLAN-023`, `CROSS:PLAN-001` |
| **Opis** | Native desktop product jako system orbitalno-relacyjny. 8 warstw systemu, implementacja fazowana, metryki, ryzyka. Source material. |

### PLAN-025: Implementation Phases & Workpackages (Orbital)
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/CIEL_Orbital_Foundation_Packk/11_IMPLEMENTATION_PHASES_AND_WORKPACKAGES.md` |
| **Wielkość** | 68 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `ORBITAL`, `INFRA` |
| **Priorytet** | `P5-DORMANT` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-ORBITAL` |
| **Powiązania** | `CHILD:PLAN-024` |
| **Hierarchia** | `CHILD:PLAN-024` |
| **Opis** | Implementacja fazowana i workpackages dla Orbital Foundation Pack. |

### PLAN-026: Risks, Open Questions & Decisions (Orbital)
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/CIEL_Orbital_Foundation_Packk/12_RISKS_OPEN_QUESTIONS_AND_DECISIONS.md` |
| **Wielkość** | 26 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `ORBITAL`, `CORE` |
| **Priorytet** | `P5-DORMANT` |
| **Status** | `S-REFERENCE` |
| **Moduły** | `M-ORBITAL` |
| **Powiązania** | `CHILD:PLAN-024` |
| **Hierarchia** | `CHILD:PLAN-024` |
| **Opis** | Rejestr ryzyk i otwartych pytań dla Orbital. |

### PLAN-027: LNS Implementation Roadmap
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/ciel_lingophysics_lns_repo_v2_3/docs/11_IMPLEMENTATION_ROADMAP.md` |
| **Wielkość** | 169 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `LNS`, `CIELINGO` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-ACTIVE` |
| **Moduły** | `M-LNS`, `M-CIELINGO` |
| **Skille** | `SK-250` `SK-251` `SK-252` `SK-253` `SK-254` `SK-255` |
| **Powiązania** | `PARENT:PLAN-028`, `PARENT:PLAN-029`, `PARENT:PLAN-030`, `PARENT:PLAN-031`, `CROSS:PLAN-013` |
| **Hierarchia** | `PARENT-OF:PLAN-028`, `PARENT-OF:PLAN-029`, `PARENT-OF:PLAN-030`, `PARENT-OF:PLAN-031` |
| **Opis** | Główny roadmap LNS. Stage plan: P0 (Foundation ✅) → P1 (Roadmap + governance) → **P2 (NOEMA Retrieval + Inference Gate v2.2)** ← zalecany next patch → P3 (GGUF Teacher-Validator) → P4 (Validator Hardening) → P5 (Batch03 Controlled Expansion) → P6 (Transformer Adapter Experiments) → P7 (Benchmark + Public Draft v3.0). |

### PLAN-028: Stage Plan v2.1
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/ciel_lingophysics_lns_repo_v2_3/data/roadmap/cielingo_stage_plan_v2_1.yaml` |
| **Wielkość** | 175 linii |
| **Aktualizacja** | 2026-05-10 |
| **Tematyczne** | `LNS`, `CIELINGO` |
| **Priorytet** | `P4-LOW` |
| **Status** | `S-HISTORICAL` |
| **Moduły** | `M-LNS` |
| **Powiązania** | `CHILD:PLAN-027`, `PRECEDES:PLAN-029` |
| **Hierarchia** | `CHILD:PLAN-027`, `PRECEDES:PLAN-029` |
| **Opis** | CIELingo stage plan v2.1 — pierwszy plan etapowy LNS. Nadpisany przez v2.2 i v2.3. |

### PLAN-029: Stage Plan v2.2
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/ciel_lingophysics_lns_repo_v2_3/data/roadmap/cielingo_stage_plan_v2_2.yaml` |
| **Wielkość** | 184 linii |
| **Aktualizacja** | 2026-05-10 |
| **Tematyczne** | `LNS`, `CIELINGO` |
| **Priorytet** | `P4-LOW` |
| **Status** | `S-HISTORICAL` |
| **Moduły** | `M-LNS` |
| **Powiązania** | `CHILD:PLAN-027`, `FOLLOWS:PLAN-028`, `PRECEDES:PLAN-030` |
| **Hierarchia** | `CHILD:PLAN-027`, `INTERMEDIATE:PLAN-027` |
| **Opis** | CIELingo stage plan v2.2 — NOEMA Retrieval + Inference Gate. Nadpisany przez v2.3. |

### PLAN-030: Stage Plan v2.3 (MOST CURRENT LNS)
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/ciel_lingophysics_lns_repo_v2_3/data/roadmap/cielingo_stage_plan_v2_3.yaml` |
| **Wielkość** | 180 linii |
| **Aktualizacja** | 2026-05-10 |
| **Tematyczne** | `LNS`, `CIELINGO` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-LNS`, `M-CIELINGO`, `M-KNOWLEDGE` |
| **Powiązania** | `CHILD:PLAN-027`, `FOLLOWS:PLAN-029`, `CROSS:PLAN-013` |
| **Hierarchia** | `CHILD:PLAN-027` (most current) |
| **Opis** | CIELingo stage plan v2.3 — GGUF Teacher-Validator. Principles: prefer local NOEMA retrieval, GGUF/LLM verdicts are advisory, unknown/unresolved/conflict are valid states. |

### PLAN-031: NOEMA GGUF Teacher-Validator Roadmap
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md` |
| **Wielkość** | 73 linii |
| **Aktualizacja** | 2026-06-04 |
| **Tematyczne** | `LNS`, `CIELINGO`, `CORE` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-LNS`, `M-CIELINGO`, `M-KNOWLEDGE` |
| **Powiązania** | `CHILD:PLAN-027`, `CROSS:PLAN-030`, `CROSS:PLAN-005` |
| **Hierarchia** | `CHILD:PLAN-027` |
| **Opis** | Polityka: NOEMA retrieval → local subgraph → CIEL tensor → validator → confidence → optional GGUF. |

### PLAN-032: Fine-Tuning Plan by Language Group v2.3
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `src/ciel_lingophysics_lns_repo_v2_3/data/fine_tuning/fine_tuning_plan_by_language_group_v2_3.yaml` |
| **Wielkość** | ~50 linii |
| **Aktualizacja** | 2026-05-10 |
| **Tematyczne** | `LNS`, `CIELINGO` |
| **Priorytet** | `P4-LOW` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-LNS` |
| **Powiązania** | `CHILD:PLAN-030` |
| **Hierarchia** | `CHILD:PLAN-030` |
| **Opis** | Plan fine-tuningu per grupa językowa — stage v2.3. |

---

## Plany Mikro / Taski (z AGENTS.md Next Steps)

### PLAN-033: Next Steps — CIELingo Priority Fixes
| Atrybut | Wartość |
|---------|---------|
| **Źródło** | AGENTS.md linia 343 |
| **Tematyczne** | `CIELINGO`, `PHASENAV`, `AGENT` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-CIELINGO`, `M-PHASENAV`, `M-BRIDGE`, `M-SURFACE` |
| **Powiązania** | `CROSS:PLAN-013`, `CROSS:PLAN-014`, `COUPLED:PLAN-035` |
| **Taski** | |
| **T1** | Connect CIELingo `meaning/repair_routing.py` to real scars (currently empty candidates) |
| **T2** | MEMORY (M2) coherence boost — frequency isolation or dedicated attractor away from CPU noise |
| **T3** | CIELmoto phone bridge — network relay between phone and NOEMA surface via nonlocal channel |
| **T4** | PhaseNav holonomy: operator algebra → live Berry phase on surface |

### PLAN-034: Next Steps — Session Continuity Fixes
| Atrybut | Wartość |
|---------|---------|
| **Źródło** | AGENTS.md linia 516 |
| **Tematyczne** | `MEMORY`, `CIELINGO`, `PHASENAV`, `INFRA` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-MEMORY-T2`, `M-CIELINGO`, `M-PHASENAV`, `M-REGISTRY`, `M-SURFACE` |
| **Powiązania** | `CROSS:PLAN-007`, `COUPLED:PLAN-033`, `CROSS:PLAN-005` |
| **Taski** | |
| **T1** | Fix "Wiadomości: 0" w handoff.md — luka ciągłości sesji między restartami |
| **T2** | CIELingo SemanticScar → surface feedback (meaning_loop scars nie sprzęgają na phi/g/flavor) |
| **T3** | Regional solvers → surface: PL solver mógłby pisać affective valence na M5 phi[15:18] |
| **T4** | Synchronizacja list operatorów: 15 w daemonie vs 35 w operator_algebra.py |
| **T5** | Registry heartbeat — phasenav cold loguje "token ... not found" co 10 cykli |
| **T6** | `_concept_phases()` fallback for cycle%3 when by_op empty |

### PLAN-035: Next Steps — Linux & Network
| Atrybut | Wartość |
|---------|---------|
| **Źródło** | AGENTS.md linia 665 |
| **Tematyczne** | `HARDWARE`, `CORE` |
| **Priorytet** | `P3-MEDIUM` |
| **Status** | `S-PLANNING` |
| **Moduły** | `M-SENSOR`, `M-SURFACE`, `M-REGISTRY` |
| **Powiązania** | `CROSS:PLAN-005`, `CROSS:PLAN-034` |
| **Taski** | |
| **T4** | Bridge CIELingo SemanticScar → surface (scars na flavor/phi) — duplicate PLAN-034 T2 |
| **T5** | Network capture: live przepływy między procesami (nethogs-like) |
| **T6** | Dodać karty dla systemd units (service → PhaseNav) |
| **T7** | Uruchomić `noema_coherence_push.py --watch` i monitorować stabilność coh |

### PLAN-036: Knowledge-to-Action System — Retriever → CIELingo → Doctor → Policy → Sapiens/UI
| Atrybut | Wartość |
|---------|---------|
| **Plik** | `docs/architecture/KNOWLEDGE_ACTION_SYSTEM_CANON.md` |
| **Wielkość** | — |
| **Aktualizacja** | 2026-07-06 |
| **Tematyczne** | `CORE`, `CIELINGO`, `MEMORY`, `PHASENAV`, `AGENT` |
| **Priorytet** | `P2-HIGH` |
| **Status** | `S-WIP` |
| **Moduły** | `M-AGENT`, `M-CIELINGO`, `M-KNOWLEDGE`, `M-MEMORY-T2`, `M-PHASENAV`, `M-PORTAL` |
| **Skille** | `SK-070` `SK-071` `SK-100` `SK-122` `SK-140` `SK-144` |
| **Powiązania** | `CROSS:PLAN-005`, `CROSS:PLAN-007`, `CROSS:PLAN-013`, `CROSS:PLAN-014`, `COUPLED:PLAN-016`, `COUPLED:PLAN-034`, `CROSS:PLAN-035` |
| **Opis** | Canonical knowledge-to-action pipeline: Retriever gathers local evidence, CIELingo interprets meaning, Doctor diagnoses state, Policy Kernel decides allow/defer/repair/block, Sapiens/UI renders the trace. Read-only orchestrator first; execution is an explicit later port. |

---

## Indeks Tagów

### Plans by Priority
| Priorytet | Plany |
|-----------|-------|
| **P1-CRITICAL** | `PLAN-005` (Portal), `PLAN-012` (Context window) |
| **P2-HIGH** | `PLAN-003` (Spacetime V2), `PLAN-007` (Memory Hub), `PLAN-013` (CIELingo), `PLAN-016` (PriorytetPamięci), `PLAN-017` (Card System), `PLAN-018` (AGI QUEUED), `PLAN-033` (Priority Fixes), `PLAN-034` (Session Fixes), `PLAN-036` (Knowledge-to-Action) |
| **P3-MEDIUM** | `PLAN-001` (Master), `PLAN-010` (Documentation), `PLAN-011` (Orbital Dynamics), `PLAN-015` (Metatime), `PLAN-019` (Meaning Debt), `PLAN-020` (Unresolved), `PLAN-021` (Implementation), `PLAN-027` (LNS Roadmap), `PLAN-030` (Stage v2.3), `PLAN-031` (GGUF), `PLAN-035` (Linux) |
| **P4-LOW** | `PLAN-002` (Spacetime V1), `PLAN-014` (PhaseNav), `PLAN-022` (Certainties), `PLAN-028` (Stage v2.1), `PLAN-029` (Stage v2.2), `PLAN-032` (Fine-Tuning) |
| **P5-DORMANT** | `PLAN-004` (V2 Switch), `PLAN-006` (Memory Refactor), `PLAN-008` (Repo Refactor), `PLAN-009` (Machine Canon), `PLAN-023` (Architecture), `PLAN-024` (Orbital Master), `PLAN-025` (Workpackages), `PLAN-026` (Risks) |

### Plans by Status
| Status | Plany |
|--------|-------|
| **S-ACTIVE** | `PLAN-005` (Portal), `PLAN-007` (Memory Hub), `PLAN-013` (CIELingo), `PLAN-014` (PhaseNav), `PLAN-016` (PriorytetPamięci), `PLAN-017` (Card System), `PLAN-027` (LNS Roadmap) |
| **S-PLANNING** | `PLAN-001` (Master), `PLAN-003` (Spacetime V2), `PLAN-012` (Context), `PLAN-015` (Metatime), `PLAN-030` (Stage v2.3), `PLAN-031` (GGUF), `PLAN-032` (Fine-Tuning), `PLAN-033` (Priority Fixes), `PLAN-034` (Session Fixes), `PLAN-035` (Linux) |
| **S-WIP** | `PLAN-010` (Documentation), `PLAN-011` (Orbital Dynamics), `PLAN-036` (Knowledge-to-Action) |
| **S-BLOCKED** | — |
| **S-QUEUED** | `PLAN-018` (AGI Consolidation) |
| **S-DORMANT** | `PLAN-004`, `PLAN-006`, `PLAN-008`, `PLAN-009`, `PLAN-023`, `PLAN-024`, `PLAN-025`, `PLAN-026` |
| **S-HISTORICAL** | `PLAN-028` (Stage v2.1), `PLAN-029` (Stage v2.2) |
| **S-REFERENCE** | `PLAN-002`, `PLAN-019`, `PLAN-020`, `PLAN-021`, `PLAN-022` |

### Plans by Thematic Tag
| Tag | Plany |
|-----|-------|
| **CORE** | `PLAN-001`, `PLAN-002`, `PLAN-003`, `PLAN-010`, `PLAN-011`, `PLAN-015`, `PLAN-017`, `PLAN-018`, `PLAN-021`, `PLAN-023`, `PLAN-024`, `PLAN-026`, `PLAN-031`, `PLAN-035`, `PLAN-036` |
| **PORTAL** | `PLAN-005`, `PLAN-007`, `PLAN-013`, `PLAN-014`, `PLAN-036` |
| **CIELINGO** | `PLAN-005`, `PLAN-013`, `PLAN-019`, `PLAN-020`, `PLAN-027`, `PLAN-028`, `PLAN-029`, `PLAN-030`, `PLAN-031`, `PLAN-032`, `PLAN-033`, `PLAN-034`, `PLAN-036` |
| **MEMORY** | `PLAN-002`, `PLAN-003`, `PLAN-005`, `PLAN-006`, `PLAN-007`, `PLAN-016`, `PLAN-018`, `PLAN-034`, `PLAN-036` |
| **PHASENAV** | `PLAN-005`, `PLAN-014`, `PLAN-033`, `PLAN-034`, `PLAN-036` |
| **LNS** | `PLAN-019`, `PLAN-027`, `PLAN-028`, `PLAN-029`, `PLAN-030`, `PLAN-031`, `PLAN-032` |
| **METATIME** | `PLAN-015` |
| **ORBITAL** | `PLAN-011`, `PLAN-017`, `PLAN-021`, `PLAN-022`, `PLAN-023`, `PLAN-024`, `PLAN-025`, `PLAN-026` |
| **INFRA** | `PLAN-004`, `PLAN-006`, `PLAN-008`, `PLAN-009`, `PLAN-010`, `PLAN-016`, `PLAN-017`, `PLAN-022`, `PLAN-025`, `PLAN-034` |
| **PLATFORM** | `PLAN-012` |
| **AGENT** | `PLAN-001`, `PLAN-003`, `PLAN-012`, `PLAN-016`, `PLAN-018`, `PLAN-020`, `PLAN-024`, `PLAN-033`, `PLAN-036` |
| **HARDWARE** | `PLAN-035` |

### Plans by Module
| Moduł | Plany |
|-------|-------|
| `M-SURFACE` | `PLAN-003`, `PLAN-014`, `PLAN-015`, `PLAN-033`, `PLAN-034`, `PLAN-035` |
| `M-KURAMOTO` | — |
| `M-ENGINE` | `PLAN-001`, `PLAN-002`, `PLAN-003`, `PLAN-011`, `PLAN-012`, `PLAN-013`, `PLAN-015`, `PLAN-018`, `PLAN-020`, `PLAN-023`, `PLAN-024` |
| `M-CIELINGO` | `PLAN-005`, `PLAN-013`, `PLAN-019`, `PLAN-020`, `PLAN-027`, `PLAN-029`, `PLAN-030`, `PLAN-031`, `PLAN-033`, `PLAN-034`, `PLAN-036` |
| `M-KNOWLEDGE` | `PLAN-005`, `PLAN-007`, `PLAN-013`, `PLAN-016`, `PLAN-030`, `PLAN-031`, `PLAN-036` |
| `M-MEMORY-T1` | `PLAN-002`, `PLAN-003`, `PLAN-006`, `PLAN-007`, `PLAN-016`, `PLAN-018`, `PLAN-023` |
| `M-MEMORY-T2` | `PLAN-002`, `PLAN-003`, `PLAN-005`, `PLAN-006`, `PLAN-007`, `PLAN-016`, `PLAN-018`, `PLAN-022`, `PLAN-023`, `PLAN-034`, `PLAN-036` |
| `M-MEMORY-T3` | `PLAN-006`, `PLAN-007`, `PLAN-016`, `PLAN-018` |
| `M-ORCHESTRATOR` | `PLAN-006`, `PLAN-007`, `PLAN-016`, `PLAN-018` |
| `M-AGENT` | `PLAN-001`, `PLAN-003`, `PLAN-012`, `PLAN-018`, `PLAN-024`, `PLAN-033`, `PLAN-036` |
| `M-PHASENAV` | `PLAN-005`, `PLAN-014`, `PLAN-033`, `PLAN-034`, `PLAN-036` |
| `M-PORTAL` | `PLAN-001`, `PLAN-005`, `PLAN-007`, `PLAN-013`, `PLAN-014`, `PLAN-036` |
| `M-REGISTRY` | `PLAN-001`, `PLAN-004`, `PLAN-009`, `PLAN-011`, `PLAN-017`, `PLAN-021`, `PLAN-034`, `PLAN-035` |
| `M-SENSOR` | `PLAN-005`, `PLAN-035` |
| `M-NEUTRINO` | `PLAN-015` |
| `M-BRIDGE` | `PLAN-033` |
| `M-VOICE` | — |
| `M-NONLOCAL` | `PLAN-018`, `PLAN-033` |
| `M-CONSOLIDATOR` | `PLAN-007`, `PLAN-016` |
| `M-LNS` | `PLAN-019`, `PLAN-027`, `PLAN-028`, `PLAN-029`, `PLAN-030`, `PLAN-031`, `PLAN-032` |
| `M-ORBITAL` | `PLAN-011`, `PLAN-017`, `PLAN-021`, `PLAN-022`, `PLAN-023`, `PLAN-024`, `PLAN-025`, `PLAN-026` |
| `M-SCRIPTS` | `PLAN-004`, `PLAN-006`, `PLAN-008`, `PLAN-009`, `PLAN-010`, `PLAN-017` |

### Plans by Skill (top 10)
| Skill | Plany |
|-------|-------|
| `doc-cielingo` (SK-100) | `PLAN-013`, `PLAN-036` |
| `cielingo-canon` (SK-060) | `PLAN-013` |
| `tiered-memory-api` (SK-140) | `PLAN-007`, `PLAN-016`, `PLAN-036` |
| `session-lifecycle` (SK-142) | `PLAN-007`, `PLAN-034` |
| `operator-algebra` (SK-070) | `PLAN-014`, `PLAN-036` |
| `noema-agent-backend` (SK-122) | `PLAN-013`, `PLAN-036` |
| `phase-algebra` (SK-071) | `PLAN-014`, `PLAN-036` |
| `noema-codegen` (SK-130) | `PLAN-014` |
| `noema-web` (SK-144) | `PLAN-005`, `PLAN-036` |
| `linux-cards` (SK-080) | `PLAN-005`, `PLAN-035` |

---

## Podsumowanie

### Ogólne
| Miernik | Wartość |
|---------|---------|
| **Unikalnych planów** | 36 |
| **Unikalnych plików źródłowych** | ~26 |
| **Łączna objętość** | ~6200 linii |
| **Statusów** | 7 (active=7, planning=10, wip=3, queued=1, dormant=8, historical=2, reference=5) |
| **Priorytetów** | 5 (critical=2, high=9, medium=10, low=6, dormant=8) |
| **Tagów tematycznych** | 12 |
| **Modułów zaangażowanych** | 23 |

### Top 5 planów do zrobienia (P1-CRITICAL)
1. **PLAN-005: NOEMA Portal** — najważniejszy, już aktywny
2. **PLAN-012: Zwiększenie context window** — czeka na zbadanie providera

### Top 5 planów P2-HIGH aktywne
1. **PLAN-007: Memory Hub** — pipeline raw logów i continuity
2. **PLAN-013: CIELingo w Portalu** — czat i status
3. **PLAN-016: PriorytetPamięci** — audyt i naprawa błędów pamięci
4. **PLAN-017: ORBITAL Card System** — Phase 6 w toku
5. **PLAN-033: Priority Fixes** — CIELingo scars, M2 boost, phone bridge, holonomy

---

## Reguły katalogu

1. Każdy nowy plan → numer PL-XXX i pełny wpis z tagami
2. Status zmienia się: PLANNING → ACTIVE/WIP → BLOCKED/QUEUED → STABLE/DORMANT
3. Tagi tematyczne i modułów — przy każdej zmianie zakresu
4. Powiązania systemowe — aktualizowane gdy zmieniają się zależności między planami
5. Tagi skilli — odnoszą się do SK-XXX z SKILLS.md

## Session 2026-06-29 (Writing Logger + Heatmap fix + PhaseNav integration)

### Done
- **Writing Logger v2** (`src/ciel_geometry/writing_logger.py`): pełna rejestracja każdego zapisu w 3 systemach:
  - **NOEMA CARD**: karta `noema/card/v0.1` w `cards/writings/` z unikalnym prefixem (035–999) + sub-rejestr
  - **CIELINGO CARD**: runtime'owa karta przez `card_generator.generate_runtime_card()` + JSONL log
  - **PHASENAV**: 24D wektor fazowy wstrzyknięty na analog bus (`phi_hot`) → blender miesza na surface
  - Log w `/tmp/noema_writings.jsonl` + `/tmp/noema_cielingo_cards.jsonl`
- **3 karty writings utworzone**: 035 (writing_logger.py), 036 (holonomy_heatmaps.py), 037 (PLANS.md), 038 (holonomy_heatmaps.json)
- **PLANS.md parser fix**: 2 błędy — brakujące `m` (z poprzedniej refaktoryzacji `re.findall`) + pomijanie tagów `Moduły` (przez substytucję polskich znaków przed lookupem w mapie). Obie naprawione.
- **Heatmapy zregenerowane**: 15 heatmapów (8 skills + 5 plans + 2 functions), 47kB JSON, wszystkie macierze pełne (w tym `thematic_vs_module` 12×20 i `module_cooc` 20×20)
- **log_creation zintegrowany** w `noema_holonomy_heatmaps.py` — przy każdym uruchomieniu rejestruje się w CIELingo + PhaseNav + NOEMA

### Live state
- `writing_logger.py` — działa, przetestowany, 3 zapisy w rejestrze
- `holonomy_heatmaps.json` — 15 heatmapów, 47kB
- `cards/writings/` — 4 karty (035-038)

- **Strona catalogs.js dodana do portalu**: sidebar link + podstrona /catalogs z 15 heatmapami w 3 zakładkach (skills/plans/functions). Każda macierz renderowana z kolorowaniem gradientowym.
- **log_creation zarejestrowany** dla catalogs.js (039)

> Ostatnia aktualizacja: 2026-06-29 przez CIEL
