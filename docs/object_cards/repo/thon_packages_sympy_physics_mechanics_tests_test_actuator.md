# test_actuator.py — .python_packages/sympy/physics/mechanics/tests/test_actuator.py

## Tożsamość
- **id_karty:** `REPO-TEST_ACTUATOR-DD2D`
- **ścieżka:** `.python_packages/sympy/physics/mechanics/tests/test_actuator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.350`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/mechanics/tests/test_actuator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.350 |
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
Tests for the ``sympy.physics.mechanics.actuator.py`` module.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestForceActuator, TestLinearSpring, TestLinearDamper, TestForcedMassSpringDamperModel, TestTorqueActuator, NonSympifyable, TestDuffingSpring, TestCoulombKineticFriction
- **funkcje:** `_linear_pathway_fixture`, `test_is_actuator_base_subclass`, `test_valid_constructor_force`, `test_invalid_constructor_force_not_sympifyable`, `test_valid_constructor_pathway`, `test_invalid_constructor_pathway_not_pathway_base`, `test_properties_are_immutable`, `test_repr`, `test_to_loads_static_pathway`, `test_to_loads_2D_pathway`, `test_to_loads_3D_pathway`, `_linear_spring_fixture`, `test_is_force_actuator_subclass`, `test_is_actuator_base_subclass`, `test_valid_constructor`, `test_invalid_constructor_stiffness_not_sympifyable`, `test_invalid_constructor_pathway_not_pathway_base`, `test_invalid_constructor_equilibrium_length_not_sympifyable`, `test_properties_are_immutable`, `test_repr`, `test_to_loads`, `_linear_damper_fixture`, `test_is_force_actuator_subclass`, `test_is_actuator_base_subclass`, `test_valid_constructor`, `test_valid_constructor_force`, `test_invalid_constructor_damping_not_sympifyable`, `test_invalid_constructor_pathway_not_pathway_base`, `test_properties_are_immutable`, `test_repr`

## Opis
Tests for the ``sympy.physics.mechanics.actuator.py`` module.
