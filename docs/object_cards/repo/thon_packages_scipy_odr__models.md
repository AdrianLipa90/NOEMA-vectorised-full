# _models.py — .python_packages/scipy/odr/_models.py

## Tożsamość
- **id_karty:** `REPO-_MODELS-7C34`
- **ścieżka:** `.python_packages/scipy/odr/_models.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.248`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/odr/_models.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.248 |
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
Collection of Model instances for use with the odrpack fitting package.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _MultilinearModel, _ExponentialModel, _UnilinearModel, _QuadraticModel
- **funkcje:** `_lin_fcn`, `_lin_fjb`, `_lin_fjd`, `_lin_est`, `_poly_fcn`, `_poly_fjacb`, `_poly_fjacd`, `_exp_fcn`, `_exp_fjd`, `_exp_fjb`, `_exp_est`, `polynomial`, `_unilin`, `_unilin_fjd`, `_unilin_fjb`, `_unilin_est`, `_quadratic`, `_quad_fjd`, `_quad_fjb`, `_quad_est`, `_poly_est`

## Opis
Collection of Model instances for use with the odrpack fitting package.
