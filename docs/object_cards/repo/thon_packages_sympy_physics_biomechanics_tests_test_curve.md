# test_curve.py — .python_packages/sympy/physics/biomechanics/tests/test_curve.py

## Tożsamość
- **id_karty:** `REPO-TEST_CURVE-7DC1`
- **ścieżka:** `.python_packages/sympy/physics/biomechanics/tests/test_curve.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.479`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/biomechanics/tests/test_curve.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.479 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Tests for the ``sympy.physics.biomechanics.characteristic.py`` module.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestCharacteristicCurveFunction, TestTendonForceLengthDeGroote2016, TestTendonForceLengthInverseDeGroote2016, TestFiberForceLengthPassiveDeGroote2016, TestFiberForceLengthPassiveInverseDeGroote2016, TestFiberForceLengthActiveDeGroote2016, TestFiberForceVelocityDeGroote2016, TestFiberForceVelocityInverseDeGroote2016, TestCharacteristicCurveCollection, ExampleFunction
- **funkcje:** `test_print_code_parenthesize`, `_tendon_force_length_arguments_fixture`, `test_class`, `test_instance`, `test_doit`, `test_doit_evaluate_false`, `test_with_defaults`, `test_differentiate_wrt_l_T_tilde`, `test_differentiate_wrt_c0`, `test_differentiate_wrt_c1`, `test_differentiate_wrt_c2`, `test_differentiate_wrt_c3`, `test_inverse`, `test_function_print_latex`, `test_expression_print_latex`, `test_print_code`, `test_derivative_print_code`, `test_lambdify`, `test_lambdify_numpy`, `test_lambdify_jax`, `_tendon_force_length_inverse_arguments_fixture`, `test_class`, `test_instance`, `test_doit`, `test_doit_evaluate_false`, `test_with_defaults`, `test_differentiate_wrt_fl_T`, `test_differentiate_wrt_c0`, `test_differentiate_wrt_c1`, `test_differentiate_wrt_c2`

## Opis
Tests for the ``sympy.physics.biomechanics.characteristic.py`` module.
