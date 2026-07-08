# actuator.py — .python_packages/sympy/physics/mechanics/actuator.py

## Tożsamość
- **id_karty:** `REPO-ACTUATOR-9DB6`
- **ścieżka:** `.python_packages/sympy/physics/mechanics/actuator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.192`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/mechanics/actuator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.192 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Implementations of actuators for linked force and torque application.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ActuatorBase, ForceActuator, LinearSpring, LinearDamper, TorqueActuator, DuffingSpring, CoulombKineticFriction
- **funkcje:** `to_loads`, `force`, `force`, `pathway`, `pathway`, `to_loads`, `force`, `force`, `stiffness`, `stiffness`, `equilibrium_length`, `equilibrium_length`, `force`, `force`, `damping`, `damping`, `at_pin_joint`, `torque`, `torque`, `axis`, `axis`, `target_frame`, `target_frame`, `reaction_frame`, `reaction_frame`, `to_loads`, `linear_stiffness`, `linear_stiffness`, `nonlinear_stiffness`, `nonlinear_stiffness`

## Opis
Implementations of actuators for linked force and torque application.
