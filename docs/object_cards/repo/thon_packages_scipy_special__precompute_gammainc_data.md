# gammainc_data.py — .python_packages/scipy/special/_precompute/gammainc_data.py

## Tożsamość
- **id_karty:** `REPO-GAMMAINC_DATA-A038`
- **ścieżka:** `.python_packages/scipy/special/_precompute/gammainc_data.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.106`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/_precompute/gammainc_data.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.106 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Compute gammainc and gammaincc for large arguments and parameters

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `gammainc`, `gammaincc`, `main`, `h`, `h`, `h`

## Opis
Compute gammainc and gammaincc for large arguments and parameters
and save the values to data files for use in tests. We can't just
compare to mpmath's gammainc in test_mpmath.TestSystematic because it
would take too long.

Note that mpmath's gammainc is computed using hypercomb, but since it
doesn't allow the user to increase the maximum number of terms used in
the series it doesn't converge for
