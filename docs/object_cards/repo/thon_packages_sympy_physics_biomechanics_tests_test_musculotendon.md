# test_musculotendon.py — .python_packages/sympy/physics/biomechanics/tests/test_musculotendon.py

## Tożsamość
- **id_karty:** `REPO-TEST_MUSCULOTENDON-D1DB`
- **ścieżka:** `.python_packages/sympy/physics/biomechanics/tests/test_musculotendon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.056`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/biomechanics/tests/test_musculotendon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.056 |
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
Tests for the ``sympy.physics.biomechanics.musculotendon.py`` module.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestMusculotendonFormulation, TestMusculotendonBase, TestMusculotendonRigidTendon, TestFiberLengthExplicit, TestTendonForceExplicit, TestMusculotendonDeGroote2016
- **funkcje:** `test_rigid_tendon_member`, `test_fiber_length_explicit_member`, `test_tendon_force_explicit_member`, `test_fiber_length_implicit_member`, `test_tendon_force_implicit_member`, `test_is_abstract_base_class`, `test_class`, `test_cannot_instantiate_directly`, `_musculotendon_rigid_tendon_fixture`, `test_state_vars`, `test_input_vars`, `test_constants`, `test_M`, `test_F`, `test_rhs`, `_musculotendon_fiber_length_explicit_fixture`, `test_state_vars`, `test_input_vars`, `test_constants`, `test_M`, `test_F`, `test_rhs`, `_musculotendon_tendon_force_explicit_fixture`, `test_state_vars`, `test_input_vars`, `test_constants`, `test_M`, `test_F`, `test_rhs`, `test_class`

## Opis
Tests for the ``sympy.physics.biomechanics.musculotendon.py`` module.
