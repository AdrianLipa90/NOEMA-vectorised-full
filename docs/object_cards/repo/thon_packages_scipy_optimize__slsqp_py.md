# _slsqp_py.py — .python_packages/scipy/optimize/_slsqp_py.py

## Tożsamość
- **id_karty:** `REPO-_SLSQP_PY-85A9`
- **ścieżka:** `.python_packages/scipy/optimize/_slsqp_py.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.897`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_slsqp_py.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.897 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
This module implements the Sequential Least Squares Programming optimization

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `approx_jacobian`, `fmin_slsqp`, `_minimize_slsqp`, `_eval_constraint`, `_eval_con_normals`, `cjac_factory`, `cjac`

## Opis
This module implements the Sequential Least Squares Programming optimization
algorithm (SLSQP), originally developed by Dieter Kraft.
See http://www.netlib.org/toms/733

Functions
---------
.. autosummary::
   :toctree: generated/

    approx_jacobian
    fmin_slsqp
