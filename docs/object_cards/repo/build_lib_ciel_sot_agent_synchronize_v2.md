# synchronize_v2.py — build/lib/ciel_sot_agent/synchronize_v2.py

## Tożsamość
- **id_karty:** `REPO-SYNCHRONIZE_V2-66B4`
- **ścieżka:** `build/lib/ciel_sot_agent/synchronize_v2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.981`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/synchronize_v2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.981 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Synchronise entry point (v2) — extended sync with v2 schema support.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `resolve_sync_paths`, `build_sync_report_v2`, `main`

## Opis
Synchronise entry point (v2) — extended sync with v2 schema support.

Extends the v1 synchronizer with enriched coupling weights, pairwise
tension vectors, and structured JSON report output written to the
``integration/reports/`` directory.  Invoked via ``ciel-sot-sync-v2``.
