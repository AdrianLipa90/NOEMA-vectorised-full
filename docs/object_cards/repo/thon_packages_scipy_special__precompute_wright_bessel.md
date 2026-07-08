# wright_bessel.py — .python_packages/scipy/special/_precompute/wright_bessel.py

## Tożsamość
- **id_karty:** `REPO-WRIGHT_BESSEL-2694`
- **ścieżka:** `.python_packages/scipy/special/_precompute/wright_bessel.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.570`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/_precompute/wright_bessel.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.570 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Precompute coefficients of several series expansions

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** g, coef_C
- **funkcje:** `series_small_a`, `dg_series`, `pg_series`, `series_small_a_small_b`, `asymptotic_series`, `optimal_epsilon_integral`, `main`, `fp`, `arclength`, `func`, `eval`, `eval`

## Opis
Precompute coefficients of several series expansions
of Wright's generalized Bessel function Phi(a, b, x).

See https://dlmf.nist.gov/10.46.E1 with rho=a, beta=b, z=x.
