# _cubic.py — .python_packages/scipy/interpolate/_cubic.py

## Tożsamość
- **id_karty:** `REPO-_CUBIC-2B62`
- **ścieżka:** `.python_packages/scipy/interpolate/_cubic.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.241`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/interpolate/_cubic.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.241 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Interpolation algorithms using piecewise cubic polynomials.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CubicHermiteSpline, PchipInterpolator, Akima1DInterpolator, CubicSpline
- **funkcje:** `prepare_input`, `pchip_interpolate`, `_edge_case`, `_find_derivatives`, `extend`, `from_spline`, `from_bernstein_basis`, `_validate_bc`

## Opis
Interpolation algorithms using piecewise cubic polynomials.
