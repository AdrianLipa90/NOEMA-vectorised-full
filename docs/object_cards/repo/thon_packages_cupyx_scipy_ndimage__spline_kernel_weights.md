# _spline_kernel_weights.py — .python_packages/cupyx/scipy/ndimage/_spline_kernel_weights.py

## Tożsamość
- **id_karty:** `REPO-_SPLINE_KERNEL_WEIGH-93A7`
- **ścieżka:** `.python_packages/cupyx/scipy/ndimage/_spline_kernel_weights.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.361`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cupyx/scipy/ndimage/_spline_kernel_weights.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.361 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Determination of spline kernel weights (adapted from SciPy)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
Determination of spline kernel weights (adapted from SciPy)

See more verbose comments for each case there:
https://github.com/scipy/scipy/blob/eba29d69846ab1299976ff4af71c106188397ccc/scipy/ndimage/src/ni_splines.c#L7

``spline_weights_inline`` is a dict where the key is the spline order and the
value is the spline weight initialization code.
