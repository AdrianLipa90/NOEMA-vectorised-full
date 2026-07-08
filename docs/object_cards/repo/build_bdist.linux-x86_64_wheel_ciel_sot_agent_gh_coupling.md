# gh_coupling.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/gh_coupling.py

## Tożsamość
- **id_karty:** `REPO-GH_COUPLING-BAB6`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/gh_coupling.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.249`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/gh_coupling.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.249 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
GitHub coupling subsystem (v1) — live upstream-aware phase coupling.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `build_live_coupling`, `main`

## Opis
GitHub coupling subsystem (v1) — live upstream-aware phase coupling.

Fetches current upstream HEAD SHAs for registered repositories, propagates
phase shifts through the coupling map, and emits a refreshed JSON coupling
report.  Invoked via the ``ciel-sot-gh-coupling`` console script.
