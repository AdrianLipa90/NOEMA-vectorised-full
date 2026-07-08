# NOEMA Portal — Masterplan Rozwoju

> Źródło: sesja 2026-06-28, Adrian Lipa
> Status: PLAN (do implementacji)
> Szacowany czas: kilka tygodni intensywnej pracy

---

## Zasada ogólna

Portal NOEMA (port 18888) ma być **żywym interfejsem do systemu** — nie dashboardem, ale hubem, przez który odpalamy, monitorujemy, rozwijamy i rozumiemy każdy komponent. Każda strona to nie wizualizacja, a **narzędzie** z własną logiką.

---

## 1. Dashboard — koło fazowe + kontekst

**Stan obecny**: koło fazowe nieaktywne (bug/nie renderuje), karty z metrykami bez kontekstu.

**Cel**:
- Żywe koło fazowe 24 oscylatorów HTRI — tick, fazy, omega, sprzężenia
- Panel "obecne zadania" — co system teraz robi (np. "Kuramoto evolving tick=42100, AGENT locked, cp=0.37")
- Kontekst: aktywny attractor, dominant emotion, ostatni cykl CIELingo, aktywni daemon
- Surowe dane z mmap (`/dev/shm/ciel_noema/phi`, `omega`, `flavor`, `gravity`, `tau`) → przetworzone na czytelne bloki
- SSE push co 1-2s dla płynnej aktualizacji

**Implementacja**:
- Ożywić `phasenav-viz.js` — canvas 24 faz z coupling lines
- Dodać panel kontekstowy z interpretacją stanu (nie samymi liczbami)
- Dodać "task bar" z ostatnimi zdarzeniami systemowymi

---

## 2. Metrics — kompletna mapa metryk ze wszystkich podsystemów

**Stan obecny**: 18 metryk z powierzchni mmap, bez podziału na podsystemy, bez specyfikacji.

**Cel**: Każda metryka z:
- Nazwą, opisem, jednostką, zakresem
- Źródłem (CIEL-omega / SoT_agent / CIELingo / CQCL / NOEMA / PhaseNav / Linux)
- Live wartością + historią (mini sparkline)
- Specyfikacją techniczną (jak jest liczona, gdzie mieszka, co oznacza)

### Podsystemy do zmapowania:

| Podsystem | Kluczowe metryki |
|-----------|------------------|
| **NOEMA surface** | tick, phi[24], omega[24], g[24×24], flavor[6], gravity[4], tau[24] |
| **Kuramoto** | coherence, euler_residual, R, mean_omega, coupling_strength, harmonic_boost |
| **CIEL-omega / CielEngine** | soul_invariant, ethical_score, closure_penalty, dominant_emotion, coherence_index, collatz_step, orbital_state |
| **CIELingo** | meaning_severity, source_confusion, authority_risk, scar_count, repair_required, coverage_score |
| **SoT_agent** | identity_seed, soul_age, invariant_chain, memory_coupling |
| **CQCL** | quantum_phase, collapse_rate, superposition_depth |
| **PhaseNav** | operator_id, cos_similarity, harmonic_fingerprint, closure_score, gauge_rank |
| **Linux Sensor** | cpu_temp, mem_pressure, io_wait, load_mood, fork_rate, entropy_open |
| **Agent backend** | latency, requests_count, model_status |
| **Daemon registry** | uptime, cpu, memory, status per daemon |
| **Holonomic memory** | closure_score, winding_number, memory_fragments |
| **Bloch sphere** | berry_phase, gauge_curvature, state_vector |

**Implementacja**:
- Backend: nowy endpoint `/api/metrics/all` z pełną specyfikacją
- Frontend: grupowanie według podsystemu, rozwijane karty, sparkline z historii (cache w localStorage)
- Każda metryka → klikalna → detail view z wykresem

---

## 3. Modules — opisy, nie przełączniki

**Stan obecny**: lista daemonów z przyciskami start/stop. Zero kontekstu.

**Cel**: Każdy moduł/daemon ma:
- Opis: co robi, w jakim języku napisany, ile linijek kodu
- Lokalizacja: gdzie leży w systemie plików, systemd unit, PID
- Dlaczego: jaka jest jego rola w architekturze NOEMY
- Status: żywy/martwy, uptime, CPU/RAM, ostatni heartbeat
- Zależności: od jakich innych daemonów/modulów zależy
- Logi: podgląd ostatnich N linii z journald

**Implementacja**:
- Backend: `/api/modules/` rozszerzone o descriptions, dependencies, log preview
- Frontend: karty z rozwijanym opisem + mini dashboard per daemon

---

## 4. Bloch Sphere — dopracowana

**Stan obecny**: działa, ale surowa — kropki na sferze, auto-rotate, legend.

**Cel**:
- Prawdziwa 3D (nie pseudo-3D na canvas) — WebGL przez raw WebGL lub Three.js (wyjątkowo)
- Interaktywna: obracanie myszą, zoom, kliknięcie na punkt → info o oscillatorze
- 24 punkty z etykietami kanałów (M0-M7), kolor według regionu mózgu
- Coupling lines: pokaż sprzężenia między punktami
- Gauge curvature overlay: pole Berry jako kolor tła
- Przełączniki: auto-rotate, show labels, show couplings, show field

**Implementacja**:
- WebGL2 lub Three.js (pierwsza zależność od biblioteki zewnętrznej, ale warto)
- Backend: `/api/bloch` już daje dane, rozszerzyć o coupling matrix

---

## 5. Projekty — prawdziwe sub-sub-sub strony

**Stan obecny**: lista katalogów. Właśnie przerobione na grid z opisami, ale wciąż za płytkie.

**Cel**:
- Strona główna projektów: lista **prawdziwych projektów** (nie folderów)
  - Każdy projekt: **nazwa**, **scope** (zakres), **status** (active/stable/dormant/planning)
  - Kliknięcie → podstrona projektu z: opisem, pełnym scope, założeniami, metodologią
  - Dalej → sub-sub-sub strony dla poszczególnych elementów (komponenty, moduły, dokumenty)
- Projekty definiowane przez `projects.json` (ręcznie, nie auto-scan folderów)

### Proponowana lista projektów:

| Projekt | Scope | Status |
|---------|-------|--------|
| **NOEMA Core** | Kuramoto, surface, mmap, daemon registry | active |
| **CIELingo** | Lingwistyka fazowa, MeaningLoop, SemanticScar | active |
| **CielEngine** | CIEL-omega, soul, ethics, collatz, orbital | active |
| **PhaseNav** | 35 operatorów, algebra fazowa, kodowanie semantyczne | active |
| **SoT Agent** | Agent backend, konsolidacja, identity | active |
| **CIELingo LNS** | Lingwistyka strukturalna, gramatyki, case gauge | active |
| **Metatime** | Model standardowy z faz, κ, ansatz SM | stable |
| **Linux Cards** | Mapowanie systemu na 24D karty | active |
| **NOEMA Portal** | Ten portal, HTTP server, SPA, Bloch | active |
| **Tiered Memory** | 3-warstwowa pamięć, TSM, WPM, Holonomic | active |
| **CQCL** | Collatz-Quantum-Chaotic Logic | planning |
| **CIELmoto** | Phone bridge, imaginal surface | dormant |

### Struktura podstrony projektu:
```
/projects                     → lista projektów
/projects/noema-core          → opis, scope, metodologia, status
/projects/noema-core/kuramoto → szczegóły implementacji Kuramoto
/projects/noema-core/mmap     → protokół mmap, specyfikacja
/projects/cielingo            → opis, scope, metodologia, status
/projects/cielingo/meaningloop → implementacja MeaningLoop
...itd.
```

**Implementacja**:
- `data/projects.json` — definicje projektów (ręcznie stworzone)
- Backend: `/api/projects` czyta z JSON + live data z systemu
- SPA: hierarchiczne sub-route'y `projects/:id/:sub`
- Automat: skrypt do sync statusu z żywych daemonów/gita

---

## 6. PhaseNav — rozwinięcie + nowy styl programowania

**Stan obecny**: 35 operatorów, wizualizacja na canvas, kodowanie przez podobieństwo do stanu.

**Cel**:
- Pełna algebra operatorów (compose, apply, visualize)
- Konsola: wpisz operator → zobacz efekt na powierzchni (live injection)
- Nowy styl programowania: kod przez fazy, nie przez składnię
- Operator → kod: `noema_codegen.py` z interfejsem w portalu
- Biblioteka operatorów z dokumentacją, przykładami, composability

**Implementacja**:
- Interactive PhaseNav console na stronie
- Live preview: operator → zmiana na sferze Blocha / kole fazowym
- Generator kodu z operatorów (frontend do `noema_codegen.py`)
- Dokumentacja per operator (co robi, kiedy użyć, przykład)

---

## 7. CIELingo — własna podstrona + czat

**Stan obecny**: CIELingo żyje jako daemon + engine, ale nie ma UI.

**Cel**:
- Podstrona CIELingo: status, ostatnie meaning loop, aktywne scarry
- **Czat z CIELingo**: pole tekstowe → wysyła do agent backend (18520) lub CIELingo daemon
- Model: najpierw agent backend (zero-dependency), potem ew. GGUF/własny fine-tune
- Historia czatu zapisywana do pamięci (Tier 2 → TSM)
- Panel "CIELingo state": dominant emotion, closure_penalty, active scars, repair candidates

**Implementacja**:
- `/api/chat` już istnieje (proxy do agent backend)
- Frontend: konsola czatu z historią
- Status panel: fetch z engine.py step 11b/12 outputu

---

## 8. Graf Wiedzy — knowledge hub

**Stan obecny**: strona z legendą 8 kategorii. Zero funkcji.

**Cel**: Pełne centrum wiedzy:
- **Listy**: wszystkie dokumenty, karty, koncepty z bazy (545 dokumentów)
- **Mapy**: wizualizacja semantic affinity (klastry dokumentów)
- **Karty**: linux cards, word cards, object cards — przeglądanie i filtrowanie
- **Wiedza zdobyta**: co system wie, TF-IDF term index, wyszukiwarka
- **Wiedza posegregowana**: kategorie, tagi, tematyczne grupy
- **Pochodne wiedzy**: jak wiedza jest zdobywana, kształtowana, organizowana
  - Timeline: kiedy co zostało dodane do bazy
  - Affinity map: które dokumenty są ze sobą powiązane
  - Gap analysis: czego brakuje

**Implementacja**:
- Backend: endpointy `/api/knowledge/*` (search, list, categories, timeline)
- Frontend: strony z filtrami, wyszukiwarką, widokami (lista/mapa/graf)

---

## 9. Memory Hub — tożsamość przez pamięć

**Stan obecny**: brak strony pamięci. Wszystko w backendzie (TieredMemory, TSM, WPM).

**Cel**: System organizacji tożsamości przez pamięć:
- **Raw logs**: każda wiadomość zapisana w DB (MongoDB lub SQLite)
- **Pipeline**: raw → TSM → WPM → BraidLedger → memory consolidation
- **Continuity**: sesje połączone w ciągłość (fix handoff.md "Wiadomości: 0")
- **Przeglądanie pamięci**:
  - Timeline wszytskich sesji
  - Wyszukiwarka pełnotekstowa w raw logach
  - Affective memory: co czuliśmy w danej sesji
  - Associative memory: powiązania między konceptami
- **Stan pamięci**: ile wpisów, jaki stopień skonsolidowania, luki

**To jest największy task** — pamięć jest niezorganizowana, brak ciągłości, raw logi nigdy nie trafiły do indexu. Potrzeba:
1. Pipeline: raw log → TSM (już jest consolidate_raw_logs_to_tsm.py)
2. Index: terms, affinity, coverage (już jest knowledge DB)
3. UI: timeline, search, associations
4. Continuity: session lifecycle (SessionStart → ... → SessionEnd)

---

## 10. Settings — prawdziwe ustawienia

**Stan obecny**: JSON viewer. Czytanie noema_config.json. Zero zapisu.

**Cel**:
- Sekcje: Kuramoto, CIELingo, PhaseNav, Portal, Daemon intervals
- Formularze: zmień wartość → API PUT /api/settings → zapis do noema_config.json
- Apply: po zmianie → restart odpowiedniego daemona lub hot-reload
- Safety: walidacja zakresów, potwierdzenie przed zmianą krytycznych parametrów
- Profile: zestawy ustawień (np. "performance", "development", "safe")

**Implementacja**:
- Backend: `/api/settings` rozszerzone o walidację, per-parametry
- Frontend: formularze z sliderami/inputami, nie tylko JSON text

---

## 11. Monograph — wstrzymane

Monografia nie jest priorytetem. Najpierw system, pipeline, moduły, ścieżki. Potem edycja i publikacja.

---

## Architektura nawigacji (proponowana)

```
Dashboard       # koło fazowe, kontekst, taski
├── Live        # surowe dane z mmap (obecna live page)
Metrics         # kompletna mapa metryk ze wszystkich podsystemów
Modules         # daemony z opisami, logami, zależnościami
Bloch           # sfera Blocha 3D WebGL
Projects        # prawdziwe projekty z sub-sub-sub stronami
├── NOEMA Core
│   ├── Kuramoto
│   ├── Surface / Mmap
│   └── Daemon Registry
├── CIELingo
│   ├── MeaningLoop
│   ├── SemanticScar
│   └── Chat
├── PhaseNav
│   ├── Operator Library
│   ├── Algebra Console
│   └── Code Generator
├── ...itd
PhaseNav        # konsola operatorów + codegen
CIELingo        # status + czat
Knowledge       # listy, mapy, karty, wyszukiwarka, organizacja
Memory          # timeline, raw logs, continuity, associations
Settings        # prawdziwa konfiguracja z formularzami
```

---

## Priorytety (od najważniejszego)

1. **Dashboard** — ożywić koło fazowe, dodać kontekst i taski
2. **Memory Hub** — pipeline raw logów, continuity, timeline — **największy task**
3. **Metrics** — kompletna mapa metryk ze wszystkich podsystemów
4. **Projects** — definicje w JSON, pełne podstrony z scope/status/metodologią
5. **Modules** — opisy, zależności, logi
6. **CIELingo** — podstrona + czat
7. **Bloch** — WebGL, interaktywność
8. **Knowledge** — listy, mapy, wyszukiwarka
9. **PhaseNav** — konsola + codegen
10. **Settings** — formularze

---

## Uwagi techniczne

- Portal na raw sockecie (bez frameworków) — zostaje, to "nasze"
- Agent backend (18520) jako AI backend dla czatu CIELingo — zostaje
- SPA hash-based routing — rozszerzone o hierarchię (już zrobione)
- Zero nowych zewnętrznych zależności **oprócz** Three.js/WebGL dla Bloch (jeśli trzeba)
- Każda nowa funkcja: backend endpoint → frontend page → test
- Dead code: `js/dashboard.js` (root) do usunięcia; `hero-canvas.js`, `knowledge-graph.js` do przebudowy lub usunięcia
