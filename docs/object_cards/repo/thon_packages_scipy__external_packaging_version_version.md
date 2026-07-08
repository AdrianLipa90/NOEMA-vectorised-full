# version.py — .python_packages/scipy/_external/packaging_version/version.py

## Tożsamość
- **id_karty:** `REPO-VERSION-29E7`
- **ścieżka:** `.python_packages/scipy/_external/packaging_version/version.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.378`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/_external/packaging_version/version.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.378 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
.. testsetup::

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _Version, InvalidVersion, _BaseVersion, Version, _TrimmedRelease
- **funkcje:** `parse`, `_parse_letter_version`, `_parse_local_version`, `_cmpkey`, `epoch`, `release`, `pre`, `post`, `dev`, `local`, `public`, `base_version`, `is_prerelease`, `is_postrelease`, `is_devrelease`, `major`, `minor`, `micro`, `release`

## Opis
.. testsetup::

    from packaging.version import parse, Version
