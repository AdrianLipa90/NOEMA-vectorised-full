# runtime_evidence_ingest.py — build/lib/ciel_sot_agent/runtime_evidence_ingest.py

## Tożsamość
- **id_karty:** `REPO-RUNTIME_EVIDENCE_ING-4837`
- **ścieżka:** `build/lib/ciel_sot_agent/runtime_evidence_ingest.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.858`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/runtime_evidence_ingest.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.858 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


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
