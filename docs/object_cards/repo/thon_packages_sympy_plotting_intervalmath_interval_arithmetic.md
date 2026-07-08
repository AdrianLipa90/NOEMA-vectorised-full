# interval_arithmetic.py — .python_packages/sympy/plotting/intervalmath/interval_arithmetic.py

## Tożsamość
- **id_karty:** `REPO-INTERVAL_ARITHMETIC-C045`
- **ścieżka:** `.python_packages/sympy/plotting/intervalmath/interval_arithmetic.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.407`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/plotting/intervalmath/interval_arithmetic.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.407 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Interval Arithmetic for plotting.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** interval
- **funkcje:** `_pow_float`, `_pow_int`, `mid`, `width`

## Opis
Interval Arithmetic for plotting.
This module does not implement interval arithmetic accurately and
hence cannot be used for purposes other than plotting. If you want
to use interval arithmetic, use mpmath's interval arithmetic.

The module implements interval arithmetic using numpy and
python floating points. The rounding up and down is not handled
and hence this is not an accurate implementation
