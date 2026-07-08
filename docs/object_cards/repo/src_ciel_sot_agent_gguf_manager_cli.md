# cli.py — src/ciel_sot_agent/gguf_manager/cli.py

## Tożsamość
- **id_karty:** `REPO-CLI-CA87`
- **ścieżka:** `src/ciel_sot_agent/gguf_manager/cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.330`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/gguf_manager/cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.330 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


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
