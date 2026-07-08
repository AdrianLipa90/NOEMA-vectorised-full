# _complexstuff.py — .python_packages/cupyx/scipy/special/_complexstuff.py

## Tożsamość
- **id_karty:** `REPO-_COMPLEXSTUFF-8CB1`
- **ścieżka:** `.python_packages/cupyx/scipy/special/_complexstuff.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.057`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cupyx/scipy/special/_complexstuff.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.057 |
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
complex-valued functions adapted from SciPy's cython code:

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
complex-valued functions adapted from SciPy's cython code:

https://github.com/scipy/scipy/blob/master/scipy/special/_complexstuff.pxd

Notes:
- instead of zabs, use thrust::abs
- instead of zarg, use thrust::arg
- instead of zcos, use thrust::cos
- instead of zexp, use thrust::exp
- instead of zisfinite, use isfinite defined in _core/include/cupy/complex.cuh
- instead of zisinf, use isinf defined
