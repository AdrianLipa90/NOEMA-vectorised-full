# event.py — .python_packages/numba/core/event.py

## Tożsamość
- **id_karty:** `REPO-EVENT-D1F1`
- **ścieżka:** `.python_packages/numba/core/event.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.726`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/event.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.726 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
The ``numba.core.event`` module provides a simple event system for applications

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EventStatus, Event, Listener, TimingListener, RecordingListener
- **funkcje:** `_guard_kind`, `register`, `unregister`, `broadcast`, `install_listener`, `install_timer`, `install_recorder`, `start_event`, `end_event`, `trigger_event`, `_prepare_chrome_trace_data`, `_setup_chrome_trace_exit_handler`, `kind`, `status`, `data`, `is_start`, `is_end`, `is_failed`, `on_start`, `on_end`, `notify`, `on_start`, `on_end`, `done`, `duration`, `on_start`, `on_end`, `_write_chrome_trace`, `on_exit`

## Opis
The ``numba.core.event`` module provides a simple event system for applications
to register callbacks to listen to specific compiler events.

The following events are built in:

- ``"numba:compile"`` is broadcast when a dispatcher is compiling. Events of
  this kind have ``data`` defined to be a ``dict`` with the following
  key-values:

  - ``"dispatcher"``: the dispatcher object that is compilin
