# generic_ops.py — .python_packages/mypyc/primitives/generic_ops.py

## Tożsamość
- **id_karty:** `REPO-GENERIC_OPS-D0BC`
- **ścieżka:** `.python_packages/mypyc/primitives/generic_ops.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.420`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/primitives/generic_ops.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.420 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Fallback primitive operations that operate on 'object' operands.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
Fallback primitive operations that operate on 'object' operands.

These just call the relevant Python C API function or a thin wrapper
around an API function. Most of these also have faster, specialized
ops that operate on some more specific types.

Many of these ops are given a low priority (0) so that specialized ops
will take precedence. If your specialized op doesn't seem to be used,
check tha
