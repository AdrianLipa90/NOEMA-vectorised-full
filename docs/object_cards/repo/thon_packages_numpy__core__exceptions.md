# _exceptions.py — .python_packages/numpy/_core/_exceptions.py

## Tożsamość
- **id_karty:** `REPO-_EXCEPTIONS-2EBB`
- **ścieżka:** `.python_packages/numpy/_core/_exceptions.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.914`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/_core/_exceptions.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.914 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
Various richly-typed exceptions, that also help us deal with string formatting

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UFuncTypeError, _UFuncNoLoopError, _UFuncBinaryResolutionError, _UFuncCastingError, _UFuncInputCastingError, _UFuncOutputCastingError, _ArrayMemoryError
- **funkcje:** `_unpack_tuple`, `_display_as_base`, `_total_size`, `_size_to_string`

## Opis
Various richly-typed exceptions, that also help us deal with string formatting
in python where it's easier.

By putting the formatting in `__str__`, we also avoid paying the cost for
users who silence the exceptions.
