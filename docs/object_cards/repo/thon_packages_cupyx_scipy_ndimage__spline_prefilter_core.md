# _spline_prefilter_core.py — .python_packages/cupyx/scipy/ndimage/_spline_prefilter_core.py

## Tożsamość
- **id_karty:** `REPO-_SPLINE_PREFILTER_CO-0261`
- **ścieżka:** `.python_packages/cupyx/scipy/ndimage/_spline_prefilter_core.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.254`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cupyx/scipy/ndimage/_spline_prefilter_core.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.254 |
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
Spline poles and boundary handling implemented as in SciPy

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `get_poles`, `get_gain`, `_causal_init_code`, `_anticausal_init_code`, `_get_spline_mode`, `_get_spline1d_code`, `get_raw_spline1d_kernel`

## Opis
Spline poles and boundary handling implemented as in SciPy

https://github.com/scipy/scipy/blob/master/scipy/ndimage/src/ni_splines.c
