# dispatcher.py — .python_packages/werkzeug/middleware/dispatcher.py

## Tożsamość
- **id_karty:** `REPO-DISPATCHER-0DA6`
- **ścieżka:** `.python_packages/werkzeug/middleware/dispatcher.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.083`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/werkzeug/middleware/dispatcher.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.083 |
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
Application Dispatcher

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DispatcherMiddleware
- **funkcje:** —

## Opis
Application Dispatcher
======================

This middleware creates a single WSGI application that dispatches to
multiple other WSGI applications mounted at different URL paths.

A common example is writing a Single Page Application, where you have a
backend API and a frontend written in JavaScript that does the routing
in the browser rather than requesting different pages from the server.
The
