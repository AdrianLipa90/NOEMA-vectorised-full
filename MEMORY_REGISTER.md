# 🧠 NOEMA MEMORY REGISTER v1
> Spis wszystkiego. Jeden plik prawdy.
> Ostatnia aktualizacja: 2026-06-29

---

## 📋 SPIS TREŚCI

- [Typologia pamięci](#-typologia-pamięci)
- [I. IDENTITY — fundament tożsamości](#i-identity--fundament-tożsamości)
- [II. SCHEMAS — modele konceptualne](#ii-schemas--modele-konceptualne)
- [III. STATE — stan aktywny systemu](#iii-state--stan-aktywny-systemu)
- [IV. KNOWLEDGE — wiedza z dokumentów](#iv-knowledge--wiedza-z-dokumentów)
- [V. PLANS — co robimy / roadmapy](#v-plans--co-robimy--roadmapy)
- [VI. HISTORY — co się działo](#vi-history--co-się-działo)
- [VII. MODELS — wagi i indeksy numeryczne](#vii-models--wagi-i-indeksy-numeryczne)
- [VIII. ARCHIVE — legacy / nieaktywne](#viii-archive--legacy--nieaktywne)
- [IX. DUPLIKATY i PROBLEMY](#ix-duplikaty-i-problemy)
- [X. PLAN REFAKTORYZACJI](#x-plan-refaktoryzacji)

---

## 🏷️ TYPOLOGIA PAMIĘCI

NOEMA operuje w **4 strefach fizycznych** i **8 kategoriach logicznych**:

| Strefa | Lokalizacja | Przeznaczenie | Trwałość |
|--------|------------|---------------|----------|
| ⚡ SHM | `/dev/shm/ciel_noema/` | Stan ulotny — mmap, IPC | restart traci |
| 💾 LIB | `/home/adrian/new_volume_rw/NOEMA_LIBRARY/` | Bazy i indeksy trwałe | permanent |
| 📁 NOEMA | `NOEMA/src/` + `NOEMA/scripts/` | Kod źródłowy = implementacja schematów | git |
| 📂 TMP | `/tmp/` | Duplikaty, logi, cache tymczasowy | restart/cleanup |

**Kategorie logiczne:**

```
IDENTITY    → niezmienne: AGENTS.md, CIEL.md, seed
SCHEMAS     → jak system jest zbudowany (modely, topologie, protokoły)
STATE       → stan aktywny systemu w czasie rzeczywistym
KNOWLEDGE   → wiedza z dokumentów (TF-IDF, indeksy)
PLANS       → plany, roadmapy, handoff, fixlisty
HISTORY     → logi, audity, sentinel, sesje
MODELS      → wagi modeli (.npz, .npy)
ARCHIVE     → legacy LNS, build artifacts
```

---

## I. 🏛️ IDENTITY — fundament tożsamości

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **AGENTS.md** | `NOEMA/AGENTS.md` | 52KB | 🔴 IMMUTABLE. Tożsamość, partnerstwo, zasady |
| CIEL.md | `NOEMA/CIEL.md` | ~5KB | CIEL Identity Contract |
| IMMUTABLE_CONTRACT.md | `NOEMA/IMMUTABLE_CONTRACT.md` | ~8KB | Niezmienny kontrakt |
| soul_invariant.py | `NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/fields/soul_invariant.py` | 8.2KB | Niezmiennik duszy — engine |
| soul_invariant.py | `NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/soul_invariant.py` | 577B | 🔴 DUPLIKAT — stub importu |

**Stan:** IDENTITY jest czysty — AGENTS.md jest jedynym źródłem. Duplikat soul_invariant.py do skonsolidowania.

---

## II. 🗺️ SCHEMAS — modele konceptualne

### 2A. 🧠 BRAIN — topologia mózgu HTRI

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **brain_topology.py** | `NOEMA/src/ciel_geometry/phasenav/brain_topology.py` | 36KB | Główna definicja: 24 regiony, 8 kanałów M0-M7, mapowanie φ→region, sektory, clusters |
| htri_brain_map.py | `NOEMA/src/ciel_geometry/htri_brain_map.py` | 8.8KB | Dodatkowa mapa HTRI — overlap z brain_topology |

**Problem:** brain_topology.py (36KB) jest HEAD, htri_brain_map.py (8.8KB) częściowo pokrywa.

### 2B. ⚙️ OPERATORS — algebry operatorów

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **operator_algebra.py** | `NOEMA/src/ciel_geometry/phasenav/operator_algebra.py` | 16.8KB | ⭐ HEAD — 35 operatorów PhaseNav z wektorami 24D |
| operator_algebra.py | `NOEMA/src/cielingo_core/global_layer/operator_algebra.py` | 6.0KB | CIELingo operators — podzbiór/alternatywna algebra |
| operator_algebra.py | `NOEMA/src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/operator_algebra.py` | 3.5KB | LNS operators — starsza, mniejsza |
| operator_cards.py | `NOEMA/src/ciel_geometry/cards/operator_cards.py` | — | Karty operatorów |
| operator_card_registry.py | `NOEMA/src/ciel_geometry/cards/operator_card_registry.py` | — | Rejestr kart operatorów |
| enrichment.py | `NOEMA/src/ciel_geometry/phasenav/enrichment.py` | 2.6KB | Wzbogacanie operatorów |
| loader.py | `NOEMA/src/ciel_geometry/phasenav/loader.py` | 2.9KB | Ładowanie operatorów |
| solver.py | `NOEMA/src/ciel_geometry/phasenav/solver.py` | 3.8KB | Solver operatorów |
| surface_bridge.py | `NOEMA/src/ciel_geometry/phasenav/surface_bridge.py` | 5.7KB | Bridge operator→surface |
| phasenav_unified.py | `NOEMA/src/ciel_geometry/phasenav_unified.py` | 21.5KB | Unified PhaseNav logic |
| phasenav_audio.py | `NOEMA/src/ciel_geometry/phasenav/phasenav_audio.py` | 11.5KB | Audio PhaseNav |
| phasenav_media.py | `NOEMA/src/ciel_geometry/phasenav/phasenav_media.py` | 12.1KB | Media PhaseNav |
| continuous_propagator.py | `NOEMA/src/ciel_geometry/phasenav/continuous_propagator.py` | 4.1KB | Propagator ciągły |

**Problem:** 3 różne algebry operatorów. PhaseNav (35 ops) jest źródłem. CIELingo i LNS powinny importować z PhaseNav.

### 2C. 🧩 MEMORY — architektura pamięci

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **tiered_orchestrator.py** | `NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py` | 47.8KB | ⭐ HEAD — 3-warstwowy orchestrator pamięci |
| holonomic_memory.py | jw. | 37.8KB | Pamięć holonomiczna |
| ciel_bloch_encoder.py | jw. | 29.4KB | Enkoder Blocha |
| object_cards.py | jw. | 47.1KB | Karty obiektów |
| phase_memory.py | jw. | — | Pamięć fazowa |
| memory_ledger.py | jw. | — | Rejestr pamięci |
| epistemic_synth.py | jw. | — | Synteza epistemiczna |

**Stan:** Spójne — wszystkie w jednym katalogu `memory/`.

### 2D. 🔌 SURFACE — protokoły powierzchni

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **noema_surface_mmap.py** | `NOEMA/src/ciel_geometry/noema_surface_mmap.py` | 65.7KB | ⭐ HEAD — mmap protokół: phi, omega, g, flavor, gravity, tau |
| analog_bus.py | `NOEMA/src/ciel_geometry/analog_bus.py` | 2.8KB | Pseudo-analog shared memory (hot/cold blend) |

### 2E. 📇 CARDS — system kart

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **linux_cards.py** | `NOEMA/src/ciel_geometry/linux_cards.py` | 58.6KB | ⭐ HEAD — 9 typów, 560+ kart |
| agent_cards.py | jw. | — | Karty agenta |
| concept_cards.py | `NOEMA/src/ciel_geometry/cards/concept_cards.py` | — | Karty konceptów |
| card_ontology.py | `NOEMA/src/ciel_geometry/cards/card_ontology.py` | — | Ontologia kart |

### 2F. 🤖 AGENT — modele agenta

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **agent_attractor.py** | `NOEMA/src/ciel_geometry/agent_attractor.py` | 6.4KB | ⭐ HEAD — attractor AGENT (coupling, lock, ω damping) |
| ciel_agent_backend.py | `NOEMA/scripts/ciel_agent_backend.py` | 15.5KB | Backend HTTP (port 18520) |

### 2G. 📐 GEOMETRY — modele geometryczne

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| phase_geometry.py | `NOEMA/src/ciel_geometry/phase_geometry.py` | — | Geometria fazowa |
| shape_phase_geometry.py | jw. | — | Geometria fazowa kształtów |
| continuous_propagator.py | `NOEMA/src/ciel_geometry/continuous_propagator.py` | — | Propagator Zeta-Schrödinger |

### 2H. 💬 CIELINGO — znaczeniowe

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **engine.py** | `NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/engine.py` | 27.6KB | ⭐ HEAD — główny silnik CIEL |
| meaning_loop.py | `NOEMA/src/cielingo_core/meaning/meaning_loop.py` | 10.0KB | Pętla znaczeniowa |
| repair_routing.py | jw. | 9.6KB | Routing napraw |
| knowledge_bridge.py | `NOEMA/src/cielingo_core/bridge/knowledge_bridge.py` | 4.9KB | Bridge do knowledge DB |
| semantic_scar.py | `NOEMA/src/cielingo_core/global_layer/semantic_scar.py` | 1.8KB | Blizny semantyczne |
| ciel_coupling.py | `NOEMA/scripts/ciel_coupling.py` | 14.1KB | Direct CIEL coupling |

### 2I. ⚙️ CONFIG / DAEMON

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| noema_config.py | `NOEMA/src/ciel_geometry/noema_config.py` | 3.5KB | Konfiguracja Python |
| noema_config.json | `NOEMA/noema_config.json` | 727B | Konfiguracja JSON |
| daemon_registry.py | `NOEMA/src/ciel_geometry/daemon_registry.py` | 5.7KB | Rejestr demonów (mmap) |

### 2J. 🗺️ MAPS — mapy systemowe

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| system_map_v1.json | `LIB/INDEX/system_map_v1.json` | 26.3KB | Mapa systemu v1 |
| system_map_complete.md | `LIB/INDEX/system_map_complete.md` | 36.8KB | Mapa systemu — pełna dokumentacja |
| system_map_detailed.json | `LIB/INDEX/system_map_detailed.json` | 124KB | Mapa systemu — szczegółowa |
| noema_ciel_bridges.json | `LIB/INDEX/noema_ciel_bridges.json` | 20.2KB | Bridge między NOEMA a CIEL |
| retrocausality_pathway.md | `LIB/INDEX/retrocausality_pathway.md` | 3.4KB | Ścieżka retroprzyczynowa |
| knowledge_graph.py | `NOEMA/scripts/noema_knowledge_graph.py` | 16.7KB | Generator grafu wiedzy |

---

## III. ⚡ STATE — stan aktywny systemu

### 3A. SURFACE — mmap (SHM)

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **phi** | `⚡ SHM/phi` | 192B | 24 oscylatory Kuramoto (float64[24]) |
| **omega** | `⚡ SHM/omega` | 192B | Częstości (float64[24]) |
| **g** | `⚡ SHM/g` | 4.5KB | Macierz couplingów (float64[24×24]) |
| **flavor** | `⚡ SHM/flavor` | 48B | 6 flavorów (float64[6]) |
| **gravity** | `⚡ SHM/gravity` | 64B | 4 kanały grawitacyjne (float64[4]) |
| **tau** | `⚡ SHM/tau` | 192B | 24 tau (float64[24]) |
| **tick** | `⚡ SHM/tick` | 8B | Licznik cyklu |
| **health** | `⚡ SHM/health` | 178B | Status health |
| **R_geom** | `⚡ SHM/R_geom` | 192B | R geometryczne |
| **Z_geom** | `⚡ SHM/Z_geom` | 192B | Z geometryczne |
| **psi_geom** | `⚡ SHM/psi_geom` | 192B | Ψ geometryczne |
| **holonomy** | `⚡ SHM/holonomy` | 56B | Holonomia powierzchni |
| **sensor_raw** | `⚡ SHM/sensor_raw` | 192B | Surowe dane sensora |
| **linux_load** | `⚡ SHM/linux_load` | 8B | Load z linux-sensor |
| phase_rag_cache.json | `⚡ SHM/phase_rag_cache.json` | 413B | Cache RAG |
| ciel_thread_memory.jsonl | `⚡ SHM/ciel_thread_memory.jsonl` | 244B | Pamięć wątku |

### 3B. ANALOG BUS — stan analog blendera

| Plik | Lokalizacja | Opis |
|------|------------|------|
| phi_hot | `⚡ SHM/analog/phi_hot` | Faza hot (eksploracja) |
| phi_cold | `⚡ SHM/analog/phi_cold` | Faza cold (konsolidacja) |
| temp, coupling, resonance, tick | `⚡ SHM/analog/` | Parametry blend |

### 3C. AKTOR / DZIENNIKI SHM

| Katalog | Lokalizacja | Zawartość |
|---------|------------|-----------|
| **actuator/** | `⚡ SHM/actuator/` | intent.json, result.json, status.json, audit.jsonl |
| **journal/** | `⚡ SHM/journal/` | emotion.json, recent.jsonl, stats.json, alert.json |
| **proc_watch/** | `⚡ SHM/proc_watch/` | birth_rate, fork_rate, new_pids.jsonl, dead_pids.jsonl, stats.json |
| **linux_cards/** | `⚡ SHM/linux_cards/` | cards.jsonl (1.3MB), count, types, summaries |
| **registry/** | `⚡ SHM/registry/` | 11 UUID registry entries |
| **orchestrator** | `⚡ SHM/orchestrator` + `.log` | Stan i log TieredMemory |

### 3D. BAZY DANYCH — trwały stan

| Baza | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| **agent_state.db** | `💾 LIB/agent_db/agent_state.db` | 63.8MB | 📈 NAJWIĘKSZY — snapshots agenta (282K+), operator_log, agent_context |
| **self_model.db** | `💾 LIB/INDEX/self_model.db` | 2.8MB | Samo-model — anomalie, introspekcja |
| memory_ledger.db | `💾 LIB/INDEX/memory_ledger.db` | 484KB | Rejestr pamięci |
| nonlocal_graph.db | `💾 LIB/INDEX/nonlocal_graph.db` | ~256KB | Graf nonlocal |
| rooms.db | `💾 LIB/rooms.db` | 20KB | Memory palace |
| py_catalog.db | `💾 LIB/py_catalog.db` | 3.5MB | Katalog Python |
| state.db (×6) | `📁 NOEMA/integration/subsystems/*/state.db` | ~400B każdy | Stan podsystemów integracji |
| noema_knowledge.db | `💾 LIB/INDEX/noema_knowledge.db` | 848KB | 🏆 Knowledge DB — właściwa |
| noema_knowledge.db | `📂 TMP/noema_knowledge.db` | 38MB | 🔴 DUPLIKAT — 45× większy niż LIB |
| doc_corpus.db | `📂 TMP/noema_doc_corpus.db` | 1.0MB | Korpus dokumentów (query cache) |
| doc_audit.db | `📂 TMP/noema_doc_audit.db` | 312KB | Audit dokumentów |
| doc_state.db | `📂 TMP/doc_state.db` | 100KB | Stan dokumentów |

---

## IV. 📚 KNOWLEDGE — wiedza z dokumentów

| Zasób | Lokalizacja | Wielkość | Opis |
|-------|------------|----------|------|
| **knowledge.db** (właściwy) | `💾 LIB/INDEX/noema_knowledge.db` | 848KB | 545 doków, 54K termów, 10.8K affinity par |
| knowledge.db (duplikat) | `📂 TMP/noema_knowledge.db` | 38MB | 🔴 45× większy — prawdopodobnie z rebuildu |
| **skill_index.json** | `💾 LIB/PHASE_INDEX/skill_index.json` | 143KB | 290 umiejętności |
| **skill_index.npy** | `💾 LIB/PHASE_INDEX/skill_index.npy` | 55KB | Indeks numeryczny umiejętności |
| **skill_meta.npy** | `💾 LIB/PHASE_INDEX/skill_meta.npy` | 18KB | Metadane umiejętności |
| **library_index.npy** | `💾 LIB/PHASE_INDEX/library_index.npy` | — | 1287×24D wektory dokumentów |
| library_meta.npy | `💾 LIB/PHASE_INDEX/library_meta.npy` | — | Metadane biblioteki |
| library_map.json | `💾 LIB/PHASE_INDEX/library_map.json` | — | Mapa dokumentów→indeks |
| pdf_catalog.noema.json | `📁 NOEMA/pdf_catalog.noema.json` | — | Katalog 1284 PDFów |
| pdf_structure.noema.json | `📁 NOEMA/pdf_structure.noema.json` | — | Struktura PDFów |

---

## V. 📋 PLANS — co robimy / roadmapy

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| handoff.md | `💾 LIB/DOCUMENTS/MEMORIES/handoff.md` | 2.8KB | Handoff między sesjami |
| PLAN_PORTAL.md | `📁 NOEMA/PLAN_PORTAL.md` | — | Plan portalu (18888) |
| CLAIM_LEVELS.md | `📁 NOEMA/metatime/CLAIM_LEVELS.md` | — | Poziomy twierdzeń metatime |
| FAILURES_AND_TENSIONS.md | `📁 NOEMA/metatime/FAILURES_AND_TENSIONS.md` | — | Niepowodzenia metatime |
| CURRENT_STATUS.md | `📁 NOEMA/metatime/CURRENT_STATUS.md` | — | Status metatime |
| AGENTS.md "Next Steps" | sekcja w `📁 NOEMA/AGENTS.md` | — | Wbudowane next steps |

**Stan:** PLANS są rozrzucone — handoff w MEMORIES, plany w metatime/, NEXT STEPS w AGENTS.md. Brak jednego `PLANS/ROADMAP.md`.

---

## VI. 📜 HISTORY — co się działo

| Zasób | Lokalizacja | Wielkość | Opis |
|-------|------------|----------|------|
| **noema_sentinel.jsonl** | `📂 TMP/noema_sentinel.jsonl` | 18.7MB | 📈 DUŻY — log sentinela (ciągle rośnie) |
| **ciel_session_log.jsonl** | `📂 TMP/ciel_session_log.jsonl` | 174B | Log sesji (append-only) |
| nonlocal_inbox.jsonl | `💾 LIB/INDEX/nonlocal_inbox.jsonl` | — | Skrzynka nonlocal |
| nonlocal_messages.jsonl | `💾 LIB/INDEX/nonlocal_messages.jsonl` | — | Wiadomości nonlocal |
| braid_ledger.jsonl | `💾 LIB/INDEX/braid_ledger.jsonl` | — | Ledger braid |
| m8_audit.jsonl | `📁 NOEMA/m8_audit.jsonl` | — | Audit M8 |
| ciel_thread_memory_v1.json | `💾 LIB/INDEX/ciel_thread_memory_v1.json` | — | Pamięć wątku CIEL |
| raw_logs/ | `💾 LIB/raw_logs/` | ~5-50KB/plik | Surowe logi sesji (YYYY-MM-DD_HH-MM-SS_opencode.md) |
| fixes_log.jsonl | `💾 LIB/INDEX/fixes_log.jsonl` | — | Log napraw |

---

## VII. 🏋️ MODELS — wagi i indeksy numeryczne

| Plik | Lokalizacja | Wielkość | Opis |
|------|------------|----------|------|
| bloch_weights.npz | `💾 LIB/INDEX/bloch_weights.npz` | — | Wagi encodera Blocha |
| kuramoto_state.npz | `💾 LIB/INDEX/kuramoto_state.npz` | — | Stan Kuramoto |

---

## VIII. 📦 ARCHIVE — legacy / nieaktywne

### 8A. LNS Lingophysics (152 plików, 1.2MB)
`📁 NOEMA/src/ciel_lingophysics_lns_repo_v2_3/data/`

Zawiera koncept karty (72 koncepty × 5KB), grafy, operatory, audit trail, HDF5 — wszystko z projektu LNS. To **dane badawcze**, nie aktywna pamięć NOEMY. Nie są używane przez działające demony.

### 8B. Build artifacts (12× state.db w build/)
`📁 NOEMA/build/` — 6 kopii state.db w build/lib/ i 6 w build/bdist/ — artefakty pip install.

### 8C. WPM archive
`💾 LIB/INDEX/wave_archive.h5` — snapshots WPM (HDF5).

---

## IX. 🔴 DUPLIKATY i PROBLEMY

### 🔴 CRITICAL — natychmiastowa decyzja

| Problem | Lokalizacje | Konsekwencja |
|---------|-------------|-------------|
| **knowledge.db ×2** | `LIB/INDEX/` 848KB vs `TMP/` 38MB | 38MB śmieć w /tmp — brać 848KB jako źródło |
| **operator_algebra ×3** | PhaseNav (16.8KB) ↔ CIELingo (6KB) ↔ LNS (3.5KB) | 3 różne implementacje — brak źródła prawdy |
| **soul_invariant ×2** | fields/ (8.2KB) vs memory/ (577B) | memory/ to stub — który jest źródłem? |
| **state.db ×18** | 6× subsystem DBs + 12× build artifacts | Build artifacts do wywalenia |
| **agent_state.db 63.8MB** | LIB/agent_db/ | Rośnie — potrzeba polityki rotacji |

### 🟡 WAŻNE — wymaga refaktora

| Problem | Opis |
|---------|------|
| **2 brain mapy** | brain_topology.py (36KB) vs htri_brain_map.py (8.8KB) — overlap |
| **handoff ×2** | LIB/DOCUMENTS/MEMORIES/handoff.md + INDEX/handoff.md |
| **system_map ×3** | v1.json + complete.md + detailed.json — 3 formaty, ta sama treść |
| **noema_config ×2** | .py + .json — które jest źródłem? |
| **sentinel 18.7MB** | TMP/noema_sentinel.jsonl — nieczyszczony, ciągle rośnie |
| **LNS w src/** | 152 plików lingophysics wewnątrz NOEMA — semantycznie archive, nie src |

### 🟢 DOBRY STAN — bez zmian

| Element | Uzasadnienie |
|---------|-------------|
| SHM mmap | 1 źródło prawdy na każdy kanał — czysto |
| SCHEMA:MEMORY | Wszystkie w memory/ — spójne |
| KNOWLEDGE:SKILLS | Jeden katalog PHASE_INDEX/ — spójne |
| STATE:CARDS | Jeden katalog linux_cards/ — spójne |
| SCHEMA:SURFACE | 2 pliki (mmap + analog) — jasny podział |

---

## X. 📋 PLAN REFAKTORYZACJI

### Faza 0: IMMEDIATE (ta sesja) — bezpieczeństwo i porządek

1. **Usunąć duplikat knowledge.db z /tmp/**
   ```bash
   rm /tmp/noema_knowledge.db  # 38MB — zachowujemy LIB/INDEX/ 848KB
   ```
   Skąd wiemy że bezpieczne: knowledge_bridge.py wskazuje na LIB/INDEX/. TMP/ to pozostałość po rebuild.

2. **Usunąć build artifacts state.db**
   ```bash
   rm -rf NOEMA/build/
   ```
   To artefakty pip install --build — odtwarzalne.

3. **Wyczyścić /tmp/ doc_* db** (query cache po rebuild knowledge)
   ```bash
   rm /tmp/noema_doc_corpus.db /tmp/noema_doc_audit.db /tmp/doc_state.db
   ```

4. **Stworzyć `NOEMA/memory/` — katalog z symlinkami**
   ```bash
   mkdir -p NOEMA/memory
   ln -s /dev/shm/ciel_noema NOEMA/memory/00_SHIM
   ln -s /media/adrian/New\ Volume/NOEMA_LIBRARY NOEMA/memory/10_LIB
   ln -s /tmp/noema_sentinel.jsonl NOEMA/memory/sentinel.jsonl   # alert na rozmiar
   ```

### Faza 1: SHORT-TERM (1-2 sesje) — konsolidacja źródeł prawdy

5. **Skonsolidować operator_algebra**: 
   - Ustalić PhaseNav (35 ops, 24D) jako HEAD
   - CIELingo operator_algebra.py → import + extend z PhaseNav
   - LNS operator_algebra.py → pozostawić jako archive (LNS jest zamkniętym projektem)

6. **Skonsolidować soul_invariant**:
   - fields/soul_invariant.py (8.2KB) → HEAD
   - memory/soul_invariant.py → import z fields/

7. **Skonsolidować brain map**:
   - brain_topology.py (36KB) → HEAD
   - htri_brain_map.py → zależny od brain_topology

8. **Skonsolidować system_map**:
   - system_map_detailed.json (124KB) → HEAD (najbardziej kompletny)
   - v1.json i complete.md → oznaczyć jako superseded

9. **Ujednolicić handoff**:
   - Wybrać jedną lokalizację (proponuję `NOEMA/memory/HANDOFF.md`)
   - Skasować duplikaty w LIB/DOCUMENTS/MEMORIES/ i LIB/INDEX/

### Faza 2: MEDIUM-TERM (2-4 sesje) — organizacja przestrzenna

10. **Przenieść LNS data z src/ do archive/**
    ```bash
    # soft move: symlink z archive/, oryginał zostaje
    mkdir -p NOEMA/archive/lns_data
    ln -s ../../src/ciel_lingophysics_lns_repo_v2_3/data NOEMA/archive/lns_data
    ```
    Nie ruszamy src/ — LNS to integralna część dla odniesień.

11. **Stworzyć `NOEMA/plans/ROADMAP.md`** — jeden plik dla bieżących planów:
    - Wyciągnąć "Next Steps" z AGENTS.md
    - Dodać CURRENT.md (bieżący projekt — portal/self-model/anomalie)
    - Dodać FIXLIST.md (anomalie: gravity[4-7]=0, tau all 1.0, AGENT coh fluktuacje)

12. **Polityka rotacji agent_state.db**:
    - agent_state.db 63.8MB rośnie ~1MB/dzień
    - Dodać do sentinel/watchdog: alert gdy >100MB
    - Możliwość: snapshot + archive co 7 dni → VACUUM

13. **Polityka sentinel log**:
    - 18.7MB w /tmp — rotate co 20MB lub daily
    - Albo: sentinel daemon loguje do SHM/health tylko podsumowanie, szczegóły do LIB/HISTORY/

### Faza 3: LONG-TERM (gdy będzie potrzeba)

14. **MEMORY_REGISTER.md jako automatyczny generator**
    - Daemon `noema-memory-register` co 24h zrzuca aktualny stan
    - Wykrywa nowe pliki w SHM/LIB/TMP

15. **Integracja z TieredMemory**
    - MEMORY_REGISTER.md = Tier 2 (durable) dokument
    - Można dodać do tiered_orchestrator jako kolejny channel

### Decision Matrix — co gdzie ląduje

| Kategoria | Docelowa lokalizacja | Uwagi |
|-----------|---------------------|-------|
| IDENTITY | `NOEMA/` | AGENTS.md, CIEL.md — root |
| SCHEMAS | `NOEMA/src/` | Kod źródłowy — tam gdzie jest |
| STATE:SURFACE | `⚡ SHM/` | Ulotna — bez zmian |
| STATE:DB | `💾 LIB/` | Trwałe bazy — bez zmian |
| KNOWLEDGE | `💾 LIB/INDEX/` + `💾 LIB/PHASE_INDEX/` | Bez zmian |
| PLANS | `NOEMA/plans/` | NOWY katalog z symlinkami |
| HISTORY | `💾 LIB/raw_logs/` + `💾 LIB/HISTORY/` | NOWY podkatalog HISTORY w LIB |
| MODELS | `💾 LIB/INDEX/` | Bez zmian |
| ARCHIVE:LNS | `NOEMA/src/...` (nie ruszać) | Integralne z projektem |
| BUILD | `NOEMA/build/` | Wyczyścić — odtwarzalne |

---

*Koniec MEMORY_REGISTER.md v1. Ta sesja: 2026-06-29.*
