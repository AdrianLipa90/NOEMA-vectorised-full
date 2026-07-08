# rtypes.py — .python_packages/mypyc/ir/rtypes.py

## Tożsamość
- **id_karty:** `REPO-RTYPES-E36C`
- **ścieżka:** `.python_packages/mypyc/ir/rtypes.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.432`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/ir/rtypes.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.432 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Types used in the intermediate representation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RType, RTypeVisitor, RVoid, RPrimitive, TupleNameVisitor, RTuple, RStruct, RInstance, RVec, RUnion, RArray
- **funkcje:** `deserialize_type`, `is_native_rprimitive`, `is_tagged`, `is_any_int`, `is_int_rprimitive`, `is_short_int_rprimitive`, `is_int16_rprimitive`, `is_int32_rprimitive`, `is_int64_rprimitive`, `is_fixed_width_rtype`, `is_uint8_rprimitive`, `is_uint32_rprimitive`, `is_uint64_rprimitive`, `is_c_py_ssize_t_rprimitive`, `is_pointer_rprimitive`, `is_float_rprimitive`, `is_bool_rprimitive`, `is_bit_rprimitive`, `is_bool_or_bit_rprimitive`, `is_object_rprimitive`, `is_none_rprimitive`, `is_list_rprimitive`, `is_dict_rprimitive`, `is_set_rprimitive`, `is_frozenset_rprimitive`, `is_str_rprimitive`, `is_bytes_rprimitive`, `is_bytearray_rprimitive`, `is_tuple_rprimitive`, `is_range_rprimitive`

## Opis
Types used in the intermediate representation.

These are runtime types (RTypes), as opposed to mypy Type objects.
The latter are only used during type checking and not directly used at
runtime.  Runtime types are derived from mypy types, but there's no
simple one-to-one correspondence. (Here 'runtime' means 'runtime
checked'.)

The generated IR ensures some runtime type safety properties based on
