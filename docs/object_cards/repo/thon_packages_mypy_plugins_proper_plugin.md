# proper_plugin.py — .python_packages/mypy/plugins/proper_plugin.py

## Tożsamość
- **id_karty:** `REPO-PROPER_PLUGIN-7D0D`
- **ścieżka:** `.python_packages/mypy/plugins/proper_plugin.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.823`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/plugins/proper_plugin.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.823 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
This plugin is helpful for mypy development itself.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ProperTypePlugin
- **funkcje:** `isinstance_proper_hook`, `is_special_target`, `is_improper_type`, `is_dangerous_target`, `proper_type_hook`, `proper_types_hook`, `get_proper_type_instance`, `plugin`, `get_function_hook`

## Opis
This plugin is helpful for mypy development itself.
By default, it is not enabled for mypy users.

It also can be used by plugin developers as a part of their CI checks.

It finds missing ``get_proper_type()`` call, which can lead to multiple errors.
