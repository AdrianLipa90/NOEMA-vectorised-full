# refcount.py — .python_packages/mypyc/transform/refcount.py

## Tożsamość
- **id_karty:** `REPO-REFCOUNT-921A`
- **ścieżka:** `.python_packages/mypyc/transform/refcount.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.038`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/transform/refcount.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.038 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
Transformation for inserting refrecence count inc/dec opcodes.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `insert_ref_count_opcodes`, `is_maybe_undefined`, `maybe_append_dec_ref`, `maybe_append_inc_ref`, `transform_block`, `insert_branch_inc_and_decrefs`, `after_branch_decrefs`, `after_branch_increfs`, `add_block`, `make_value_ordering`

## Opis
Transformation for inserting refrecence count inc/dec opcodes.

This transformation happens towards the end of compilation. Before this
transformation, reference count management is not explicitly handled at all.
By postponing this pass, the previous passes are simpler as they don't have
to update reference count opcodes.

The approach is to decrement reference counts soon after a value is no
long
