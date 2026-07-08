# runtime_evidence_ingest.py — src/ciel_sot_agent/runtime_evidence_ingest.py

## Tożsamość
- **id_karty:** `REPO-RUNTIME_EVIDENCE_ING-C4EE`
- **ścieżka:** `src/ciel_sot_agent/runtime_evidence_ingest.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.084`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/runtime_evidence_ingest.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.084 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


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
