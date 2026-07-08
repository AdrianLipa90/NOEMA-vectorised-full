# libelefun.py — .python_packages/mpmath/libmp/libelefun.py

## Tożsamość
- **id_karty:** `REPO-LIBELEFUN-1A82`
- **ścieżka:** `.python_packages/mpmath/libmp/libelefun.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.424`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpmath/libmp/libelefun.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.424 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
This module implements computation of elementary transcendental

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `constant_memo`, `def_mpf_constant`, `bsp_acot`, `acot_fixed`, `machin`, `ln2_fixed`, `ln10_fixed`, `bs_chudnovsky`, `pi_fixed`, `degree_fixed`, `bspe`, `e_fixed`, `phi_fixed`, `ln_sqrt2pi_fixed`, `sqrtpi_fixed`, `mpf_pow`, `int_pow_fixed`, `nthroot_fixed`, `mpf_nthroot`, `mpf_cbrt`, `log_int_fixed`, `agm_fixed`, `log_agm`, `log_taylor`, `log_taylor_cached`, `mpf_log`, `mpf_log_hypot`, `atan_newton`, `atan_taylor_get_cached`, `atan_taylor`

## Opis
This module implements computation of elementary transcendental
functions (powers, logarithms, trigonometric and hyperbolic
functions, inverse trigonometric and hyperbolic) for real
floating-point numbers.

For complex and interval implementations of the same functions,
see libmpc and libmpi.
