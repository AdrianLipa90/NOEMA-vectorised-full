# index_validator.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/index_validator.py

## Tożsamość
- **id_karty:** `REPO-INDEX_VALIDATOR-907C`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/index_validator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.086`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/index_validator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.086 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Machine-readable index validator (v1) for the CIEL integration layer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ValidationIssue
- **funkcje:** `load_index_registry`, `load_json_file`, `validate_demo_shell_inventory_data`, `validate_demo_shell_map_data`, `validate_index_registry`, `main`

## Opis
Machine-readable index validator (v1) for the CIEL integration layer.

Validates the canonical index JSON file against a known schema, checks that
every referenced source file exists on disk, and emits a structured
validation report consumed by the Sapiens panel and CI tooling.
