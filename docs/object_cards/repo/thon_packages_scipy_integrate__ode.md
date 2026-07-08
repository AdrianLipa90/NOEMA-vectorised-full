# _ode.py — .python_packages/scipy/integrate/_ode.py

## Tożsamość
- **id_karty:** `REPO-_ODE-AEB9`
- **ścieżka:** `.python_packages/scipy/integrate/_ode.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.517`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/integrate/_ode.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.517 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
First-order ODE integrators.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ode, complex_ode, IntegratorConcurrencyError, IntegratorBase, vode, zvode, dopri5, dop853, lsoda
- **funkcje:** `_transform_banded_jac`, `find_integrator`, `y`, `set_initial_value`, `set_integrator`, `integrate`, `successful`, `get_return_code`, `set_f_params`, `set_jac_params`, `set_solout`, `_wrap`, `_wrap_jac`, `y`, `set_integrator`, `set_initial_value`, `integrate`, `set_solout`, `acquire_new_handle`, `check_handle`, `reset`, `run`, `step`, `run_relax`, `_determine_mf_and_set_bands`, `reset`, `run`, `step`, `run_relax`, `reset`

## Opis
First-order ODE integrators.

User-friendly interface to various numerical integrators for solving a
system of first order ODEs with prescribed initial conditions::

    d y(t)[i]
    ---------  = f(t,y(t))[i],
       d t

    y(t=0)[i] = y0[i],

where::

    i = 0, ..., len(y0) - 1

class ode
---------

A generic interface class to numeric integrators. It has the following
methods::

    integrat
