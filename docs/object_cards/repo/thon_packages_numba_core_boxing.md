# boxing.py — .python_packages/numba/core/boxing.py

## Tożsamość
- **id_karty:** `REPO-BOXING-EE87`
- **ścieżka:** `.python_packages/numba/core/boxing.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.675`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/boxing.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.675 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Boxing and unboxing of native Numba values to / from CPython objects.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _NumbaTypeHelper
- **funkcje:** `box_bool`, `unbox_boolean`, `box_literal_integer`, `box_integer`, `unbox_integer`, `box_float`, `unbox_float`, `box_complex`, `unbox_complex`, `box_none`, `unbox_none`, `box_npdatetime`, `unbox_npdatetime`, `box_nptimedelta`, `unbox_nptimedelta`, `box_raw_pointer`, `box_enum`, `unbox_enum`, `box_undefvar`, `box_record`, `unbox_record`, `box_unicodecharseq`, `unbox_unicodecharseq`, `box_bytes`, `box_charseq`, `unbox_charseq`, `box_optional`, `unbox_optional`, `unbox_slice`, `box_slice_literal`

## Opis
Boxing and unboxing of native Numba values to / from CPython objects.
