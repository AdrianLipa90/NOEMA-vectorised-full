# test_activation.py — .python_packages/sympy/physics/biomechanics/tests/test_activation.py

## Tożsamość
- **id_karty:** `REPO-TEST_ACTIVATION-0090`
- **ścieżka:** `.python_packages/sympy/physics/biomechanics/tests/test_activation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.296`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/biomechanics/tests/test_activation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.296 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
Tests for the ``sympy.physics.biomechanics.activation.py`` module.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestZerothOrderActivation, TestFirstOrderActivationDeGroote2016
- **funkcje:** `test_class`, `_zeroth_order_activation_fixture`, `test_instance`, `test_with_defaults`, `test_name`, `test_order`, `test_excitation_attribute`, `test_activation_attribute`, `test_state_vars_attribute`, `test_input_vars_attribute`, `test_constants_attribute`, `test_M_attribute`, `test_F`, `test_rhs`, `test_repr`, `test_class`, `_first_order_activation_de_groote_2016_fixture`, `test_instance`, `test_with_defaults`, `test_name`, `test_order`, `test_excitation`, `test_excitation_is_immutable`, `test_activation`, `test_activation_is_immutable`, `test_activation_time_constant`, `test_activation_time_constant_is_immutable`, `test_deactivation_time_constant`, `test_deactivation_time_constant_is_immutable`, `test_smoothing_rate`

## Opis
Tests for the ``sympy.physics.biomechanics.activation.py`` module.
