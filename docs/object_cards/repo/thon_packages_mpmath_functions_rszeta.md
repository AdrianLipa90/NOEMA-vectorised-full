# rszeta.py — .python_packages/mpmath/functions/rszeta.py

## Tożsamość
- **id_karty:** `REPO-RSZETA-CE87`
- **ścieżka:** `.python_packages/mpmath/functions/rszeta.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.959`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpmath/functions/rszeta.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.959 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
---------------------------------------------------------------------

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RSCache
- **funkcje:** `_coef`, `coef`, `aux_M_Fp`, `aux_J_needed`, `Rzeta_simul`, `Rzeta_set`, `z_half`, `zeta_half`, `zeta_offline`, `z_offline`, `rs_zeta`, `rs_z`, `trunc_a`, `trunc_a`

## Opis
---------------------------------------------------------------------
.. sectionauthor:: Juan Arias de Reyna <arias@us.es>

This module implements zeta-related functions using the Riemann-Siegel
expansion: zeta_offline(s,k=0)

* coef(J, eps): Need in the computation of Rzeta(s,k)

* Rzeta_simul(s, der=0) computes Rzeta^(k)(s) and Rzeta^(k)(1-s) simultaneously
  for  0 <= k <= der. Used by zeta_off
