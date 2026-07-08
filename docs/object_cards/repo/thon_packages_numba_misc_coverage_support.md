# coverage_support.py — .python_packages/numba/misc/coverage_support.py

## Tożsamość
- **id_karty:** `REPO-COVERAGE_SUPPORT-6A58`
- **ścieżka:** `.python_packages/numba/misc/coverage_support.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.936`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/misc/coverage_support.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.936 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Implement code coverage support.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NotifyLocBase, NotifyCompilerCoverage, NumbaTracer
- **funkcje:** `get_active_coverage`, `get_registered_loc_notify`, `_register_coverage_notifier`, `notify`, `close`, `notify`, `close`, `_pack_arcs`, `start`, `stop`, `activity`, `reset_activity`, `get_stats`, `trace`

## Opis
Implement code coverage support.

Currently contains logic to extend ``coverage`` with lines covered by the
compiler.
