# _root_scalar.py — .python_packages/scipy/optimize/_root_scalar.py

## Tożsamość
- **id_karty:** `REPO-_ROOT_SCALAR-9A2E`
- **ścieżka:** `.python_packages/scipy/optimize/_root_scalar.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.305`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_root_scalar.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.305 |
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
Unified interfaces to root finding algorithms for real or complex

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MemoizeDer
- **funkcje:** `root_scalar`, `_root_scalar_brentq_doc`, `_root_scalar_brenth_doc`, `_root_scalar_toms748_doc`, `_root_scalar_secant_doc`, `_root_scalar_newton_doc`, `_root_scalar_halley_doc`, `_root_scalar_ridder_doc`, `_root_scalar_bisect_doc`, `fprime`, `fprime2`, `ncalls`, `fprime`, `f_wrapped`

## Opis
Unified interfaces to root finding algorithms for real or complex
scalar functions.

Functions
---------
- root : find a root of a scalar function.
