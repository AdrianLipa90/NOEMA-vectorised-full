# index_validator_v2.py — src/ciel_sot_agent/index_validator_v2.py

## Tożsamość
- **id_karty:** `REPO-INDEX_VALIDATOR_V2-6350`
- **ścieżka:** `src/ciel_sot_agent/index_validator_v2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.187`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/index_validator_v2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.187 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
Machine-readable index validator v2 for the CIEL integration layer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ValidationIssue
- **funkcje:** `load_index_registry`, `load_json_file`, `resolve_existing_path`, `resolve_index_registry_path`, `find_demo_shell_map_object`, `validate_demo_shell_inventory_data`, `validate_demo_shell_map_data`, `validate_index_registry`, `main`

## Opis
Machine-readable index validator v2 for the CIEL integration layer.

Extends the v1 validator with v2 schema support, coupling-aware validation,
and enriched diagnostic output.  Produces a versioned report written to
``integration/reports/index_validation_v2/``.
