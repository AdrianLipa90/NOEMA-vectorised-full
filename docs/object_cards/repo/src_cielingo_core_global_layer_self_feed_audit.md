# self_feed_audit.py — src/cielingo_core/global_layer/self_feed_audit.py

## Tożsamość
- **id_karty:** `REPO-SELF_FEED_AUDIT-E80D`
- **ścieżka:** `src/cielingo_core/global_layer/self_feed_audit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.999`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/self_feed_audit.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.999 |
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
Self-feed audit log and dry-run export bundle v0.8C.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SelfFeedAuditEventKind, SelfFeedAuditEvent, SelfFeedAuditLog, RuntimeDryRunExportBundle
- **funkcje:** `_hash_obj`, `_event`, `build_self_feed_audit_log`, `build_runtime_dry_run_export_bundle`, `validate`, `to_dict`, `validate`, `to_dict`, `stable_hash`, `write_jsonl`, `validate`, `to_dict`, `stable_hash`, `write_json`

## Opis
Self-feed audit log and dry-run export bundle v0.8C.

Captures the advisory self-feed chain:
    MeaningLoop -> RepairRouting -> GlobalMeaningSignal -> RuntimeBridgeDryRun

Boundary:
- audit log is appendable local artifact, not NOEMA writeback;
- dry-run export is portable artifact, not CURRENT update;
- no runtime execution, no SOURCE/canon promotion.
