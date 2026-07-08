# noema_file_sense.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/noema_file_sense.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_FILE_SENSE-CDE8`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/noema_file_sense.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.538`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/noema_file_sense.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.538 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


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
