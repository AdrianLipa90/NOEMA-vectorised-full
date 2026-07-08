# cli.py — build/lib/ciel_sot_agent/gguf_manager/cli.py

## Tożsamość
- **id_karty:** `REPO-CLI-9F46`
- **ścieżka:** `build/lib/ciel_sot_agent/gguf_manager/cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.354`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/gguf_manager/cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.354 |
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
CLI entry point for GGUF model installation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_progress`, `main`

## Opis
CLI entry point for GGUF model installation.

Usage:
    ciel-sot-install-model                       # download default (TinyLlama)
    ciel-sot-install-model --model qwen2.5-0.5b-q4
    ciel-sot-install-model --model qwen2.5-1.5b-q4
    ciel-sot-install-model --list
