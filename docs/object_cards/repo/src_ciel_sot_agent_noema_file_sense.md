# noema_file_sense.py — src/ciel_sot_agent/noema_file_sense.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_FILE_SENSE-BC55`
- **ścieżka:** `src/ciel_sot_agent/noema_file_sense.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.313`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/noema_file_sense.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.313 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


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
