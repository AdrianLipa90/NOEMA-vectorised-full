# synchronize_v2.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/synchronize_v2.py

## Tożsamość
- **id_karty:** `REPO-SYNCHRONIZE_V2-26A0`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/synchronize_v2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.675`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/synchronize_v2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.675 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


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
