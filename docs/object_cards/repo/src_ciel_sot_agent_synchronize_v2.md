# synchronize_v2.py — src/ciel_sot_agent/synchronize_v2.py

## Tożsamość
- **id_karty:** `REPO-SYNCHRONIZE_V2-1A57`
- **ścieżka:** `src/ciel_sot_agent/synchronize_v2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.276`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/synchronize_v2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.276 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


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
