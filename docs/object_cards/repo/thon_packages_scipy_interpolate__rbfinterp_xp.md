# _rbfinterp_xp.py — .python_packages/scipy/interpolate/_rbfinterp_xp.py

## Tożsamość
- **id_karty:** `REPO-_RBFINTERP_XP-EC8B`
- **ścieżka:** `.python_packages/scipy/interpolate/_rbfinterp_xp.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.459`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/interpolate/_rbfinterp_xp.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.459 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
'Generic' Array API backend for RBF interpolation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_monomial_powers`, `_build_and_solve_system`, `linear`, `thin_plate_spline`, `cubic`, `quintic`, `multiquadric`, `inverse_multiquadric`, `inverse_quadratic`, `gaussian`, `kernel_matrix`, `polynomial_matrix`, `_build_system`, `_build_evaluation_coefficients`, `compute_interpolation`

## Opis
'Generic' Array API backend for RBF interpolation.

The general logic is this: `_rbfinterp.py` implements the user API and calls
into either `_rbfinterp_np` (the "numpy backend"), or `_rbfinterp_xp` (the
"generic backend".

The numpy backend offloads performance-critical computations to the
pythran-compiled `_rbfinterp_pythran` extension. This way, the call chain is

    _rbfinterp.py <-- _rbfinte
