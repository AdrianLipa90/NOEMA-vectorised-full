# index_validator.py — src/ciel_sot_agent/index_validator.py

## Tożsamość
- **id_karty:** `REPO-INDEX_VALIDATOR-E24E`
- **ścieżka:** `src/ciel_sot_agent/index_validator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.909`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/index_validator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.909 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
