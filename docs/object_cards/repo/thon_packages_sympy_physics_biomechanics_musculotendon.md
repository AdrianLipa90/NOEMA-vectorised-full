# musculotendon.py — .python_packages/sympy/physics/biomechanics/musculotendon.py

## Tożsamość
- **id_karty:** `REPO-MUSCULOTENDON-7D4D`
- **ścieżka:** `.python_packages/sympy/physics/biomechanics/musculotendon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.872`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/biomechanics/musculotendon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.872 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Implementations of musculotendon models.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MusculotendonFormulation, MusculotendonBase, MusculotendonDeGroote2016
- **funkcje:** `with_defaults`, `curves`, `tendon_slack_length`, `l_T_slack`, `peak_isometric_force`, `F_M_max`, `optimal_fiber_length`, `l_M_opt`, `maximal_fiber_velocity`, `v_M_max`, `optimal_pennation_angle`, `alpha_opt`, `fiber_damping_coefficient`, `beta`, `activation_dynamics`, `excitation`, `e`, `activation`, `a`, `musculotendon_dynamics`, `_rigid_tendon_musculotendon_dynamics`, `_fiber_length_explicit_musculotendon_dynamics`, `_tendon_force_explicit_musculotendon_dynamics`, `_fiber_length_implicit_musculotendon_dynamics`, `_tendon_force_implicit_musculotendon_dynamics`, `state_vars`, `x`, `input_vars`, `r`, `constants`

## Opis
Implementations of musculotendon models.

Musculotendon models are a critical component of biomechanical models, one that
differentiates them from pure multibody systems. Musculotendon models produce a
force dependent on their level of activation, their length, and their
extension velocity. Length- and extension velocity-dependent force production
are governed by force-length and force-velocity ch
