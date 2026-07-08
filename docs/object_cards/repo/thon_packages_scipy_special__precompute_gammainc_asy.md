# gammainc_asy.py — .python_packages/scipy/special/_precompute/gammainc_asy.py

## Tożsamość
- **id_karty:** `REPO-GAMMAINC_ASY-9DB5`
- **ścieżka:** `.python_packages/scipy/special/_precompute/gammainc_asy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.761`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/_precompute/gammainc_asy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.761 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
Precompute coefficients of Temme's asymptotic expansion for gammainc.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `compute_a`, `compute_g`, `eta`, `compute_alpha`, `compute_d`, `main`

## Opis
Precompute coefficients of Temme's asymptotic expansion for gammainc.

This takes about 8 hours to run on a 2.3 GHz Macbook Pro with 4GB ram.

Sources:
[1] NIST, "Digital Library of Mathematical Functions",
    https://dlmf.nist.gov/
