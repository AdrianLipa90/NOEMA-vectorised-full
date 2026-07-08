# _byteordercodes.py — .python_packages/scipy/io/matlab/_byteordercodes.py

## Tożsamość
- **id_karty:** `REPO-_BYTEORDERCODES-BE5F`
- **ścieżka:** `.python_packages/scipy/io/matlab/_byteordercodes.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.910`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/matlab/_byteordercodes.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.910 |
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
Byteorder utilities for system - numpy byteorder encoding

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `to_numpy_code`

## Opis
Byteorder utilities for system - numpy byteorder encoding

Converts a variety of string codes for little endian, big endian,
native byte order and swapped byte order to explicit NumPy endian
codes - one of '<' (little endian) or '>' (big endian)
