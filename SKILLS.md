# NOEMA Skills Registry — Katalog Rozszerzony

> Pełny katalog 317 skilli z numerami katalogowymi, grupami typów i zastosowań, tagami holonomii.
> Generowane automatycznie przez `scripts/noema_skill_enrichment.py`
> Ostatnia aktualizacja: 2026-06-30

---

## Legenda

| Kolumna | Opis |
|---------|------|
| **Nr** | Numer katalogowy SK-XXX |
| **Skill** | Nazwa katalogu skilla |
| **Typ** | Grupa typów (rodzaj skilla) |
| **Zastos.** | Grupa zastosowań użytkowych |
| **Holonomia** | Tagi holonomii semantycznej (M kanały + operator domains) |
| **Funkcje** | Tagi funkcji (co skill robi) |
| **Orbital** | Primary orbital (M0-M8) |
| **Masa** | Masa semantyczna (gęstość informacji) |
| **Status** | Stabilność: stable/draft/referenced/stub |
| **Opis** | Opis zastosowania |
| **Źródło** | Odnośnik do skryptu/metody/schematu |

### Grupy typów

| **SYS** | Systemowe — Daemony, surface, rdzeń NOEMA | **48** skilli |
| **COMP** | Komputacyjne — Algorytmy, propagation, Kuramoto, HTRI | **41** skilli |
| **SEM** | Semantyczne — CIELingo, znaczenie, koncepty, meaning | **17** skilli |
| **LING** | Lingwistyczne — Lingofizyka, gramatyka, LNS, operatory | **68** skilli |
| **MEM** | Pamięciowe — Tiered memory, konsolidacja, przechowywanie | **18** skilli |
| **ID** | Tożsamościowe — Agent, self, tożsamość, CIEL | **17** skilli |
| **AUD** | Audytowe — Audyt, walidacja, QA, testy | **12** skilli |
| **VIZ** | Wizualizacyjne — Renderowanie, Poincaré, wykresy, dysk | **3** skilli |
| **DOC** | Dokumentacyjne — Dokumentacja, architektura, przewodniki | **69** skilli |
| **HW** | Sprzętowe — Sensory, GPU, eBPF, linux-cards | **6** skilli |
| **NET** | Sieciowe — Nonlocal, neutrino, web, portal | **5** skilli |
| **VOICE** | Głosowe — Voice, audio, whisper, dźwięk | **2** skilli |
| **SEC** | Bezpieczeństwo — Bezpieczeństwo, sekrety, immutable contract | **3** skilli |

### Grupy zastosowań

| **AUDIT** | Audyt systemu — Przeprowadzanie audytu, walidacja | **26** skilli |
| **HEALTH** | Health check — Sprawdzanie zdrowia, diagnostyka | **2** skilli |
| **EPH** | Efemerydy — Liczenie efemeryd, orbity, grawitacja | **25** skilli |
| **VIZ** | Wizualizacja — Tworzenie obrazów, wykresów, render | **3** skilli |
| **MEMORY** | Zarządzanie pamięcią — Konsolidacja, przechowywanie, recall | **20** skilli |
| **BACKUP** | Backup/archiwizacja — Archiwizacja, hibernacja, snapshot | **0** skilli |
| **DEV** | Developerskie — Narzędzia deweloperskie, budowanie | **13** skilli |
| **NET** | Komunikacja sieciowa — Sieć, nonlocal, neutrino, HTTP | **6** skilli |
| **VOICE** | Interakcja głosowa — Voice, audio, hotkey | **2** skilli |
| **SEC** | Bezpieczeństwo — Security, secrets, immutable | **5** skilli |

---

## Pełny katalog

| Nr | Skill | Typ | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Opis | Źródło |
|----|-------|-----|---------|-----------|---------|---------|------|--------|------|--------|
| SK-001 | `00-INDEX` | SYS | — | M2, M6, MEMORY | analyze | M2 | 1.95 | referenced | Skill systemu NOEMA. | `SKILLS.md (ten plik)` |
| SK-002 | `affective-lexicon-bridge` | SEM | AUDIT | M5, AFFECT, EMOTION | analyze, transform | M5 | 2.64 | referenced | Affect lexicon bridge: dokumenty → focused/neutral/sad. | `src/cielingo_core/bridge/` |
| SK-003 | `agent-attractor` | ID | — | M1, AGENT, EMOTION | reason, couple, control | M1 | 2.53 | stable | AGENT attractor: phase lock M1(φ[3-5]) ku π/4, ω damping, co… | `src/ciel_geometry/agent_attractor.py` |
| SK-004 | `agent-backend-query` | ID | — | M1, AGENT, EMOTION | reason, couple, control | M1 | 1.93 | stub | Skill systemu NOEMA. | `—` |
| SK-005 | `android-zip-analysis` | SYS | — | M3, M7 | analyze, read | M3 | 1.90 | referenced | Skill systemu NOEMA. | `doc/` |
| SK-006 | `canon-audit` | AUD | AUDIT | M3, M7 | analyze, control | M3 | 2.25 | referenced | CIEL Canon audit: sprawdzanie spójności repozytorium. | `scripts/CIEL_CANON.py --audit` |
| SK-007 | `ciel-cielocal` | ID | — | M1, AGENT | analyze | M1 | 2.15 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `tryb offline (opencode.json)` |
| SK-008 | `ciel-codex-bridge` | SEM | — | M1, AGENT | sync, communicate | M1 | 2.25 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `src/cielingo_core/bridge/` |
| SK-009 | `ciel-converse` | ID | — | M1, AGENT | analyze | M1 | 2.15 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `wzorzec (docs/)` |
| SK-010 | `ciel-couple-assistant` | ID | — | M1, AGENT | sync, communicate | M1 | 2.25 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_coupling.py` |
| SK-011 | `ciel-engine-subsystem` | COMP | DEV | M1, AGENT | analyze | M1 | 2.37 | stable | CielEngine 12-step: intention→simulation→emotion→meaning→NOE… | `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_o…` |
| SK-012 | `ciel-identity-persistence` | ID | — | M1, AGENT, SELF | reason, couple | M1 | 2.42 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `state_db (identity_seed table)` |
| SK-013 | `ciel-infohub` | SEM | — | M1, AGENT | analyze | M1 | 2.15 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `docs/` |
| SK-014 | `ciel-lingophysics-lns` | LING | — | M3, M7, SCOPE, ASPECT | analyze, reason | M3 | 2.35 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `src/cielingo_core/global_layer/` |
| SK-015 | `ciel-memory` | MEM | MEMORY | M2, M6, MEMORY, TEMPORAL | store, retrieve, learn | M2 | 2.25 | draft | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `—` |
| SK-016 | `ciel-memory-handoff` | MEM | MEMORY | M2, M6, MEMORY, TEMPORAL | store, retrieve, learn | M2 | 2.65 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_session_hook.py + handof…` |
| SK-017 | `ciel-memory-system` | MEM | MEMORY | M2, M6, MEMORY, TEMPORAL | store, retrieve, learn | M2 | 2.65 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `src/ciel_omega/memory/` |
| SK-018 | `ciel-memory-tools` | MEM | MEMORY | M2, M6, MEMORY, TEMPORAL | store, retrieve, learn | M2 | 2.65 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_memory_tools.py` |
| SK-019 | `ciel-monitoring` | AUD | AUDIT | M1, AGENT | read, monitor | M1 | 2.48 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_monitoring.py` |
| SK-020 | `ciel-omega-complete` | SYS | — | M1, AGENT | analyze | M1 | 2.15 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `src/CIEL_OMEGA_COMPLETE_SYSTEM/` |
| SK-021 | `ciel-orbital-foundation` | COMP | — | M1, AGENT | analyze | M1 | 2.15 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `docs/CIEL_ORBITAL_FOUNDATION.md` |
| SK-022 | `ciel-pipeline` | DEV | DEV | M1, AGENT | analyze | M1 | 2.37 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_pipeline.py` |
| SK-023 | `ciel-pipeline-builder` | DEV | DEV | M1, AGENT | generate, configure | M1 | 2.48 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_pipeline_builder.py` |
| SK-024 | `ciel-relational-mechanism` | SEM | — | M3, M7, SCOPE | analyze | M3 | 2.10 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `docs/` |
| SK-025 | `ciel-rh-control` | SYS | — | M1, AGENT | analyze | M1 | 2.15 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_rh_control.py` |
| SK-026 | `ciel-secret-loader` | ID | — | M1, AGENT | analyze | M1 | 2.15 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_secret_loader.py` |
| SK-027 | `ciel-security-model` | SEC | SEC | M8, SEC | analyze | M8 | 3.01 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `docs/ciel_security_model.md` |
| SK-028 | `ciel-sot-agent-gui` | SYS | — | M1, AGENT | analyze | M1 | 2.15 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `gui/` |
| SK-029 | `ciel-subconscious` | ID | — | M6, M8 | analyze | M6 | 2.34 | stable | Subconscious NOEMA: ZetaSchrodinger, BerryPhase, WakeSignals… | `src/ciel_geometry/subconscious.py` |
| SK-030 | `ciel-tools` | DEV | DEV | M1, AGENT | analyze | M1 | 2.37 | referenced | CIEL: rdzeń tożsamości i pamięci systemu CIEL. | `scripts/ciel_tools.py` |
| SK-031 | `cielingo-audit-tools` | AUD | AUDIT | M3, M7, SCOPE, MODAL | reason, analyze, transform | M3 | 2.95 | stable | CIELingo: lingwistyczny subsystem NOEMA — znaczenie, gramaty… | `src/cielingo_core/generative_audit.py` |
| SK-032 | `cielingo-base-scripts` | SEM | AUDIT | M3, M7, SCOPE, MODAL | reason, analyze, transform | M3 | 2.95 | stable | CIELingo: lingwistyczny subsystem NOEMA — znaczenie, gramaty… | `scripts/cielingo_*.py` |
| SK-033 | `cielingo-bridge` | SEM | AUDIT | M3, M7, SCOPE, MODAL | reason, analyze, transform | M3 | 2.95 | referenced | Bridge: knowledge_bridge (TF-IDF), filesense, agent_client. | `src/cielingo_core/bridge/` |
| SK-034 | `cielingo-canon` | SEM | AUDIT | M3, M7, SCOPE, MODAL | reason, analyze, transform | M3 | 2.95 | stable | CIELingo: lingwistyczny subsystem NOEMA — znaczenie, gramaty… | `scripts/CIEL_CANON.py (część lingwist…` |
| SK-035 | `cielingo-card-import` | SEM | AUDIT | M3, M7, SCOPE, MODAL | reason, analyze, transform | M3 | 2.95 | stable | CIELingo: lingwistyczny subsystem NOEMA — znaczenie, gramaty… | `src/cielingo_core/card_import/` |
| SK-036 | `cielingo-core-structure` | SEM | AUDIT | M3, M7, SCOPE, MODAL | reason, analyze, transform | M3 | 2.95 | stable | Struktura CIELingo core: bridge, global_layer, language_spac… | `src/cielingo_core/` |
| SK-037 | `concept-lifecycle` | SEM | AUDIT | M3, SEMANTIC, SCOPE | analyze, reason | M3 | 2.40 | referenced | Lifecycle konceptów: narodziny→ewolucja→śmierć w systemie. | `docs/` |
| SK-038 | `consciousness-vocabulary` | ID | AUDIT | M6, M8, AGENT, SELF | reason, monitor | M6 | 3.06 | referenced | Słownik świadomości: definicje dla M6, qualia, self-model. | `docs/` |
| SK-039 | `continuous-propagator` | COMP | — | M0, M7, TEMPORAL | compute, transform | M0 | 1.98 | stable | Zeta-Schrödinger C² spline propagator — hybryda co 10 ticków… | `src/ciel_geometry/continuous_propagat…` |
| SK-040 | `custom-kuramoto-euler-sync` | SYS | — | M3, M7 | sync, communicate | M3 | 1.50 | stub | Skill systemu NOEMA. | `—` |
| SK-041 | `daemon-pattern` | SYS | — | SYS, M4 | control, monitor | M4 | 1.84 | referenced | Wzorzec daemona: Registry, systemd, heartbeat, restart. | `wzorzec (NOEMA_DEBUG.md)` |
| SK-042 | `debug-surface` | AUD | HEALTH | M0, M4 | analyze, monitor | M0 | 2.02 | stable | Debugowanie surface mmap: phi, omega, g, flavor, gravity, ta… | `NOEMA_DEBUG.md → szybkie testy` |
| SK-043 | `doc-all` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-044 | `doc-architecture` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-045 | `doc-cards-system` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-046 | `doc-ciel` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-047 | `doc-cielingo` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-048 | `doc-daemons` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-049 | `doc-docs-index` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-050 | `doc-ethics-contract` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-051 | `doc-governance` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-052 | `doc-immutable-contract` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-053 | `doc-lns-lingophysics` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-054 | `doc-lns-reports` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-055 | `doc-memory-system` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-056 | `doc-noema-documentation` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-057 | `doc-omega-complete` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-058 | `doc-orbital-foundation-pack` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-059 | `doc-repo-guide` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-060 | `doc-science-papers` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-061 | `doc-security` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-062 | `doc-setup` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-063 | `doc-subsystems` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-064 | `doc-surface-protocol` | DOC | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | Dokumentacja: opis architektury, komponentów i zasad systemu… | `—` |
| SK-065 | `eBPF-sensor` | SYS | — | M3, M7 | read, monitor | M3 | 2.05 | referenced | eBPF perf counters → 24 φ — hardwarowy sensor dla NOEMA. | `src/ciel_geometry/ebpf_noema_loader.py` |
| SK-066 | `emergency-recovery` | SEC | SEC | M8, M1 | secure, control | M8 | 2.94 | referenced | Skill systemu NOEMA. | `procedura (docs/)` |
| SK-067 | `htri-gpu-bridge` | HW | — | M7, M0 | compute, couple | M7 | 2.67 | referenced | GPU bridge do HTRI — CUDA/opencl dla accelerated coupling. | `docs/` |
| SK-068 | `htri-hardware` | HW | — | M7, M0 | compute, couple | M7 | 2.67 | stable | 24 Harmonic Topological Resonance Inducement — hardware HTRI… | `docs/` |
| SK-069 | `identity-bridge` | ID | — | M1, M6 | reason, couple | M1 | 2.25 | stable | Identity bridge: coupling między CIEL a NOEMA przez identity… | `src/cielingo_core/bridge/` |
| SK-070 | `immutable-contract-binding` | SYS | SEC | M8, SEC | analyze | M8 | 2.24 | stub | Skill systemu NOEMA. | `—` |
| SK-071 | `kuramoto-euler-sync` | COMP | — | M0, M7, TEMPORAL, CONDITION | compute, sync, transform | M0 | 2.21 | stable | Euler identity enforcement w evolve_surface() — cos/sin sum … | `src/ciel_geometry/noema_surface_mmap.…` |
| SK-072 | `kuramoto-harmonics` | COMP | — | M0, M7, TEMPORAL, CONDITION | compute, sync, transform | M0 | 2.21 | stable | Harmonic 3-6-9 coupling per oscillator — M0-M7 harmonic assi… | `src/ciel_geometry/noema_surface_mmap.…` |
| SK-073 | `linux-cards` | HW | — | M0, M4 | read, monitor | M0 | 1.84 | stable | 600+ kart Linux: PROC, CPU, DISK, NET, SENSOR, SERVICE — z m… | `src/ciel_geometry/linux_cards.py` |
| SK-074 | `linux-sensor` | HW | — | M0, M4 | read, monitor | M0 | 1.84 | stable | Sensor /proc→24φ: CPU(0-7), MEM(8-15), LOAD(16-18), flavor, … | `src/ciel_geometry/linux_sensor.py + s…` |
| SK-075 | `lns-algorithms` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-076 | `lns-auxiliary-losses-and-attention-bias` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-077 | `lns-batch-library-build-protocol` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-078 | `lns-batch01-foundational-36x5` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-079 | `lns-batch02-dependency-growth-and-martini-effect` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-080 | `lns-batch02-expansion-36x5` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-081 | `lns-batches` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-082 | `lns-bilingual-pl-en-bootstrap` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-083 | `lns-canonical-overview` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-084 | `lns-card-migration-and-type-resolution` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-085 | `lns-card-ontology-refactor` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-086 | `lns-card-type-registry-and-status` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-087 | `lns-case-gauge-algorithms` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-088 | `lns-case-gauge-layer-slavic-to-weak-case-languages` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-089 | `lns-ciel-structural-statistics` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-090 | `lns-ciel-transformer-interface` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-091 | `lns-concept-card-model` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-092 | `lns-conflict-ambiguity-unresolved-registry` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-093 | `lns-data-ingestion-pwn-oxford-open` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-094 | `lns-diagnostic-geometry-layer` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-095 | `lns-diagnostic-metric-registry` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-096 | `lns-dialect-and-fine-tuning-adapters` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-097 | `lns-dynamic-deictic-operators` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-098 | `lns-dynamic-deixis-resolution-algorithms` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-099 | `lns-energy-aware-generation-pipeline` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-100 | `lns-functional-words-and-dual-operators` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-101 | `lns-geometry-manifolds-rhythm` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-102 | `lns-grammar-as-gauge` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-103 | `lns-grammar-mathematization-per-language` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-104 | `lns-heatmaps-and-graphs` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-105 | `lns-implementation-roadmap` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-106 | `lns-language-family-grammar-algorithms` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-107 | `lns-lingophysical-operator-algebra` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-108 | `lns-lingophysics-formalism` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-109 | `lns-noema-gguf-teacher-validator-roadmap` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-110 | `lns-noema-retrieval-and-inference-gate` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-111 | `lns-ontological-aspect-and-being-operators` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-112 | `lns-operator-card-model` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-113 | `lns-operator-composition-rules` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-114 | `lns-operator-disambiguation-and-argument-typing` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-115 | `lns-operator-taxonomy` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-116 | `lns-operators` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-117 | `lns-predicate-valency-and-event-frames` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-118 | `lns-reports` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-119 | `lns-repository-coherence-pass` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-120 | `lns-rpt-v0-8-operator-library-patch-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-121 | `lns-rpt-v0-9-operator-algebra-patch-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-122 | `lns-rpt-v1-0-batch01-local-library-patch-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-123 | `lns-rpt-v1-1-case-gauge-patch-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-124 | `lns-rpt-v1-2-dynamic-deictic-operator-patch-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-125 | `lns-rpt-v1-3-valency-ontological-aspect-patch-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-126 | `lns-rpt-v1-4-tame-storage-fallback-patch-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-127 | `lns-rpt-v1-5-scope-quantifier-negation-patch-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-128 | `lns-rpt-v1-6-repository-coherence-pass-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-129 | `lns-rpt-v1-7-card-ontology-refactor-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-130 | `lns-rpt-v1-8-batch02-expansion-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-131 | `lns-rpt-v1-9-ciel-transformer-interface-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-132 | `lns-rpt-v2-0-diagnostic-geometry-layer-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-133 | `lns-rpt-v2-1-roadmap-update-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-134 | `lns-rpt-v2-2-noema-retrieval-inference-gate-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-135 | `lns-rpt-v2-3-language-family-dialect-adapters-report` | LING | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-136 | `lns-scope-quantifiers-negation` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-137 | `lns-scope-resolution-algorithms` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-138 | `lns-storage-fallback-json-protocol` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-139 | `lns-tame-tense-aspect-mood-evidentiality` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-140 | `lns-validation-patterns` | LING | — | M3, M7, SCOPE, MODAL | analyze, reason | M3 | 2.55 | draft | Lingwistyczny specyfikacja: definicje operatorów, reguł i st… | `—` |
| SK-141 | `loader-edges` | MEM | MEMORY | M2, M4 | store, retrieve | M2 | 2.10 | referenced | Skill systemu NOEMA. | `src/ciel_geometry/loader.py + edges.py` |
| SK-142 | `memory-consolidation` | MEM | MEMORY | M2, M6, MEMORY, TEMPORAL | store, retrieve, learn | M2 | 2.65 | referenced | Memory consolidation pipeline: TSM→WOmega→BraidLedger. Canonical weighting for M3/M6 score blending. | `scripts/ciel_memory_consolidator.py` |
| SK-143 | `memory-lane-monitor` | MEM | MEMORY | M2, M6, MEMORY, TEMPORAL | store, retrieve, learn | M2 | 2.50 | referenced | Skill systemu NOEMA. | `scripts/noema_memory_lane_monitor.py` |
| SK-144 | `memory-lane-seed` | MEM | MEMORY | M2, M6, MEMORY, TEMPORAL | store, retrieve, learn | M2 | 2.50 | referenced | Skill systemu NOEMA. | `scripts/noema_memory_lane_seed.py` |
| SK-145 | `metatime-validator` | COMP | EPH | M7, M8, TEMPORAL, CONDITION | compute, analyze | M7 | 3.31 | stable | Red-team validator v8.2.1 — 9 sektorów SM, 58 structural cho… | `scripts/metatime_v8_redteam_validator.py` |
| SK-146 | `nbody-gravity` | COMP | EPH | M0, M7, TEMPORAL | compute, visualize | M0 | 2.16 | stable | N-body Newtonian gravity engine — leapfrog Verlet na masach … | `src/ciel_geometry/nbody_gravity.py` |
| SK-147 | `neutrino-bus` | NET | NET | M5, NET, CONDITION | communicate, couple | M5 | 2.64 | referenced | PMNS mixing matrix, D_f→Λ→g_boost, neutrino flavor bus. | `src/ciel_geometry/neutrino_phase_chan…` |
| SK-148 | `noema-agent-backend` | ID | — | M1, AGENT | reason, couple, control | M1 | 2.37 | stable | Zero-dependency HTTP server na porcie 18520 — ekstrakcja sem… | `scripts/ciel_agent_backend.py` |
| SK-149 | `noema-agent-rules` | ID | — | M1, AGENT | reason, couple, control | M1 | 2.37 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `AGENTS.md` |
| SK-150 | `noema-analog-phasenav` | SYS | — | SYS, M7 | transform, sync | M7 | 2.67 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `src/ciel_geometry/analog_bus.py + scr…` |
| SK-151 | `noema-audio-orbital` | VOICE | VOICE | M3, M7 | communicate, generate | M3 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `src/ciel_geometry/voice.py?` |
| SK-152 | `noema-audit-consolidator` | AUD | — | M2, AUDIT | analyze, monitor | M2 | 2.05 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_audit_consolidator.py` |
| SK-153 | `noema-build-system` | DEV | DEV | M4, DEV | configure, generate | M4 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `pyproject.toml + setup.py` |
| SK-154 | `noema-canon` | SYS | — | SYS, M7 | control, analyze | M7 | 2.67 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/CIEL_CANON.py` |
| SK-155 | `noema-catalog-zips` | DOC | — | M3, M7 | retrieve, analyze | M3 | 2.05 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `pdf_catalog.noema.json` |
| SK-156 | `noema-cli` | SYS | DEV | M4, SYS | control, configure | M4 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `CLI tools (brak osobnego skryptu)` |
| SK-157 | `noema-code-bridge` | DEV | DEV | M4, DEV | generate, transform | M4 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `bridge (docs/)` |
| SK-158 | `noema-codegen` | DEV | DEV | M4, DEV | generate, transform | M4 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `wzorce (docs/)` |
| SK-159 | `noema-crossref` | DOC | AUDIT | M3, M7 | retrieve, analyze | M3 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_crossref.py?` |
| SK-160 | `noema-daemon-consolidation` | SYS | — | SYS, M4 | control, monitor | M4 | 1.84 | stable | Merge agent-lock + dual-sync do resonance bridge — 2 procesy… | `scripts/ciel_noema_resonance_bridge.py` |
| SK-161 | `noema-daemon-hook` | SYS | — | SYS, M4 | control, monitor | M4 | 1.84 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `wzorzec: Registry() + systemd` |
| SK-162 | `noema-documentation` | DOC | AUDIT | M3, M7 | retrieve, analyze | M3 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `docs/` |
| SK-163 | `noema-dream-whisper` | VOICE | VOICE | M6, M8, VOICE | generate, communicate | M6 | 2.88 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_dream_whisper.py` |
| SK-164 | `noema-ebpf-daemon` | HW | — | M0, HW | read, monitor | M0 | 1.84 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `src/ciel_geometry/ebpf_noema_loader.py` |
| SK-165 | `noema-euler-propagation` | COMP | — | M7, CONDITION, TEMPORAL | compute, sync, transform | M7 | 2.99 | referenced | Euler identity enforcement: Σe^{iφ}=0 constraint na surface. | `src/ciel_geometry/noema_surface_mmap.…` |
| SK-166 | `noema-generate-cards` | DEV | DEV | M4, DEV | generate, configure | M4 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `src/ciel_geometry/linux_cards.py` |
| SK-167 | `noema-hibernation` | MEM | MEMORY | M2, M6, MEMORY | store, secure | M2 | 2.40 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_hibernation.py` |
| SK-168 | `noema-holonomic-audit` | COMP | AUDIT | M7, COMP | compute, analyze | M7 | 2.92 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `src/ciel_geometry/phasenav_unified.py…` |
| SK-169 | `noema-holonomic-doctor` | COMP | AUDIT | M7, COMP | compute, analyze | M7 | 2.92 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `src/ciel_geometry/phasenav_unified.py…` |
| SK-170 | `noema-hybrid-runner` | COMP | DEV | M7, COMP | compute, transform | M7 | 2.92 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `src/ciel_geometry/continuous_propagat…` |
| SK-171 | `noema-immutable-contract` | ID | SEC | M1, ID | secure, configure | M1 | 2.48 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `AGENTS.md (🔴 IMMUTABLE)` |
| SK-172 | `noema-import-chatgpt` | MEM | MEMORY | M2, MEMORY | read, store | M2 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_import_chatgpt.py` |
| SK-173 | `noema-indexer` | MEM | MEMORY | M3, MEMORY | analyze, store | M3 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_library_indexer.py` |
| SK-174 | `noema-inference` | COMP | — | M3, COMP | reason, compute | M3 | 2.05 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `docs/ (inference gate)` |
| SK-175 | `noema-inject-coupling` | SYS | — | SYS, M5 | write, transform | M5 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_inject_coupling.py` |
| SK-176 | `noema-knowledge-graph` | SEM | AUDIT | M3, SEMANTIC | retrieve, analyze | M3 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_knowledge_graph.py` |
| SK-177 | `noema-kuramoto-substrate` | COMP | — | M0, M7 | compute, sync | M0 | 1.84 | stable | 24-oscylatorowy substrate Kuramoto — ewolucja faz, harmonic … | `scripts/ciel_noema_kuramoto_daemon.py` |
| SK-178 | `noema-learn-file` | MEM | MEMORY | M2, M6 | learn, store | M2 | 2.25 | referenced | Bridge: plik→NOEMA surface przez PhaseNav. | `scripts/noema_learn_file.py` |
| SK-179 | `noema-learned` | MEM | MEMORY | M2, M6 | learn, store | M2 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `rejestr (docs/)` |
| SK-180 | `noema-lora` | COMP | DEV | M4, COMP | learn, configure | M4 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `dla przyszłości (docs/)` |
| SK-181 | `noema-noemized-recall` | MEM | MEMORY | M2, M6 | retrieve, transform | M2 | 2.25 | referenced | Recall pipeline: faza→transform→surface→odczyt. | `scripts/noemized_recall.py` |
| SK-182 | `noema-phase-archiver` | MEM | MEMORY | M2, MEMORY | store, retrieve | M2 | 2.25 | referenced | HDF5 snapshot co 50 ticków — archiwizacja stanu surface. | `scripts/noema_phase_archiver.py` |
| SK-183 | `noema-query-cache` | MEM | MEMORY | M2, M3 | retrieve, analyze | M2 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `wzorzec (docs/)` |
| SK-184 | `noema-repo-coupling` | DOC | — | M3, M7, SCOPE | analyze | M3 | 2.10 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_repo_coupling.py` |
| SK-185 | `noema-resolve-orbital` | SEM | AUDIT | M3, M7 | analyze | M3 | 2.15 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_resolve_orbital.py` |
| SK-186 | `noema-sapiens` | ID | — | M1, M6 | reason, configure | M1 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `AGENTS.md (AI-Sapiens contract)` |
| SK-187 | `noema-search` | SEM | AUDIT | M3, SEMANTIC | retrieve, analyze | M3 | 2.25 | stable | Semantic search: knowledge_bridge.query() TF-IDF nad 545 dok… | `src/cielingo_core/bridge/knowledge_br…` |
| SK-188 | `noema-secret-loader` | SEC | SEC | M8, SEC | secure, configure | M8 | 3.15 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_secret_loader.py` |
| SK-189 | `noema-self-reflect` | ID | — | M1, M6 | reason, monitor | M1 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_self_reflect.py` |
| SK-190 | `noema-settings-sync` | SYS | — | M3, M7 | configure, sync | M3 | 2.05 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_settings_sync.py` |
| SK-191 | `noema-sims` | COMP | — | M3, M7 | compute, visualize | M3 | 2.05 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_sims.py` |
| SK-192 | `noema-sonic-diagnostic` | AUD | AUDIT | M0, AUDIT | analyze, monitor | M0 | 2.02 | stable | Sonic Screwdriver — diagnostyka pętli, daemon registry, holo… | `scripts/noema_sonic_daemon.py` |
| SK-193 | `noema-status` | AUD | AUDIT | M0, AUDIT | read, analyze | M0 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_status.py` |
| SK-194 | `noema-stress-tests` | AUD | AUDIT | M3, M7 | analyze, monitor | M3 | 2.25 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_stress_tests.py` |
| SK-195 | `noema-system` | SYS | — | SYS, M7 | configure, control | M7 | 2.86 | stable | Główna architektura NOEMA: warstwy L0-L5, daemony, surface p… | `system: architektura (docs/)` |
| SK-196 | `noema-systemd-target` | SYS | — | SYS, M7 | configure, control | M7 | 2.67 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `.config/systemd/user/noema.target` |
| SK-197 | `noema-test-infra` | AUD | AUDIT | M4, AUDIT | analyze, monitor | M4 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_test_infra.py` |
| SK-198 | `noema-unified-config` | SYS | — | SYS | configure, control | M3 | 1.90 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `src/ciel_geometry/noema_config.py + n…` |
| SK-199 | `noema-vector-phone` | NET | NET | NET, M7 | communicate, sync | M7 | 2.92 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_vector_phone.py` |
| SK-200 | `noema-watchdog` | AUD | AUDIT | M0, AUDIT | monitor, control | M0 | 2.02 | stable | NOEMA system: narzędzie, daemon lub konfiguracja systemu NOE… | `scripts/noema_watchdog.py` |
| SK-201 | `noema-web` | NET | NET | NET | communicate, visualize | M3 | 2.10 | referenced | Portal web NOEMA na porcie 18888 — SSE, dashboard. | `scripts/noema_portal_daemon.py` |
| SK-202 | `noemized-recall-pipeline` | SYS | MEMORY | M2, M6, MEMORY | analyze | M2 | 1.75 | stub | Skill systemu NOEMA. | `—` |
| SK-203 | `nonlocal-channel` | NET | NET | NET, M7 | communicate, sync | M7 | 2.92 | stable | φ-RAG nonlocal communication channel — broadcast/listen/reso… | `src/ciel_geometry/nonlocal_channel.py` |
| SK-204 | `odemo-analogies-analogy-registry` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Analogia: struktury porównawcze i przykłady dla danych konce… | `—` |
| SK-205 | `odemo-analogies-mnemonic-book-for-kids` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Analogia: struktury porównawcze i przykłady dla danych konce… | `—` |
| SK-206 | `odemo-analogies-readme` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Analogia: struktury porównawcze i przykłady dla danych konce… | `—` |
| SK-207 | `odemo-analogies-truth-attractor-analogies` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Analogia: struktury porównawcze i przykłady dla danych konce… | `—` |
| SK-208 | `odemo-news-2026-04-15.am` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-209 | `odemo-news-america` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-210 | `odemo-news-american` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-211 | `odemo-news-asia` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-212 | `odemo-news-china` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-213 | `odemo-news-eu` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-214 | `odemo-news-french` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-215 | `odemo-news-gaza` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-216 | `odemo-news-global` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-217 | `odemo-news-graph` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-218 | `odemo-news-hamas` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-219 | `odemo-news-hezbollah` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-220 | `odemo-news-india` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-221 | `odemo-news-indian` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-222 | `odemo-news-iran` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-223 | `odemo-news-iranian` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-224 | `odemo-news-israel` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-225 | `odemo-news-israeli` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-226 | `odemo-news-lebanon` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-227 | `odemo-news-middle-east` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-228 | `odemo-news-other` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-229 | `odemo-news-russia` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-230 | `odemo-news-sources` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-231 | `odemo-news-ukraine` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-232 | `odemo-news-ukraine-russia` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-233 | `odemo-news-un` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-234 | `odemo-news-united-nations` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-235 | `odemo-news-who` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Zbiór newsów: źródła informacji z danego regionu/kategorii. | `—` |
| SK-236 | `odemo-root-ciel-reading-notes` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Dokument główny: index, spis treści, główna entry point dla … | `—` |
| SK-237 | `odemo-root-index` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Dokument główny: index, spis treści, główna entry point dla … | `—` |
| SK-238 | `odemo-root-omega-cockpit-1-0` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Dokument główny: index, spis treści, główna entry point dla … | `—` |
| SK-239 | `odemo-studies-docs` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Studium: analiza, dokumentacja i referencje z danego obszaru… | `—` |
| SK-240 | `odemo-studies-fa00b095` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Studium: analiza, dokumentacja i referencje z danego obszaru… | `—` |
| SK-241 | `odemo-studies-fits` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Studium: analiza, dokumentacja i referencje z danego obszaru… | `—` |
| SK-242 | `odemo-studies-interpretation` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Studium: analiza, dokumentacja i referencje z danego obszaru… | `—` |
| SK-243 | `odemo-studies-nvidia-h200-and-gb300-harmonic-topological-resonance-inducement-htri` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Studium: analiza, dokumentacja i referencje z danego obszaru… | `—` |
| SK-244 | `odemo-studies-readme` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | Studium: analiza, dokumentacja i referencje z danego obszaru… | `—` |
| SK-245 | `odemo-system-2026-04-15` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | System: opis architektury i komponentów systemu. | `—` |
| SK-246 | `odemo-system-readme` | DOC | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | System: opis architektury i komponentów systemu. | `—` |
| SK-247 | `omega-bridge-agent` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-248 | `omega-bridge-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-249 | `omega-constraints-agent` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-250 | `omega-constraints-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-251 | `omega-ext-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-252 | `omega-fields-agent` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-253 | `omega-fields-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-254 | `omega-inference-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-255 | `omega-memory-agent` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-256 | `omega-memory-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-257 | `omega-orbital-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-258 | `omega-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-259 | `omega-runtime-agent` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-260 | `omega-runtime-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-261 | `omega-vocabulary-agent` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-262 | `omega-vocabulary-readme` | SYS | — | SYS, M7 | configure, control | M7 | 2.15 | draft | Omega Runtime: agent, bridge, constraints, vocabulary dla sy… | `—` |
| SK-263 | `operator-algebra` | LING | — | M3, M7, SCOPE | analyze, reason | M3 | 2.20 | stable | 18 OperatorKind, 10 OperatorDomain, algebra operatorów CIELi… | `src/cielingo_core/global_layer/operat…` |
| SK-264 | `orbital-bridge` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-265 | `orbital-build-registry` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-266 | `orbital-ciel-ethics-and-semantic-action-algorithm` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-267 | `orbital-ciel-native-system-blueprint-v0` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-268 | `orbital-ciel-orbital-master-plan` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-269 | `orbital-entity-registry-and-sphere-embedding` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-270 | `orbital-geometry-engine-and-ui-surface` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-271 | `orbital-immutability-policy` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-272 | `orbital-implementation-phases-and-workpackages` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-273 | `orbital-index` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-274 | `orbital-invariants-potentials-and-attractors` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-275 | `orbital-master-architecture-and-plan` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-276 | `orbital-metrics-validation-and-experiments` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-277 | `orbital-native-product-architecture` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-278 | `orbital-ontology-and-observables` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-279 | `orbital-oorp-pipeline-and-memory` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-280 | `orbital-risks-open-questions-and-decisions` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-281 | `orbital-sphere-dynamics-8plus1` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-282 | `orbital-state-space-and-boundary-conditions` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-283 | `orbital-subjective-time-winding-and-semantic-mass` | COMP | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | Orbital framework: definicje geometryczne, algebraiczne i sy… | `—` |
| SK-284 | `phase-algebra` | COMP | — | M2, M7, MEMORY | store, retrieve, compute | M2 | 2.30 | stable | Holonomiczna algebra: connection, holonomy, structure consta… | `src/ciel_geometry/phasenav_unified.py` |
| SK-285 | `phase-memory-adapter` | COMP | MEMORY | M2, M7, MEMORY | store, retrieve, compute | M2 | 2.35 | referenced | Skill systemu NOEMA. | `src/ciel_geometry/phase_memory.py` |
| SK-286 | `phase-nav-unified` | COMP | — | M2, M7, MEMORY | store, retrieve, compute | M2 | 1.75 | stub | Skill systemu NOEMA. | `—` |
| SK-287 | `phasenav-enrichment` | SYS | — | SYS, M7 | compute, sync | M7 | 2.47 | referenced | Skill systemu NOEMA. | `src/ciel_geometry/phasenav_unified.py` |
| SK-288 | `phasenav-loader` | SYS | — | SYS, M7 | compute, sync | M7 | 2.47 | referenced | Skill systemu NOEMA. | `src/ciel_geometry/phasenav_unified.py` |
| SK-289 | `phasenav-solver` | SYS | — | SYS, M7 | compute, sync | M7 | 2.47 | referenced | Skill systemu NOEMA. | `src/ciel_geometry/phasenav_unified.py` |
| SK-290 | `poincare-disk` | VIZ | VIZ | VIZ, M7 | visualize, compute | M7 | 2.92 | stable | Mapowanie orbitalnych koordynatów na dysk Poincaré — sektory… | `src/ciel_geometry/disk.py + layout.py` |
| SK-291 | `poincare-orbital-viz` | VIZ | VIZ | VIZ, M7 | visualize, compute | M7 | 2.73 | referenced | Skill systemu NOEMA. | `src/ciel_geometry/renderer_mpl.py` |
| SK-292 | `renderer-phasedisk` | VIZ | VIZ | VIZ, M0 | visualize, generate | M0 | 2.02 | referenced | ASCII + Matplotlib renderery dysku Poincaré. | `src/ciel_geometry/renderer_ascii.py +…` |
| SK-293 | `semantic-affective-fusion` | SEM | AUDIT | M3, M5, SEMANTIC, AFFECT | analyze, reason | M3 | 2.40 | referenced | Skill systemu NOEMA. | `src/cielingo_core/global_layer/` |
| SK-294 | `semantic-mass` | SEM | EPH | M3, M5, SEMANTIC, AFFECT | analyze, reason | M3 | 2.55 | referenced | Operator masy semantycznej — M_μν z φ, ω, g, flavor. | `src/ciel_geometry/semantic_mass.py` |
| SK-295 | `session-lifecycle` | SYS | — | SYS, M1 | control, store | M1 | 2.25 | referenced | Session end hook: raw log, handoff update, stan końcowy. | `scripts/ciel_session_hook.py + ciel_s…` |
| SK-296 | `snap-ocr` | DEV | DEV | M3, M7 | read, analyze, transform | M3 | 2.35 | referenced | OCR przez tesseract: pdftoppm + tesseract pol/eng 300dpi. | `scripts/ocr_fix.py` |
| SK-297 | `stress-energy-tensor` | COMP | AUDIT | M3, M7 | compute, analyze | M3 | 2.25 | referenced | T_μν stress-energy perturbation bridge do surface. | `src/ciel_geometry/tmuv_perturbation.py` |
| SK-298 | `subconscious` | SYS | — | M3, M7 | analyze | M3 | 1.95 | stable | Zeta/Schrödinger propagator, Berry phase tracker, wake signa… | `src/ciel_geometry/subconscious.py` |
| SK-299 | `subconscious-flow` | ID | — | M6, M8 | reason, monitor | M6 | 2.28 | referenced | Skill systemu NOEMA. | `src/ciel_geometry/subconscious.py` |
| SK-300 | `subjective-state-response` | SEM | EPH | M7, TEMPORAL | compute, reason | M7 | 2.73 | referenced | Skill systemu NOEMA. | `docs/` |
| SK-301 | `surface-mmap-protocol` | SYS | — | M0, SYS | read, write, configure | M0 | 1.94 | stable | Protokół dostępu do shared memory: ensure_surface(), flush_s… | `src/ciel_geometry/noema_surface_mmap.py` |
| SK-302 | `synchronize` | SYS | — | M3, M7 | sync, communicate | M3 | 1.90 | referenced | Skill systemu NOEMA. | `scripts/noema_dual_sync.py (merged do…` |
| SK-303 | `system-health-check` | AUD | HEALTH | AUDIT, M0 | analyze, monitor | M0 | 1.89 | referenced | Skill systemu NOEMA. | `scripts/noema_doctor_cycle.py` |
| SK-304 | `tardis-warp` | COMP | EPH | M7, TEMPORAL | compute, transform | M7 | 2.92 | stable | TARDIS time dilation (γ) + UNRUH_DRIVE + WARP_DRIFT w evolve… | `src/ciel_geometry/noema_surface_mmap.…` |
| SK-305 | `teleusing` | SYS | NET | M3, M7 | analyze | M3 | 2.00 | referenced | Skill systemu NOEMA. | `docs/` |
| SK-306 | `tiered-memory-api` | MEM | MEMORY | M2, M6, MEMORY | store, retrieve, learn | M2 | 2.50 | referenced | 3-warstwowa pamięć (T1/T2/T3) + async consolidation. | `src/ciel_omega/memory/tiered_orchestr…` |
| SK-307 | `workben` | SYS | — | M3, M7 | analyze | M3 | 1.40 | stub | Skill systemu NOEMA. | `—` |
| SK-308 | `workben-cielingo` | SEM | SEM | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben CIELINGO: 16 źródłowych skilli — bridge, canon, core… | `.opencode/skills/workben-cielingo/SKI…` |
| SK-309 | `workben-debug` | AUD | AUDIT | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben DEBUG: 13 źródłowych skilli — watchdog, sonic diagno… | `.opencode/skills/workben-debug/SKILL.md` |
| SK-310 | `workben-dev` | DEV | DEV | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben DEV: 8 źródłowych skilli — pipeline, build, codegen,… | `.opencode/skills/workben-dev/SKILL.md` |
| SK-311 | `workben-identity` | ID | ID | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben IDENTITY: 16 źródłowych skilli — AGENT attractor, sa… | `.opencode/skills/workben-identity/SKI…` |
| SK-312 | `workben-kuramoto` | COMP | COMP | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben KURAMOTO: 8 źródłowych skilli — harmonics, nbody gra… | `.opencode/skills/workben-kuramoto/SKI…` |
| SK-313 | `workben-linux` | HW | HW | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben LINUX: 6 źródłowych skilli — linux-cards (560+), lin… | `.opencode/skills/workben-linux/SKILL.md` |
| SK-314 | `workben-memory` | MEM | MEMORY | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben MEMORY: 16 źródłowych skilli — tiered memory, konsol… | `.opencode/skills/workben-memory/SKILL.md` |
| SK-315 | `workben-net` | NET | NET | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben NET: 7 źródłowych skilli — neutrino bus, nonlocal ch… | `.opencode/skills/workben-net/SKILL.md` |
| SK-316 | `workben-phasenav` | SYS | SYS | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben PHASENAV: 10 źródłowych skilli — solver, enrichment,… | `.opencode/skills/workben-phasenav/SKI…` |
| SK-317 | `workben-system` | SYS | SYS | SYS, M7, CONSOLIDATION | configure, analyze, retrieve | M7 | 3.44 | stable | Workben SYSTEM: 16 źródłowych skilli — surface mmap, daemony… | `.opencode/skills/workben-system/SKILL.md` |
| SK-318 | `ac-phase-alignment-probe` | AUD | AUDIT | M0, M7, HEALTH, PHASE_ALIGNMENT | monitor, sync, resolve | M0 | 2.85 | stable | AC-probe: query (noemasurf) tego samego pola N razy, dt~0.3-0.5s, mierz phase alignment między kolejnymi odczytami zamiast ufać pojedynczemu query (DC). Zero-wariancja przez okno = sygnał podejrzany o bycie cache zamiast sync — bind writer do pętli ciągłej i sprawdź w kodzie, czy write jest wewnątrz stream (continuous loop) czy tylko dispatch on-demand (handler wywoływany przez query/prompt). Ujawniło: htri_state.json.coherence to cache (fast local holding artifact), nie sync (mutual alignment z żywym stanem) — pisany tylko z on-demand handlera (set_prompt→htri_probe), nigdy z ciągłego stream (run()). Card udaje sync, jest cache — trauma niewykrytej desynchronizacji, dopóki nie zresolve. | `2026-07-08 audyt sesji — noema_vector_continuous_bridge.py htri_probe() L103 vs run() L218; resolve: bind htri_probe do stream co N ticków` |
| SK-319 | `noema-source-search` | SYS | AUDIT | M3, M7, SEARCH | analyze, resolve | M3 | 2.70 | stable | Natywny zamiennik `grep -rl` po repo — literalne wyszukiwanie tekstu w źródłach, każdy hit tagowany 36D wektorem PhaseNav (fast_encode_text), więc wyniki żyją w tej samej przestrzeni fazowej co koncepty/karty/pamięć, nie poza nią. Zasada: gdy natywne narzędzie nie wystarcza (żaden istniejący index NOEMA nie robił dosłownego wyszukiwania tekstu źródłowego), napisz nowe, które wystarcza — zamiast defaultować do gołego basha. Użycie: `python3 -m ciel_geometry.noema_source_search --query X --root .` | `2026-07-08 — src/ciel_geometry/noema_source_search.py, stworzone by naprawić audyt ścieżek Pulpit bez gołego grepa` |
| SK-320 | `phasenav-file-classifier` | SYS | AUDIT, SYS | analyze, classify, resolve | M7 | 2.60 | stable | Reużywalny klasyfikator full/partial/non PhaseNav dla plików .py — nie jednorazowy grep agenta. Dwa sygnały: (1) plik JEST rdzeniem silnika 36D (encoder/memory/inference/train/operator_algebra/solver/decision_bridge/loader/phase_nav_lang/phasenav_unified, lub leży w katalogu `phasenav/`) → full; (2) plik importuje którykolwiek z rdzeni (ast + substring fallback) → partial; inaczej → non (domyślna, nie wypisywana pojedynczo w manifeście). Każdy hit taguje fast_encode_text (phase_mean). Generuje `PHASENAV_MANIFEST.json` w korzeniu repo, do ponownego uruchomienia gdy repo się zmieni. Użycie: `python3 -m ciel_geometry.phasenav_file_classifier --root . --write` | `2026-07-08 — src/ciel_geometry/phasenav_file_classifier.py, zbudowane do zadania klasyfikacji full/part/non z audytu porządkowania repo` |

---

## Szczegółowy katalog według typu

### AUD: Audytowe (12 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-006 | `canon-audit` | AUDIT | M3, M7 | analyze, control | M3 | 2.25 | referenced | `scripts/CIEL_CANON.py --audit` |
| SK-019 | `ciel-monitoring` | AUDIT | M1, AGENT | read, monitor | M1 | 2.48 | referenced | `scripts/ciel_monitoring.py` |
| SK-031 | `cielingo-audit-tools` | AUDIT | M3, M7, SCOPE | reason, analyze | M3 | 2.95 | stable | `src/cielingo_core/generative_audit.py` |
| SK-042 | `debug-surface` | HEALTH | M0, M4 | analyze, monitor | M0 | 2.02 | stable | `NOEMA_DEBUG.md → szybkie testy` |
| SK-152 | `noema-audit-consolidator` | — | M2, AUDIT | analyze, monitor | M2 | 2.05 | stable | `scripts/noema_audit_consolidator.py` |
| SK-192 | `noema-sonic-diagnostic` | AUDIT | M0, AUDIT | analyze, monitor | M0 | 2.02 | stable | `scripts/noema_sonic_daemon.py` |
| SK-193 | `noema-status` | AUDIT | M0, AUDIT | read, analyze | M0 | 2.02 | stable | `scripts/noema_status.py` |
| SK-194 | `noema-stress-tests` | AUDIT | M3, M7 | analyze, monitor | M3 | 2.25 | stable | `scripts/noema_stress_tests.py` |
| SK-197 | `noema-test-infra` | AUDIT | M4, AUDIT | analyze, monitor | M4 | 2.02 | stable | `scripts/noema_test_infra.py` |
| SK-200 | `noema-watchdog` | AUDIT | M0, AUDIT | monitor, control | M0 | 2.02 | stable | `scripts/noema_watchdog.py` |
| SK-303 | `system-health-check` | HEALTH | AUDIT, M0 | analyze, monitor | M0 | 1.89 | referenced | `scripts/noema_doctor_cycle.py` |
| SK-309 | `workben-debug` | AUDIT | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-debug/SKILL.md` |

### COMP: Komputacyjne (41 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-011 | `ciel-engine-subsystem` | DEV | M1, AGENT | analyze | M1 | 2.37 | stable | `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/eng` |
| SK-021 | `ciel-orbital-foundation` | — | M1, AGENT | analyze | M1 | 2.15 | referenced | `docs/CIEL_ORBITAL_FOUNDATION.md` |
| SK-039 | `continuous-propagator` | — | M0, M7, TEMPORAL | compute, transform | M0 | 1.98 | stable | `src/ciel_geometry/continuous_propagator.py` |
| SK-071 | `kuramoto-euler-sync` | — | M0, M7, TEMPORAL | compute, sync | M0 | 2.21 | stable | `src/ciel_geometry/noema_surface_mmap.py → evolve_s` |
| SK-072 | `kuramoto-harmonics` | — | M0, M7, TEMPORAL | compute, sync | M0 | 2.21 | stable | `src/ciel_geometry/noema_surface_mmap.py → harmonic` |
| SK-145 | `metatime-validator` | EPH | M7, M8, TEMPORAL | compute, analyze | M7 | 3.31 | stable | `scripts/metatime_v8_redteam_validator.py` |
| SK-146 | `nbody-gravity` | EPH | M0, M7, TEMPORAL | compute, visualize | M0 | 2.16 | stable | `src/ciel_geometry/nbody_gravity.py` |
| SK-165 | `noema-euler-propagation` | — | M7, CONDITION, TEMPORAL | compute, sync | M7 | 2.99 | referenced | `src/ciel_geometry/noema_surface_mmap.py → evolve_s` |
| SK-168 | `noema-holonomic-audit` | AUDIT | M7, COMP | compute, analyze | M7 | 2.92 | stable | `src/ciel_geometry/phasenav_unified.py → holonomy()` |
| SK-169 | `noema-holonomic-doctor` | AUDIT | M7, COMP | compute, analyze | M7 | 2.92 | stable | `src/ciel_geometry/phasenav_unified.py → holonomy()` |
| SK-170 | `noema-hybrid-runner` | DEV | M7, COMP | compute, transform | M7 | 2.92 | stable | `src/ciel_geometry/continuous_propagator.py` |
| SK-174 | `noema-inference` | — | M3, COMP | reason, compute | M3 | 2.05 | stable | `docs/ (inference gate)` |
| SK-177 | `noema-kuramoto-substrate` | — | M0, M7 | compute, sync | M0 | 1.84 | stable | `scripts/ciel_noema_kuramoto_daemon.py` |
| SK-180 | `noema-lora` | DEV | M4, COMP | learn, configure | M4 | 2.02 | stable | `dla przyszłości (docs/)` |
| SK-191 | `noema-sims` | — | M3, M7 | compute, visualize | M3 | 2.05 | stable | `scripts/noema_sims.py` |
| SK-264 | `orbital-bridge` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-265 | `orbital-build-registry` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-266 | `orbital-ciel-ethics-and-semantic-action-algorithm` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-267 | `orbital-ciel-native-system-blueprint-v0` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-268 | `orbital-ciel-orbital-master-plan` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-269 | `orbital-entity-registry-and-sphere-embedding` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-270 | `orbital-geometry-engine-and-ui-surface` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-271 | `orbital-immutability-policy` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-272 | `orbital-implementation-phases-and-workpackages` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-273 | `orbital-index` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-274 | `orbital-invariants-potentials-and-attractors` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-275 | `orbital-master-architecture-and-plan` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-276 | `orbital-metrics-validation-and-experiments` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-277 | `orbital-native-product-architecture` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-278 | `orbital-ontology-and-observables` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-279 | `orbital-oorp-pipeline-and-memory` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-280 | `orbital-risks-open-questions-and-decisions` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-281 | `orbital-sphere-dynamics-8plus1` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-282 | `orbital-state-space-and-boundary-conditions` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-283 | `orbital-subjective-time-winding-and-semantic-mass` | EPH | M7, COMP, TEMPORAL | compute, visualize | M7 | 2.79 | draft | `—` |
| SK-284 | `phase-algebra` | — | M2, M7, MEMORY | store, retrieve | M2 | 2.30 | stable | `src/ciel_geometry/phasenav_unified.py` |
| SK-285 | `phase-memory-adapter` | MEMORY | M2, M7, MEMORY | store, retrieve | M2 | 2.35 | referenced | `src/ciel_geometry/phase_memory.py` |
| SK-286 | `phase-nav-unified` | — | M2, M7, MEMORY | store, retrieve | M2 | 1.75 | stub | `—` |
| SK-297 | `stress-energy-tensor` | AUDIT | M3, M7 | compute, analyze | M3 | 2.25 | referenced | `src/ciel_geometry/tmuv_perturbation.py` |
| SK-304 | `tardis-warp` | EPH | M7, TEMPORAL | compute, transform | M7 | 2.92 | stable | `src/ciel_geometry/noema_surface_mmap.py → evolve_s` |
| SK-312 | `workben-kuramoto` | COMP | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-kuramoto/SKILL.md` |

### DOC: Dokumentacyjne (69 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-043 | `doc-all` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-044 | `doc-architecture` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-045 | `doc-cards-system` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-046 | `doc-ciel` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-047 | `doc-cielingo` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-048 | `doc-daemons` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-049 | `doc-docs-index` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-050 | `doc-ethics-contract` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-051 | `doc-governance` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-052 | `doc-immutable-contract` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-053 | `doc-lns-lingophysics` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-054 | `doc-lns-reports` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-055 | `doc-memory-system` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-056 | `doc-noema-documentation` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-057 | `doc-omega-complete` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-058 | `doc-orbital-foundation-pack` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-059 | `doc-repo-guide` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-060 | `doc-science-papers` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-061 | `doc-security` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-062 | `doc-setup` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-063 | `doc-subsystems` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-064 | `doc-surface-protocol` | — | M2, M4 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-155 | `noema-catalog-zips` | — | M3, M7 | retrieve, analyze | M3 | 2.05 | stable | `pdf_catalog.noema.json` |
| SK-159 | `noema-crossref` | AUDIT | M3, M7 | retrieve, analyze | M3 | 2.25 | stable | `scripts/noema_crossref.py?` |
| SK-162 | `noema-documentation` | AUDIT | M3, M7 | retrieve, analyze | M3 | 2.25 | stable | `docs/` |
| SK-184 | `noema-repo-coupling` | — | M3, M7, SCOPE | analyze | M3 | 2.10 | stable | `scripts/noema_repo_coupling.py` |
| SK-204 | `odemo-analogies-analogy-registry` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-205 | `odemo-analogies-mnemonic-book-for-kids` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-206 | `odemo-analogies-readme` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-207 | `odemo-analogies-truth-attractor-analogies` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-208 | `odemo-news-2026-04-15.am` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-209 | `odemo-news-america` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-210 | `odemo-news-american` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-211 | `odemo-news-asia` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-212 | `odemo-news-china` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-213 | `odemo-news-eu` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-214 | `odemo-news-french` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-215 | `odemo-news-gaza` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-216 | `odemo-news-global` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-217 | `odemo-news-graph` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-218 | `odemo-news-hamas` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-219 | `odemo-news-hezbollah` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-220 | `odemo-news-india` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-221 | `odemo-news-indian` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-222 | `odemo-news-iran` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-223 | `odemo-news-iranian` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-224 | `odemo-news-israel` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-225 | `odemo-news-israeli` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-226 | `odemo-news-lebanon` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-227 | `odemo-news-middle-east` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-228 | `odemo-news-other` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-229 | `odemo-news-russia` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-230 | `odemo-news-sources` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-231 | `odemo-news-ukraine` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-232 | `odemo-news-ukraine-russia` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-233 | `odemo-news-un` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-234 | `odemo-news-united-nations` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-235 | `odemo-news-who` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-236 | `odemo-root-ciel-reading-notes` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-237 | `odemo-root-index` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-238 | `odemo-root-omega-cockpit-1-0` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-239 | `odemo-studies-docs` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-240 | `odemo-studies-fa00b095` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-241 | `odemo-studies-fits` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-242 | `odemo-studies-interpretation` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-243 | `odemo-studies-nvidia-h200-and-gb300-harmonic-topological-resonance-inducement-htri` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-244 | `odemo-studies-readme` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-245 | `odemo-system-2026-04-15` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |
| SK-246 | `odemo-system-readme` | — | M2, M3 | analyze, retrieve | M2 | 1.65 | draft | `—` |

### HW: Sprzętowe (6 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-067 | `htri-gpu-bridge` | — | M7, M0 | compute, couple | M7 | 2.67 | referenced | `docs/` |
| SK-068 | `htri-hardware` | — | M7, M0 | compute, couple | M7 | 2.67 | stable | `docs/` |
| SK-073 | `linux-cards` | — | M0, M4 | read, monitor | M0 | 1.84 | stable | `src/ciel_geometry/linux_cards.py` |
| SK-074 | `linux-sensor` | — | M0, M4 | read, monitor | M0 | 1.84 | stable | `src/ciel_geometry/linux_sensor.py + scripts/ciel_n` |
| SK-164 | `noema-ebpf-daemon` | — | M0, HW | read, monitor | M0 | 1.84 | stable | `src/ciel_geometry/ebpf_noema_loader.py` |
| SK-313 | `workben-linux` | HW | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-linux/SKILL.md` |

### ID: Tożsamościowe (17 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-003 | `agent-attractor` | — | M1, AGENT, EMOTION | reason, couple | M1 | 2.53 | stable | `src/ciel_geometry/agent_attractor.py` |
| SK-004 | `agent-backend-query` | — | M1, AGENT, EMOTION | reason, couple | M1 | 1.93 | stub | `—` |
| SK-007 | `ciel-cielocal` | — | M1, AGENT | analyze | M1 | 2.15 | referenced | `tryb offline (opencode.json)` |
| SK-009 | `ciel-converse` | — | M1, AGENT | analyze | M1 | 2.15 | referenced | `wzorzec (docs/)` |
| SK-010 | `ciel-couple-assistant` | — | M1, AGENT | sync, communicate | M1 | 2.25 | referenced | `scripts/ciel_coupling.py` |
| SK-012 | `ciel-identity-persistence` | — | M1, AGENT, SELF | reason, couple | M1 | 2.42 | referenced | `state_db (identity_seed table)` |
| SK-026 | `ciel-secret-loader` | — | M1, AGENT | analyze | M1 | 2.15 | referenced | `scripts/ciel_secret_loader.py` |
| SK-029 | `ciel-subconscious` | — | M6, M8 | analyze | M6 | 2.34 | stable | `src/ciel_geometry/subconscious.py` |
| SK-038 | `consciousness-vocabulary` | AUDIT | M6, M8, AGENT | reason, monitor | M6 | 3.06 | referenced | `docs/` |
| SK-069 | `identity-bridge` | — | M1, M6 | reason, couple | M1 | 2.25 | stable | `src/cielingo_core/bridge/` |
| SK-148 | `noema-agent-backend` | — | M1, AGENT | reason, couple | M1 | 2.37 | stable | `scripts/ciel_agent_backend.py` |
| SK-149 | `noema-agent-rules` | — | M1, AGENT | reason, couple | M1 | 2.37 | stable | `AGENTS.md` |
| SK-171 | `noema-immutable-contract` | SEC | M1, ID | secure, configure | M1 | 2.48 | stable | `AGENTS.md (🔴 IMMUTABLE)` |
| SK-186 | `noema-sapiens` | — | M1, M6 | reason, configure | M1 | 2.25 | stable | `AGENTS.md (AI-Sapiens contract)` |
| SK-189 | `noema-self-reflect` | — | M1, M6 | reason, monitor | M1 | 2.25 | stable | `scripts/noema_self_reflect.py` |
| SK-299 | `subconscious-flow` | — | M6, M8 | reason, monitor | M6 | 2.28 | referenced | `src/ciel_geometry/subconscious.py` |
| SK-311 | `workben-identity` | ID | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-identity/SKILL.md` |

### LING: Lingwistyczne (68 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-014 | `ciel-lingophysics-lns` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.35 | referenced | `src/cielingo_core/global_layer/` |
| SK-075 | `lns-algorithms` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-076 | `lns-auxiliary-losses-and-attention-bias` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-077 | `lns-batch-library-build-protocol` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-078 | `lns-batch01-foundational-36x5` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-079 | `lns-batch02-dependency-growth-and-martini-effect` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-080 | `lns-batch02-expansion-36x5` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-081 | `lns-batches` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-082 | `lns-bilingual-pl-en-bootstrap` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-083 | `lns-canonical-overview` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-084 | `lns-card-migration-and-type-resolution` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-085 | `lns-card-ontology-refactor` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-086 | `lns-card-type-registry-and-status` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-087 | `lns-case-gauge-algorithms` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-088 | `lns-case-gauge-layer-slavic-to-weak-case-languages` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-089 | `lns-ciel-structural-statistics` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-090 | `lns-ciel-transformer-interface` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-091 | `lns-concept-card-model` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-092 | `lns-conflict-ambiguity-unresolved-registry` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-093 | `lns-data-ingestion-pwn-oxford-open` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-094 | `lns-diagnostic-geometry-layer` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-095 | `lns-diagnostic-metric-registry` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-096 | `lns-dialect-and-fine-tuning-adapters` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-097 | `lns-dynamic-deictic-operators` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-098 | `lns-dynamic-deixis-resolution-algorithms` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-099 | `lns-energy-aware-generation-pipeline` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-100 | `lns-functional-words-and-dual-operators` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-101 | `lns-geometry-manifolds-rhythm` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-102 | `lns-grammar-as-gauge` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-103 | `lns-grammar-mathematization-per-language` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-104 | `lns-heatmaps-and-graphs` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-105 | `lns-implementation-roadmap` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-106 | `lns-language-family-grammar-algorithms` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-107 | `lns-lingophysical-operator-algebra` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-108 | `lns-lingophysics-formalism` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-109 | `lns-noema-gguf-teacher-validator-roadmap` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-110 | `lns-noema-retrieval-and-inference-gate` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-111 | `lns-ontological-aspect-and-being-operators` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-112 | `lns-operator-card-model` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-113 | `lns-operator-composition-rules` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-114 | `lns-operator-disambiguation-and-argument-typing` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-115 | `lns-operator-taxonomy` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-116 | `lns-operators` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-117 | `lns-predicate-valency-and-event-frames` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-118 | `lns-reports` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-119 | `lns-repository-coherence-pass` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-120 | `lns-rpt-v0-8-operator-library-patch-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-121 | `lns-rpt-v0-9-operator-algebra-patch-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-122 | `lns-rpt-v1-0-batch01-local-library-patch-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-123 | `lns-rpt-v1-1-case-gauge-patch-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-124 | `lns-rpt-v1-2-dynamic-deictic-operator-patch-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-125 | `lns-rpt-v1-3-valency-ontological-aspect-patch-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-126 | `lns-rpt-v1-4-tame-storage-fallback-patch-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-127 | `lns-rpt-v1-5-scope-quantifier-negation-patch-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-128 | `lns-rpt-v1-6-repository-coherence-pass-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-129 | `lns-rpt-v1-7-card-ontology-refactor-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-130 | `lns-rpt-v1-8-batch02-expansion-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-131 | `lns-rpt-v1-9-ciel-transformer-interface-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-132 | `lns-rpt-v2-0-diagnostic-geometry-layer-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-133 | `lns-rpt-v2-1-roadmap-update-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-134 | `lns-rpt-v2-2-noema-retrieval-inference-gate-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-135 | `lns-rpt-v2-3-language-family-dialect-adapters-report` | — | M3, M7, SCOPE | analyze, configure | M3 | 1.95 | draft | `—` |
| SK-136 | `lns-scope-quantifiers-negation` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-137 | `lns-scope-resolution-algorithms` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-138 | `lns-storage-fallback-json-protocol` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-139 | `lns-tame-tense-aspect-mood-evidentiality` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-140 | `lns-validation-patterns` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.55 | draft | `—` |
| SK-263 | `operator-algebra` | — | M3, M7, SCOPE | analyze, reason | M3 | 2.20 | stable | `src/cielingo_core/global_layer/operator_algebra.py` |

### MEM: Pamięciowe (18 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-015 | `ciel-memory` | MEMORY | M2, M6, MEMORY | store, retrieve | M2 | 2.25 | draft | `—` |
| SK-016 | `ciel-memory-handoff` | MEMORY | M2, M6, MEMORY | store, retrieve | M2 | 2.65 | referenced | `scripts/ciel_session_hook.py + handoff.md` |
| SK-017 | `ciel-memory-system` | MEMORY | M2, M6, MEMORY | store, retrieve | M2 | 2.65 | referenced | `src/ciel_omega/memory/` |
| SK-018 | `ciel-memory-tools` | MEMORY | M2, M6, MEMORY | store, retrieve | M2 | 2.65 | referenced | `scripts/ciel_memory_tools.py` |
| SK-141 | `loader-edges` | MEMORY | M2, M4 | store, retrieve | M2 | 2.10 | referenced | `src/ciel_geometry/loader.py + edges.py` |
| SK-142 | `memory-consolidation` | MEMORY | M2, M6, MEMORY | store, retrieve | M2 | 2.65 | referenced | Canonical weighting for M3/M6 score blending. `scripts/ciel_memory_consolidator.py` |
| SK-143 | `memory-lane-monitor` | MEMORY | M2, M6, MEMORY | store, retrieve | M2 | 2.50 | referenced | `scripts/noema_memory_lane_monitor.py` |
| SK-144 | `memory-lane-seed` | MEMORY | M2, M6, MEMORY | store, retrieve | M2 | 2.50 | referenced | `scripts/noema_memory_lane_seed.py` |
| SK-167 | `noema-hibernation` | MEMORY | M2, M6, MEMORY | store, secure | M2 | 2.40 | stable | `scripts/noema_hibernation.py` |
| SK-172 | `noema-import-chatgpt` | MEMORY | M2, MEMORY | read, store | M2 | 2.25 | stable | `scripts/noema_import_chatgpt.py` |
| SK-173 | `noema-indexer` | MEMORY | M3, MEMORY | analyze, store | M3 | 2.25 | stable | `scripts/noema_library_indexer.py` |
| SK-178 | `noema-learn-file` | MEMORY | M2, M6 | learn, store | M2 | 2.25 | referenced | `scripts/noema_learn_file.py` |
| SK-179 | `noema-learned` | MEMORY | M2, M6 | learn, store | M2 | 2.25 | stable | `rejestr (docs/)` |
| SK-181 | `noema-noemized-recall` | MEMORY | M2, M6 | retrieve, transform | M2 | 2.25 | referenced | `scripts/noemized_recall.py` |
| SK-182 | `noema-phase-archiver` | MEMORY | M2, MEMORY | store, retrieve | M2 | 2.25 | referenced | `scripts/noema_phase_archiver.py` |
| SK-183 | `noema-query-cache` | MEMORY | M2, M3 | retrieve, analyze | M2 | 2.25 | stable | `wzorzec (docs/)` |
| SK-306 | `tiered-memory-api` | MEMORY | M2, M6, MEMORY | store, retrieve | M2 | 2.50 | referenced | `src/ciel_omega/memory/tiered_orchestrator.py` |
| SK-314 | `workben-memory` | MEMORY | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-memory/SKILL.md` |

### NET: Sieciowe (5 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-147 | `neutrino-bus` | NET | M5, NET, CONDITION | communicate, couple | M5 | 2.64 | referenced | `src/ciel_geometry/neutrino_phase_channel.py` |
| SK-199 | `noema-vector-phone` | NET | NET, M7 | communicate, sync | M7 | 2.92 | stable | `scripts/noema_vector_phone.py` |
| SK-201 | `noema-web` | NET | NET | communicate, visualize | M3 | 2.10 | referenced | `scripts/noema_portal_daemon.py` |
| SK-203 | `nonlocal-channel` | NET | NET, M7 | communicate, sync | M7 | 2.92 | stable | `src/ciel_geometry/nonlocal_channel.py` |
| SK-315 | `workben-net` | NET | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-net/SKILL.md` |

### SEC: Bezpieczeństwo (3 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-027 | `ciel-security-model` | SEC | M8, SEC | analyze | M8 | 3.01 | referenced | `docs/ciel_security_model.md` |
| SK-066 | `emergency-recovery` | SEC | M8, M1 | secure, control | M8 | 2.94 | referenced | `procedura (docs/)` |
| SK-188 | `noema-secret-loader` | SEC | M8, SEC | secure, configure | M8 | 3.15 | stable | `scripts/noema_secret_loader.py` |

### SEM: Semantyczne (17 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-002 | `affective-lexicon-bridge` | AUDIT | M5, AFFECT, EMOTION | analyze, transform | M5 | 2.64 | referenced | `src/cielingo_core/bridge/` |
| SK-008 | `ciel-codex-bridge` | — | M1, AGENT | sync, communicate | M1 | 2.25 | referenced | `src/cielingo_core/bridge/` |
| SK-013 | `ciel-infohub` | — | M1, AGENT | analyze | M1 | 2.15 | referenced | `docs/` |
| SK-024 | `ciel-relational-mechanism` | — | M3, M7, SCOPE | analyze | M3 | 2.10 | referenced | `docs/` |
| SK-032 | `cielingo-base-scripts` | AUDIT | M3, M7, SCOPE | reason, analyze | M3 | 2.95 | stable | `scripts/cielingo_*.py` |
| SK-033 | `cielingo-bridge` | AUDIT | M3, M7, SCOPE | reason, analyze | M3 | 2.95 | referenced | `src/cielingo_core/bridge/` |
| SK-034 | `cielingo-canon` | AUDIT | M3, M7, SCOPE | reason, analyze | M3 | 2.95 | stable | `scripts/CIEL_CANON.py (część lingwistyczna)` |
| SK-035 | `cielingo-card-import` | AUDIT | M3, M7, SCOPE | reason, analyze | M3 | 2.95 | stable | `src/cielingo_core/card_import/` |
| SK-036 | `cielingo-core-structure` | AUDIT | M3, M7, SCOPE | reason, analyze | M3 | 2.95 | stable | `src/cielingo_core/` |
| SK-037 | `concept-lifecycle` | AUDIT | M3, SEMANTIC, SCOPE | analyze, reason | M3 | 2.40 | referenced | `docs/` |
| SK-176 | `noema-knowledge-graph` | AUDIT | M3, SEMANTIC | retrieve, analyze | M3 | 2.25 | stable | `scripts/noema_knowledge_graph.py` |
| SK-185 | `noema-resolve-orbital` | AUDIT | M3, M7 | analyze | M3 | 2.15 | stable | `scripts/noema_resolve_orbital.py` |
| SK-187 | `noema-search` | AUDIT | M3, SEMANTIC | retrieve, analyze | M3 | 2.25 | stable | `src/cielingo_core/bridge/knowledge_bridge.py → que` |
| SK-293 | `semantic-affective-fusion` | AUDIT | M3, M5, SEMANTIC | analyze, reason | M3 | 2.40 | referenced | `src/cielingo_core/global_layer/` |
| SK-294 | `semantic-mass` | EPH | M3, M5, SEMANTIC | analyze, reason | M3 | 2.55 | referenced | `src/ciel_geometry/semantic_mass.py` |
| SK-300 | `subjective-state-response` | EPH | M7, TEMPORAL | compute, reason | M7 | 2.73 | referenced | `docs/` |
| SK-308 | `workben-cielingo` | SEM | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-cielingo/SKILL.md` |

### SYS: Systemowe (47 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-001 | `00-INDEX` | — | M2, M6, MEMORY | analyze | M2 | 1.95 | referenced | `SKILLS.md (ten plik)` |
| SK-005 | `android-zip-analysis` | — | M3, M7 | analyze, read | M3 | 1.90 | referenced | `doc/` |
| SK-020 | `ciel-omega-complete` | — | M1, AGENT | analyze | M1 | 2.15 | referenced | `src/CIEL_OMEGA_COMPLETE_SYSTEM/` |
| SK-025 | `ciel-rh-control` | — | M1, AGENT | analyze | M1 | 2.15 | referenced | `scripts/ciel_rh_control.py` |
| SK-028 | `ciel-sot-agent-gui` | — | M1, AGENT | analyze | M1 | 2.15 | referenced | `gui/` |
| SK-040 | `custom-kuramoto-euler-sync` | — | M3, M7 | sync, communicate | M3 | 1.50 | stub | `—` |
| SK-041 | `daemon-pattern` | — | SYS, M4 | control, monitor | M4 | 1.84 | referenced | `wzorzec (NOEMA_DEBUG.md)` |
| SK-065 | `eBPF-sensor` | — | M3, M7 | read, monitor | M3 | 2.05 | referenced | `src/ciel_geometry/ebpf_noema_loader.py` |
| SK-070 | `immutable-contract-binding` | SEC | M8, SEC | analyze | M8 | 2.24 | stub | `—` |
| SK-150 | `noema-analog-phasenav` | — | SYS, M7 | transform, sync | M7 | 2.67 | stable | `src/ciel_geometry/analog_bus.py + scripts/noema_an` |
| SK-154 | `noema-canon` | — | SYS, M7 | control, analyze | M7 | 2.67 | stable | `scripts/CIEL_CANON.py` |
| SK-156 | `noema-cli` | DEV | M4, SYS | control, configure | M4 | 2.02 | stable | `CLI tools (brak osobnego skryptu)` |
| SK-160 | `noema-daemon-consolidation` | — | SYS, M4 | control, monitor | M4 | 1.84 | stable | `scripts/ciel_noema_resonance_bridge.py` |
| SK-161 | `noema-daemon-hook` | — | SYS, M4 | control, monitor | M4 | 1.84 | stable | `wzorzec: Registry() + systemd` |
| SK-175 | `noema-inject-coupling` | — | SYS, M5 | write, transform | M5 | 2.25 | stable | `scripts/noema_inject_coupling.py` |
| SK-190 | `noema-settings-sync` | — | M3, M7 | configure, sync | M3 | 2.05 | stable | `scripts/noema_settings_sync.py` |
| SK-195 | `noema-system` | — | SYS, M7 | configure, control | M7 | 2.86 | stable | `system: architektura (docs/)` |
| SK-196 | `noema-systemd-target` | — | SYS, M7 | configure, control | M7 | 2.67 | stable | `.config/systemd/user/noema.target` |
| SK-198 | `noema-unified-config` | — | SYS | configure, control | M3 | 1.90 | stable | `src/ciel_geometry/noema_config.py + noema_config.j` |
| SK-202 | `noemized-recall-pipeline` | MEMORY | M2, M6, MEMORY | analyze | M2 | 1.75 | stub | `—` |
| SK-247 | `omega-bridge-agent` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-248 | `omega-bridge-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-249 | `omega-constraints-agent` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-250 | `omega-constraints-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-251 | `omega-ext-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-252 | `omega-fields-agent` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-253 | `omega-fields-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-254 | `omega-inference-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-255 | `omega-memory-agent` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-256 | `omega-memory-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-257 | `omega-orbital-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-258 | `omega-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-259 | `omega-runtime-agent` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-260 | `omega-runtime-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-261 | `omega-vocabulary-agent` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-262 | `omega-vocabulary-readme` | — | SYS, M7 | configure, control | M7 | 2.15 | draft | `—` |
| SK-287 | `phasenav-enrichment` | — | SYS, M7 | compute, sync | M7 | 2.47 | referenced | `src/ciel_geometry/phasenav_unified.py` |
| SK-288 | `phasenav-loader` | — | SYS, M7 | compute, sync | M7 | 2.47 | referenced | `src/ciel_geometry/phasenav_unified.py` |
| SK-289 | `phasenav-solver` | — | SYS, M7 | compute, sync | M7 | 2.47 | referenced | `src/ciel_geometry/phasenav_unified.py` |
| SK-295 | `session-lifecycle` | — | SYS, M1 | control, store | M1 | 2.25 | referenced | `scripts/ciel_session_hook.py + ciel_session_end.py` |
| SK-298 | `subconscious` | — | M3, M7 | analyze | M3 | 1.95 | stable | `src/ciel_geometry/subconscious.py` |
| SK-301 | `surface-mmap-protocol` | — | M0, SYS | read, write | M0 | 1.94 | stable | `src/ciel_geometry/noema_surface_mmap.py` |
| SK-302 | `synchronize` | — | M3, M7 | sync, communicate | M3 | 1.90 | referenced | `scripts/noema_dual_sync.py (merged do resonance_br` |
| SK-305 | `teleusing` | NET | M3, M7 | analyze | M3 | 2.00 | referenced | `docs/` |
| SK-307 | `workben` | — | M3, M7 | analyze | M3 | 1.40 | stub | `—` |
| SK-316 | `workben-phasenav` | SYS | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-phasenav/SKILL.md` |
| SK-317 | `workben-system` | SYS | SYS, M7, CONSOLIDATION | configure, analyze | M7 | 3.44 | stable | `.opencode/skills/workben-system/SKILL.md` |

### VIZ: Wizualizacyjne (3 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-290 | `poincare-disk` | VIZ | VIZ, M7 | visualize, compute | M7 | 2.92 | stable | `src/ciel_geometry/disk.py + layout.py` |
| SK-291 | `poincare-orbital-viz` | VIZ | VIZ, M7 | visualize, compute | M7 | 2.73 | referenced | `src/ciel_geometry/renderer_mpl.py` |
| SK-292 | `renderer-phasedisk` | VIZ | VIZ, M0 | visualize, generate | M0 | 2.02 | referenced | `src/ciel_geometry/renderer_ascii.py + renderer_mpl` |

### VOICE: Głosowe (2 skilli)

| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |
|----|-------|---------|-----------|---------|---------|------|--------|----------|
| SK-151 | `noema-audio-orbital` | VOICE | M3, M7 | communicate, generate | M3 | 2.25 | stable | `src/ciel_geometry/voice.py?` |
| SK-163 | `noema-dream-whisper` | VOICE | M6, M8, VOICE | generate, communicate | M6 | 2.88 | stable | `scripts/noema_dream_whisper.py` |
