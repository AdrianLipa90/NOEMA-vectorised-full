# index_validator_v2.py — build/lib/ciel_sot_agent/index_validator_v2.py

## Tożsamość
- **id_karty:** `REPO-INDEX_VALIDATOR_V2-21DF`
- **ścieżka:** `build/lib/ciel_sot_agent/index_validator_v2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.441`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/index_validator_v2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.441 |
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
