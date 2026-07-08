# version.py — .python_packages/packaging/version.py

## Tożsamość
- **id_karty:** `REPO-VERSION-626A`
- **ścieżka:** `.python_packages/packaging/version.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.400`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/packaging/version.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.400 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
.. testsetup::

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _VersionReplace, InvalidVersion, _BaseVersion, _Version, Version, _TrimmedRelease
- **funkcje:** `normalize_pre`, `parse`, `_validate_epoch`, `_validate_release`, `_validate_pre`, `_validate_post`, `_validate_dev`, `_validate_local`, `_parse_letter_version`, `_parse_local_version`, `_cmpkey`, `from_parts`, `_key`, `_version`, `_version`, `_str`, `epoch`, `release`, `pre`, `post`, `dev`, `local`, `public`, `base_version`, `is_prerelease`, `is_postrelease`, `is_devrelease`, `major`, `minor`, `micro`

## Opis
.. testsetup::

    from packaging.version import parse, normalize_pre, Version, _cmpkey
