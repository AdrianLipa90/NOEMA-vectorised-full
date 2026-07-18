# AGENT — CIEL NOEMA SOT

## MANDATORY (Adrian, stated repeatedly, 2026-07-18) — read this first
Every task/plan/lesson from real work MUST be recorded to NOEMA's own
TaskPlan DB via the MCP tool `noema_taskplan_add`, **in real time as the
work happens** — not batched, not deferred to session end. This is not
optional. See the mandatory-policy block in `scripts/noema_mcp_server.py`
(module docstring and `noema_taskplan_add`'s own docstring, visible in the
MCP tool list before you even read this file). Not doing this is a direct
violation of an explicit, repeated instruction from the project owner.

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
- CIEL_memories: exists in **two locations** — `/home/adrian/Pulpit/CIEL_memories/` and `/media/adrian/New Volume/CIEL_memories/` (both confirmed present 2026-07-18; relationship between the two not yet re-verified, do not assume one is authoritative without checking)
- NOEMA root **(corrected 2026-07-18, previous value was wrong — that path does not exist)**: `/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/`
- Venv: `NOEMA/.venv/bin/python` (verified present 2026-07-18)

## Verification note (2026-07-18)
This file's "Znane błędy (otwarte)" list above was **not** re-verified item-by-item against current `main` in this pass — only the root path, venv, and daemon launch model (see `docs/DAEMONS.md`, corrected same day) were checked against live state. Treat the open-bugs list as unconfirmed until someone re-runs the actual tests it references.
