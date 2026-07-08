# sleep_consolidation.py — runtime/ciel_omega/memory/sleep_consolidation.py

## Tożsamość
- **id_karty:** `REPO-SLEEP_CONSOLIDATION-A0BB`
- **ścieżka:** `runtime/ciel_omega/memory/sleep_consolidation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.359`
- **masa_semantyczna:** `0.40`

## Kotwice
- `runtime/ciel_omega/memory/sleep_consolidation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.359 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Idle-time book consolidation for the sleep mode braid.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SleepConsolidationReport
- **funkcje:** `_utc_now_iso`, `_utc_now_epoch`, `_bounded`, `_sha256_text`, `_norm_load`, `default_sleep_corpus_paths`, `_existing_paths`, `_pairwise_holonomy_score`, `_promotion_score`, `_idle_gate`, `analyze_sleep_mode_corpus`, `analyze_sleep_mode_default_corpus`, `as_dict`

## Opis
Idle-time book consolidation for the sleep mode braid.

The intent here is explicit:
- analyse book-like sources when the system is quiet,
- digest them through the existing cognitive book analysis pipeline,
- evaluate pairwise holonomy / coherence,
- promote the stabilized corpus into a higher memory layer only when the gate is open.
