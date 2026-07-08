# cli.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/monolith/cli.py

## Tożsamość
- **id_karty:** `REPO-CLI-20C7`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/monolith/cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.053`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/monolith/cli.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.053 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
CIEL/Ω Memory — CLI and kernel adapter.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_cli_status`, `_cli_run`, `_cli_verify`, `_cli_backup`, `_cli_export`, `main`

## Opis
CIEL/Ω Memory — CLI and kernel adapter.

Split from: unified_memory.py (lines 607–731)

Usage:
    python -m memory.monolith.cli status
    python -m memory.monolith.cli run --context test --sense "hello world" --promote
