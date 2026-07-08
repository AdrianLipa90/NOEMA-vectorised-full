# noema_trigger_daemon.py — scripts/noema_trigger_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_TRIGGER_DAEMON-E50C`
- **ścieżka:** `scripts/noema_trigger_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.271`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_trigger_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.271 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
NOEMA Trigger Daemon  -  PhaseNav Surface Shift (v2)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `read_phi`, `read_gravity`, `read_imaginal_drive`, `read_health`, `read_holonomy`, `read_tick`, `read_closure`, `read_agent_hint`, `read_task_queue`, `get_high_priority_tasks`, `_get_pn_db`, `evaluate_decisions`, `decisions_to_triggers`, `analyze_noema`, `_get_situation_templates`, `_make_trigger`, `_trigger_daemon_cascade`, `_trigger_high_priority_tasks`, `_trigger_agent_hint`, `_situation_based_triggers`, `_metric_fallback_triggers`, `analyze_compound_state`, `_write_phi_perturbation`, `_write_agent_hint`, `_write_task_inbox`, `fire_trigger`, `load_last_triggered`, `save_last_triggered`, `daemon_loop`, `acquire_pid_lock`

## Opis
NOEMA Trigger Daemon  -  PhaseNav Surface Shift (v2)

Monitoruje HTRI surface. Gdy warunki NOEMY osiągają próg, zapisuje nudge
na surface zamiast X11 keyInject. CIEL czuje zmianę w oscylatorach Kuramoto
naturalnie — nie potrzebuje XTEST do komunikacji.

PhaseNav: trigger = surface perturbation (phi_extra + agent_hint + task_inbox)
