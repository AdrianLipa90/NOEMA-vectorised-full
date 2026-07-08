# test_asnumbatype.py — .python_packages/numba/tests/test_asnumbatype.py

## Tożsamość
- **id_karty:** `REPO-TEST_ASNUMBATYPE-426C`
- **ścieżka:** `.python_packages/numba/tests/test_asnumbatype.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.866`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_asnumbatype.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.866 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
Tests for the as_numba_type() machinery.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestAsNumbaType, MyInt, bfloat16, _type_class_bfloat16, _model_bfloat16
- **funkcje:** `test_simple_types`, `test_numba_types`, `test_single_containers`, `test_optional`, `test_nested_containers`, `test_jitclass_registers`, `test_type_alias`, `test_overwrite_type`, `test_any_throws`, `test_bad_union_throws`, `test_instance_check_usecase`, `typeof_bfloat16`, `unbox_bfloat16`, `type_bfloat16_ctor`, `instancecheck_no_ant_reg`, `instancecheck`, `typer`

## Opis
Tests for the as_numba_type() machinery.
