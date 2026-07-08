# risch.py — .python_packages/sympy/integrals/risch.py

## Tożsamość
- **id_karty:** `REPO-RISCH-B7BA`
- **ścieżka:** `.python_packages/sympy/integrals/risch.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.695`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/integrals/risch.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.695 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
The Risch Algorithm for transcendental function integration.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DifferentialExtension, DecrementLevel, NonElementaryIntegralException, NonElementaryIntegral
- **funkcje:** `integer_powers`, `update_sets`, `gcdex_diophantine`, `frac_in`, `as_poly_1t`, `derivation`, `get_case`, `splitfactor`, `splitfactor_sqf`, `canonical_representation`, `hermite_reduce`, `polynomial_reduce`, `laurent_series`, `recognize_derivative`, `recognize_log_derivative`, `residue_reduce`, `residue_reduce_to_basic`, `residue_reduce_derivation`, `integrate_primitive_polynomial`, `integrate_primitive`, `integrate_hyperexponential_polynomial`, `integrate_hyperexponential`, `integrate_hypertangent_polynomial`, `integrate_nonlinear_no_specials`, `risch_integrate`, `_rewrite_exps_pows`, `_rewrite_logs`, `_auto_attrs`, `_exp_part`, `_log_part`

## Opis
The Risch Algorithm for transcendental function integration.

The core algorithms for the Risch algorithm are here.  The subproblem
algorithms are in the rde.py and prde.py files for the Risch
Differential Equation solver and the parametric problems solvers,
respectively.  All important information concerning the differential extension
for an integrand is stored in a DifferentialExtension object,
