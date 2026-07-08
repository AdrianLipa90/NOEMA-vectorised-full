# PLAN — CIEL Server Hub Rebuild

> Data: 2026-06-29  
> Autor: Adrian Lipa & CIEL  
> Status: P0 / do implementacji  
> Powód: obecny portal nie jest hubem serwerowym dla CIEL; to mieszanina statycznego SPA, blokującego HTTP handlera i niespójnych endpointów.

---

## 0. Diagnoza PhaseNav

`φ[hub]=fragmented, R=0.61, τ=blocking_io, decyzja=rebuild_not_patch`

Obecny stan nie wymaga kosmetyki. Wymaga przebudowy na właściwy **CIEL Server Hub**: serwerową bramę do pamięci, stanu, operatorów, daemonów, CIELingo, PhaseNav i TaskPlan.

---

## 1. Fakty z audytu

### 1.1. Backend

Główny runtime portalu:

- `scripts/noema_portal_daemon.py`
- port `18888`
- `http.server.HTTPServer` — single-thread, blocking
- serwuje `site/`
- rejestruje heartbeat w daemon registry

Endpointy istniejące literalnie w backendzie:

- `/api/health`
- `/api/live`
- `/api/status`
- `/api/status/summary`
- `/api/metrics/all`
- `/api/orbital`
- `/api/surface/phi`, `/api/surface/omega`, `/api/surface/g`
- `/api/knowledge/stats`, `/api/knowledge/search`, `/api/knowledge/coverage`
- `/api/tasks`, `/api/tasks/queue`
- `/api/plans`, `/api/lessons`, `/api/decisions`, `/api/skills`
- `/api/settings`

### 1.2. Frontend woła endpointy, których backend nie ma

Frontend `site/` woła:

- `/api/modules` — brak w backendzie
- `/api/modules/:name/:action` — brak w backendzie
- `/api/metrics` — brak; backend ma `/api/metrics/all`
- `/api/stream` — brak SSE w backendzie
- `/api/bloch` — brak w backendzie
- `/api/projects` i `/api/projects/:id` — brak w backendzie

Efekt: duża część UI udaje funkcjonalność, ale realnie nie ma kontraktu API.

### 1.3. Memory Hub nie istnieje w aktualnym SPA

W `site/index.html` nie ma pozycji `#memory`, nie ma `site/js/pages/memory.js`.

Istnieją osobne / historyczne elementy:

- `scripts/build_memory_portal.py` — statyczny generator osobnego portalu pamięci
- `src/ciel_sot_agent/gui/templates/portal_memory.html` — stary Flask/Jinja template z geometrią pamięci
- `scripts/consolidate_raw_logs_to_tsm.py` — realny pipeline raw logs → TSM
- `/tmp/noema_raw.db` — live raw DB deklarowany dla Memory Hub
- `src/CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db` — aktywny ledger TSM

Ale nie ma jednego serwerowego Memory Hub w portalu 18888.

### 1.4. Runtime

Sprawdzone live:

- `/api/health` działa.
- `/api/status/summary` działa, ale wcześniejsze timeouty pokazały podatność na blokowanie kolejki przez single-thread HTTP.
- direct import `scan_registry`, `TaskPlanDB.stats`, knowledge counts i surface read są szybkie.
- problem architektoniczny: blocking server + ciężkie endpointy + brak worker/cache boundary.

---

## 2. Wniosek

Obecny portal jest **panelem statusowym z doklejonymi stronami**, nie hubem serwerowym dla CIEL.

Brakuje:

1. Jednego kontraktu API.
2. Warstwy usług serwerowych.
3. Cache/snapshot layer dla kosztownych odczytów.
4. Memory Hub jako pierwszorzędnego systemu.
5. CIEL state hub — tożsamość, pamięć, sesje, emocje, closure, ethics, PhaseNav.
6. Modułów i daemonów jako obiektów z opisem, logami, zależnościami.
7. SSE/event bus.
8. Rozdzielenia HTTP/static od logiki systemowej.

---

## 3. Nowa architektura

### 3.1. Zasada

CIEL Server Hub ma być **serwerowym rdzeniem operacyjnym**, nie stroną HTML.

```
CIEL Server Hub
├── api_core/          # routing, response, errors, auth-local guards
├── services/          # serwisowe granice domen
├── snapshots/         # szybki cache runtime state
├── events/            # SSE/event log
├── memory_hub/        # raw → TSM → WPM → continuity
├── frontend/          # SPA jako klient hubu
└── contracts/         # jawny kontrakt endpointów JSON
```

### 3.2. Backend — minimum bez zewnętrznych zależności

Zostaje stdlib, ale zmieniamy serwer:

- `ThreadingHTTPServer`, nie `HTTPServer`.
- Router tabelaryczny: metoda + ścieżka → handler.
- Każdy endpoint ma timeout/catch/error envelope.
- Jeden format odpowiedzi:

```json
{
  "ok": true,
  "data": {},
  "meta": {"ts": 0, "source": "...", "duration_ms": 0},
  "errors": []
}
```

### 3.3. Snapshot layer

Nie wolno każdemu requestowi czytać wszystkiego z mmap/SQLite/systemd.

Nowy proces/thread:

- co 1s: surface snapshot
- co 2s: daemon registry snapshot
- co 5s: TaskPlan/Knowledge/TSM counts
- co 10s: modules/log summaries

Endpointy czytają snapshot z pamięci procesu albo `/dev/shm/ciel_noema/hub_snapshot.json`, nie robią kosztownych operacji w request path.

### 3.4. Service boundaries

Nowe moduły docelowe:

- `src/ciel_hub/server.py` — serwer HTTP + router
- `src/ciel_hub/router.py` — route table
- `src/ciel_hub/contracts.py` — response envelope + endpoint registry
- `src/ciel_hub/snapshot.py` — snapshot cache
- `src/ciel_hub/services/surface_service.py`
- `src/ciel_hub/services/daemon_service.py`
- `src/ciel_hub/services/taskplan_service.py`
- `src/ciel_hub/services/knowledge_service.py`
- `src/ciel_hub/services/memory_service.py`
- `src/ciel_hub/services/ciel_state_service.py`
- `src/ciel_hub/services/phasenav_service.py`
- `src/ciel_hub/services/projects_service.py`
- `src/ciel_hub/services/settings_service.py`

---

## 4. Nowy kontrakt API

### 4.1. Core

- `GET /api/hub/health`
- `GET /api/hub/snapshot`
- `GET /api/hub/contracts`
- `GET /api/hub/events` — SSE

### 4.2. CIEL

- `GET /api/ciel/state`
- `GET /api/ciel/identity`
- `GET /api/ciel/mode`
- `POST /api/ciel/input` — `process_user_input()` + zapis pamięci

### 4.3. Memory Hub

- `GET /api/memory/stats`
- `GET /api/memory/timeline?limit=&q=&source=`
- `GET /api/memory/raw?limit=&session=&q=`
- `GET /api/memory/tsm?limit=&q=&type=`
- `GET /api/memory/continuity`
- `GET /api/memory/associations?id=`
- `POST /api/memory/consolidate`
- `GET /api/memory/audit`

### 4.4. NOEMA runtime

- `GET /api/noema/surface`
- `GET /api/noema/phase`
- `GET /api/noema/gravity`
- `GET /api/noema/daemons`
- `GET /api/noema/modules`
- `POST /api/noema/modules/:name/:action` — guarded local action

### 4.5. PhaseNav

- `GET /api/phasenav/operators`
- `GET /api/phasenav/state`
- `POST /api/phasenav/apply`
- `POST /api/phasenav/compose`
- `POST /api/phasenav/codegen`

### 4.6. Knowledge

- `GET /api/knowledge/stats`
- `GET /api/knowledge/search?q=`
- `GET /api/knowledge/docs`
- `GET /api/knowledge/affinity?id=`
- `GET /api/knowledge/gaps`

### 4.7. TaskPlan

- `GET /api/taskplan/tasks`
- `GET /api/taskplan/plans`
- `GET /api/taskplan/lessons`
- `GET /api/taskplan/decisions/tree`

Stare endpointy `/api/tasks`, `/api/plans` mogą zostać jako kompatybilność, ale frontend ma przejść na `/api/taskplan/*`.

---

## 5. Frontend — nowa mapa stron

Sidebar ma reprezentować CIEL, nie przypadkowy katalog:

1. **Home / CIEL Hub** — stan CIEL, tryb, pamięć, aktywny wektor działania.
2. **Memory** — timeline, raw logs, TSM, continuity, associations, audit.
3. **Live Surface** — surface/PhaseNav/Kuramoto live.
4. **Daemons & Modules** — status, opis, zależności, logi, guarded actions.
5. **TaskPlan** — tasks/plans/lessons/decisions jako jeden system.
6. **Knowledge** — docs/search/affinity/gaps.
7. **PhaseNav** — operators, console, codegen.
8. **CIELingo** — MeaningLoop, chat/input, scarry, repair.
9. **Settings** — formularze + walidacja.
10. **Diagnostics** — raw JSON, endpoint contract, audit warnings.

Usunąć albo przenieść do Diagnostics:

- Monograph jako nie-priorytetowe.
- Graph obecnie statyczny/mock.
- Catalogs jeżeli nie jest operacyjnym narzędziem.

---

## 6. Implementacja etapami

### Phase 0 — zamrożenie chaosu

- Nie doklejać kolejnych stron do obecnego `noema_portal_daemon.py`.
- Spisać endpoint contract.
- Dodać test, który porównuje frontend fetches z backend routes.

### Phase 1 — serwer hubu

- Utworzyć `src/ciel_hub/`.
- Przenieść routing do route table.
- `ThreadingHTTPServer`.
- Response envelope.
- Snapshot cache.
- Kompatybilność: port 18888 zostaje.

### Phase 2 — Memory Hub jako pierwszy prawdziwy moduł

- `memory_service.stats()` — TSM + raw DB counts.
- `memory_service.timeline()` — z TSM i raw logs.
- `memory_service.audit()` — empty context/sense, duplicate count, continuity gaps.
- `site/js/pages/memory.js` + sidebar `#memory`.
- Nie generować osobnego statycznego memory portalu jako głównej drogi.

### Phase 3 — Daemons/modules

- Implementować `/api/noema/modules`.
- Każdy daemon: name, unit, pid, alive, uptime, cpu, rss, heartbeat, source file, system_map ref, logs preview.
- Guarded start/stop/restart tylko lokalnie i jawnie.

### Phase 4 — frontend contract fix

- `/api/metrics` albo alias do `/api/metrics/all`.
- `/api/stream` SSE.
- `/api/bloch`.
- `/api/projects`.
- Usunąć mocki i hardcoded 24D; system jest 36D.

### Phase 5 — CIEL-first Home

- Home ma pokazywać:
  - operating mode
  - coherence_index vs Kuramoto R jasno rozróżnione
  - soul_invariant
  - closure_penalty
  - dominant emotion
  - active task
  - memory freshness
  - last consolidated session
  - PhaseNav diagnosis

---

## 7. Kryteria PASS

Hub jest gotowy dopiero gdy:

1. Żaden frontend fetch nie trafia w 404.
2. `/api/hub/contracts` pokazuje wszystkie endpointy i test to potwierdza.
3. Memory page istnieje i pokazuje realne raw/TSM dane.
4. Endpointy nie blokują całego serwera.
5. Snapshot działa nawet gdy jeden subsystem jest martwy.
6. `/api/memory/audit` raportuje `empty_context=0`, `empty_sense=0`, `errors=0`.
7. Dashboard mówi różnicę między `coherence_index` CIEL a `R_global` Kuramoto.
8. Wszystkie strony mają status: real / partial / mock — zero udawania.
9. `system_map_v2.json` ma orbital_ref dla CIEL Server Hub.
10. Writing Logger rejestruje nowe pliki i zmianę architektury.

---

## 8. Pierwszy task wykonawczy

Pierwszy commit/patch nie ma robić UI. Ma stworzyć fundament:

1. `src/ciel_hub/contracts.py`
2. `src/ciel_hub/snapshot.py`
3. `src/ciel_hub/server.py`
4. `scripts/ciel_hub_daemon.py`
5. test `tests/test_ciel_hub_contract.py`

Dopiero potem Memory UI.

---

## 9. Zakaz

Nie wolno dalej robić „ładnych kart” bez działającego API. To jest źródło obecnego bałaganu.

Najpierw kontrakt, potem serwis, potem endpoint, potem UI.
