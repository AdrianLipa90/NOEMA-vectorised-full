# wright_bessel_data.py — .python_packages/scipy/special/_precompute/wright_bessel_data.py

## Tożsamość
- **id_karty:** `REPO-WRIGHT_BESSEL_DATA-3F98`
- **ścieżka:** `.python_packages/scipy/special/_precompute/wright_bessel_data.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.112`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/_precompute/wright_bessel_data.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.112 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Compute a grid of values for Wright's generalized Bessel function

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `rgamma_cached`, `mp_wright_bessel`, `main`

## Opis
Compute a grid of values for Wright's generalized Bessel function
and save the values to data files for use in tests. Using mpmath directly in
tests would take too long.

This takes about 10 minutes to run on a 2.7 GHz i7 Macbook Pro.
