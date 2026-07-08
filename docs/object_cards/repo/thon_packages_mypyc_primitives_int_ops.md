# int_ops.py — .python_packages/mypyc/primitives/int_ops.py

## Tożsamość
- **id_karty:** `REPO-INT_OPS-7CC4`
- **ścieżka:** `.python_packages/mypyc/primitives/int_ops.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.010`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/primitives/int_ops.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.010 |
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
Arbitrary-precision integer primitive ops.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `int_binary_primitive`, `int_binary_op`, `int_unary_op`

## Opis
Arbitrary-precision integer primitive ops.

These mostly operate on (usually) unboxed integers that use a tagged pointer
representation (CPyTagged) and correspond to the Python 'int' type.

See also the documentation for mypyc.rtypes.int_rprimitive.

Use mypyc.ir.ops.IntOp for operations on fixed-width/C integers.
