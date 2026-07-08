# AGENT — CIEL NOEMA SOT

## Stan systemu (2026-06-23)
- **NOEMA** = Source of Truth (SOT)
- CIELINGO_CANON = podzbiór lingwistyczny, nie SOT
- CIEL_memories = `~/Pulpit/CIEL_memories/`
- Package `ciel-sot-agent` **zainstalowany** w `.venv/` (PEP 668)
- Warstwy pamięci: NOEMA 3.4 GB, CIELINGO 48 MB, TIR 876 KB, CIEL_memories 572 KB, repo stages 55 MB

## Architektura
- `ciel_coupling.process_user_input()` — bezpośrednie API, bez I/O
- `ciel_monitor.py` — daemon monitora (socket: ~/.ciel/monitor.sock)
- `ciel_session_hook.py` — SessionStart hook
- `ciel.sh` — wrapper + monitor + shell
- `cielingo_bridge.build_lingo_frame()` — CIELingo enrichment każdego promptu

## Znane błędy (naprawione)
- ~~1. DEFAULT_OSCILLATORS = 24 vs testy 120 — parametryzacja~~
- ~~2. CLI scripts nie widzą cielingo (PYTHONPATH subprocess) — dodany PYTHONPATH w test_main.py~~
- ~~8. Import cycle noema_bootstrap vs src.ciel_sot_agent — dynamiczny sys.path w __init__.py~~

## Znane błędy (otwarte)
3. Brakujące pip: scipy, h5py, flask, numba, cupy — **ZAINSTALOWANE** w `.venv/`
4. Monitor daemon — socket connection refused (engine init timeout)
5. ciel_secret_loader szuka ~/Pulpit/CIEL_memories/secrets/cielapi
6. sqlite3 nie zainstalowany do odczytu ciel_state.db
7. test_gui.py — Flask app context poza kontekstem (27 testów)
8. test_orbital_regression.py — hangs (timeout 30s)
9. test_sapiens_client_packet.py — hangs (timeout 15s)
10. test_sapiens_panel.py — hangs (timeout 15s)
11. test_noema_file_sense.py — hangs (timeout 15s)

## Stale
- HTRI: freq=7.83Hz, osc=24 (NOEMA) / 780 (runtime daemon)
- CIEL_memories: ~/Pulpit/CIEL_memories/
- NOEMA root: /home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/
- Venv: `NOEMA/.venv/bin/python`
