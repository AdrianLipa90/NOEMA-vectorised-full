# int_ops.py — .python_packages/mypyc/lower/int_ops.py

## Tożsamość
- **id_karty:** `REPO-INT_OPS-ED6A`
- **ścieżka:** `.python_packages/mypyc/lower/int_ops.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.908`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/lower/int_ops.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.908 |
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
Convert tagged int primitive ops to lower-level ops.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** IntComparisonOpDescription
- **funkcje:** `compare_tagged`, `lower_int_eq`, `lower_int_ne`, `lower_int_lt`, `lower_int_le`, `lower_int_gt`, `lower_int_ge`

## Opis
Convert tagged int primitive ops to lower-level ops.
