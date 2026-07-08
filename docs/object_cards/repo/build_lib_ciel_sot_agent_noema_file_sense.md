# noema_file_sense.py — build/lib/ciel_sot_agent/noema_file_sense.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_FILE_SENSE-0D52`
- **ścieżka:** `build/lib/ciel_sot_agent/noema_file_sense.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.847`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/noema_file_sense.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.847 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
NOEMA file-sense layer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_json`, `_normalize_annotation`, `_path_location`, `_infer_file_type`, `_infer_subsystem`, `_infer_purpose`, `_infer_status`, `_infer_authority`, `_safe_flags`, `_build_sync_lookup`, `_build_internal_lookup`, `_build_annotation_lookup`, `build_registry`, `filter_entries`, `inspect_registry`, `write_registry`, `main`, `_match`

## Opis
NOEMA file-sense layer.

Builds a semantic registry over repository files so cleanup and inspection can
reason about function, ownership, hierarchy, and lifecycle rather than raw
paths alone.
