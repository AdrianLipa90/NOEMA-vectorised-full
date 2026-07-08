# trf.py — .python_packages/scipy/optimize/_lsq/trf.py

## Tożsamość
- **id_karty:** `REPO-TRF-6DE8`
- **ścieżka:** `.python_packages/scipy/optimize/_lsq/trf.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.045`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_lsq/trf.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.045 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Trust Region Reflective algorithm for least-squares optimization.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `trf`, `select_step`, `trf_bounds`, `trf_no_bounds`

## Opis
Trust Region Reflective algorithm for least-squares optimization.

The algorithm is based on ideas from paper [STIR]_. The main idea is to
account for the presence of the bounds by appropriate scaling of the variables (or,
equivalently, changing a trust-region shape). Let's introduce a vector v:

           | ub[i] - x[i], if g[i] < 0 and ub[i] < np.inf
    v[i] = | x[i] - lb[i], if g[i] > 0 and l
