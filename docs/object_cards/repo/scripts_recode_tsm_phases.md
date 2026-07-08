# recode_tsm_phases.py — scripts/recode_tsm_phases.py

## Tożsamość
- **id_karty:** `REPO-RECODE_TSM_PHASES-2265`
- **ścieżka:** `scripts/recode_tsm_phases.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.745`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/recode_tsm_phases.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.745 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Recode TSM phi_berry from SHA-256 hash to semantic encoder phases.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_direct`, `main`

## Opis
Recode TSM phi_berry from SHA-256 hash to semantic encoder phases.

Run after ciel_encoder.py and sentence-transformers are installed.
Updates phi_berry metadata only — D_sense and D_context are never touched.

Usage:
    python3 scripts/recode_tsm_phases.py [--dry-run]
