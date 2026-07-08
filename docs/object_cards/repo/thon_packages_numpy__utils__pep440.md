# _pep440.py — .python_packages/numpy/_utils/_pep440.py

## Tożsamość
- **id_karty:** `REPO-_PEP440-8C1B`
- **ścieżka:** `.python_packages/numpy/_utils/_pep440.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.033`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/_utils/_pep440.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.033 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Utility to compare pep440 compatible version strings.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Infinity, NegativeInfinity, InvalidVersion, _BaseVersion, LegacyVersion, Version
- **funkcje:** `parse`, `_parse_version_parts`, `_legacy_cmpkey`, `_parse_letter_version`, `_parse_local_version`, `_cmpkey`, `_compare`, `public`, `base_version`, `local`, `is_prerelease`, `is_postrelease`, `public`, `base_version`, `local`, `is_prerelease`, `is_postrelease`

## Opis
Utility to compare pep440 compatible version strings.

The LooseVersion and StrictVersion classes that distutils provides don't
work; they don't recognize anything like alpha/beta/rc/dev versions.
