# _windows.py — .python_packages/cupyx/scipy/signal/windows/_windows.py

## Tożsamość
- **id_karty:** `REPO-_WINDOWS-131E`
- **ścieżka:** `.python_packages/cupyx/scipy/signal/windows/_windows.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.946`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cupyx/scipy/signal/windows/_windows.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.946 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Filtering and spectral estimation windows.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_len_guards`, `_extend`, `_truncate`, `general_cosine`, `boxcar`, `triang`, `parzen`, `bohman`, `blackman`, `nuttall`, `blackmanharris`, `flattop`, `bartlett`, `hann`, `tukey`, `barthann`, `general_hamming`, `hamming`, `kaiser`, `kaiser_bessel_derived`, `gaussian`, `general_gaussian`, `chebwin`, `cosine`, `exponential`, `taylor`, `lanczos`, `_fftautocorr`, `get_window`, `_calc_right_side_lanczos`

## Opis
Filtering and spectral estimation windows.

Some of the functions defined on this namespace were ported directly
from CuSignal under terms of the MIT license.
