# manualintegrate.py — .python_packages/sympy/integrals/manualintegrate.py

## Tożsamość
- **id_karty:** `REPO-MANUALINTEGRATE-E98C`
- **ścieżka:** `.python_packages/sympy/integrals/manualintegrate.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.606`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/integrals/manualintegrate.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.606 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Integration method that emulates by-hand techniques.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Rule, AtomicRule, ConstantRule, ConstantTimesRule, PowerRule, NestedPowRule, AddRule, URule, PartsRule, CyclicPartsRule, TrigRule, SinRule, CosRule, SecTanRule, CscCotRule, Sec2Rule, Csc2Rule, HyperbolicRule, SinhRule, CoshRule
- **funkcje:** `manual_diff`, `manual_subs`, `find_substitutions`, `rewriter`, `proxy_rewriter`, `multiplexer`, `alternatives`, `constant_rule`, `power_rule`, `exp_rule`, `orthogonal_poly_rule`, `special_function_rule`, `_add_degenerate_step`, `nested_pow_rule`, `inverse_trig_rule`, `add_rule`, `mul_rule`, `_parts_rule`, `parts_rule`, `trig_rule`, `trig_product_rule`, `quadratic_denom_rule`, `sqrt_linear_rule`, `sqrt_quadratic_rule`, `hyperbolic_rule`, `make_wilds`, `sincos_pattern`, `tansec_pattern`, `cotcsc_pattern`, `heaviside_pattern`

## Opis
Integration method that emulates by-hand techniques.

This module also provides functionality to get the steps used to evaluate a
particular integral, in the ``integral_steps`` function. This will return
nested ``Rule`` s representing the integration rules used.

Each ``Rule`` class represents a (maybe parametrized) integration rule, e.g.
``SinRule`` for integrating ``sin(x)`` and ``ReciprocalSqrt
