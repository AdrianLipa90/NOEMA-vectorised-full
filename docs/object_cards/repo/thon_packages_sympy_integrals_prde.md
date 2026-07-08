# prde.py — .python_packages/sympy/integrals/prde.py

## Tożsamość
- **id_karty:** `REPO-PRDE-A580`
- **ścieżka:** `.python_packages/sympy/integrals/prde.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.577`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/integrals/prde.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.577 |
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
Algorithms for solving Parametric Risch Differential Equations.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `prde_normal_denom`, `real_imag`, `prde_special_denom`, `prde_linear_constraints`, `poly_linear_constraints`, `constant_system`, `prde_spde`, `prde_no_cancel_b_large`, `prde_no_cancel_b_small`, `prde_cancel_liouvillian`, `param_poly_rischDE`, `param_rischDE`, `limited_integrate_reduce`, `limited_integrate`, `parametric_log_deriv_heu`, `parametric_log_deriv`, `is_deriv_k`, `is_log_deriv_k_t_radical`, `is_log_deriv_k_t_radical_in_field`

## Opis
Algorithms for solving Parametric Risch Differential Equations.

The methods used for solving Parametric Risch Differential Equations parallel
those for solving Risch Differential Equations.  See the outline in the
docstring of rde.py for more information.

The Parametric Risch Differential Equation problem is, given f, g1, ..., gm in
K(t), to determine if there exist y in K(t) and c1, ..., cm in
