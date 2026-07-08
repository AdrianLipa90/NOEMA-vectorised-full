# activation.py — .python_packages/sympy/physics/biomechanics/activation.py

## Tożsamość
- **id_karty:** `REPO-ACTIVATION-9FCB`
- **ścieżka:** `.python_packages/sympy/physics/biomechanics/activation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.468`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/biomechanics/activation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.468 |
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
Activation dynamics for musclotendon models.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ActivationBase, ZerothOrderActivation, FirstOrderActivationDeGroote2016
- **funkcje:** `with_defaults`, `excitation`, `e`, `activation`, `a`, `order`, `state_vars`, `x`, `input_vars`, `r`, `constants`, `p`, `M`, `F`, `rhs`, `with_defaults`, `order`, `state_vars`, `x`, `input_vars`, `r`, `constants`, `p`, `M`, `F`, `rhs`, `with_defaults`, `activation_time_constant`, `activation_time_constant`, `tau_a`

## Opis
Activation dynamics for musclotendon models.

Musculotendon models are able to produce active force when they are activated,
which is when a chemical process has taken place within the muscle fibers
causing them to voluntarily contract. Biologically this chemical process (the
diffusion of :math:`\textrm{Ca}^{2+}` ions) is not the input in the system,
electrical signals from the nervous system are.
