# puiseux.py — .python_packages/sympy/polys/puiseux.py

## Tożsamość
- **id_karty:** `REPO-PUISEUX-03A7`
- **ścieżka:** `.python_packages/sympy/polys/puiseux.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.737`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/puiseux.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.737 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Puiseux rings. These are used by the ring_series module to represented

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PuiseuxRing, PuiseuxPoly
- **funkcje:** `puiseux_ring`, `_div_poly_monom`, `_mul_poly_monom`, `_div_monom`, `from_poly`, `from_dict`, `from_int`, `domain_new`, `ground_new`, `index`, `_new`, `_new_raw`, `_normalize`, `_monom_fromint`, `_monom_toint`, `itermonoms`, `monoms`, `iterterms`, `terms`, `is_term`, `to_dict`, `from_dict`, `as_expr`, `_unify`, `_add`, `_add_ground`, `_sub`, `_sub_ground`, `_rsub_ground`, `_mul`

## Opis
Puiseux rings. These are used by the ring_series module to represented
truncated Puiseux series. Elements of a Puiseux ring are like polynomials
except that the exponents can be negative or rational rather than just
non-negative integers.
