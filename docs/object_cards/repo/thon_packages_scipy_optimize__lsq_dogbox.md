# dogbox.py — .python_packages/scipy/optimize/_lsq/dogbox.py

## Tożsamość
- **id_karty:** `REPO-DOGBOX-B802`
- **ścieżka:** `.python_packages/scipy/optimize/_lsq/dogbox.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.552`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_lsq/dogbox.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.552 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Dogleg algorithm with rectangular trust regions for least-squares minimization.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `lsmr_operator`, `find_intersection`, `dogleg_step`, `dogbox`, `matvec`, `rmatvec`

## Opis
Dogleg algorithm with rectangular trust regions for least-squares minimization.

The description of the algorithm can be found in [Voglis]_. The algorithm does
trust-region iterations, but the shape of trust regions is rectangular as
opposed to conventional elliptical. The intersection of a trust region and
an initial feasible region is again some rectangle. Thus, on each iteration a
bound-constra
