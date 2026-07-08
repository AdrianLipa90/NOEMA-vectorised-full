# runtime_evidence_ingest.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/runtime_evidence_ingest.py

## Tożsamość
- **id_karty:** `REPO-RUNTIME_EVIDENCE_ING-9FAE`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/runtime_evidence_ingest.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.964`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/runtime_evidence_ingest.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.964 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
Runtime evidence ingest pipeline for CIEL-SOT-Agent.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ValidationIssue
- **funkcje:** `load_json_file`, `validate_runtime_evidence_data`, `classify_evidence`, `ingest_runtime_evidence`, `main`

## Opis
Runtime evidence ingest pipeline for CIEL-SOT-Agent.

Reads structured evidence artefacts (schemas, reports, registry files) from
the ``integration/`` directory, validates them against known schemas, and
writes a consolidated ``runtime_evidence_ingest.json`` report consumed by
the Sapiens interaction layer and CI tooling.
