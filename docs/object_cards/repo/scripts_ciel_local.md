# ciel_local.py — scripts/ciel_local.py

## Tożsamość
- **id_karty:** `REPO-CIEL_LOCAL-4C98`
- **ścieżka:** `scripts/ciel_local.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.065`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_local.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.065 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
CIEL Local — lokalny model GGUF z CUDA jako offline fallback lub autonomiczny agent.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_orchestrator`, `build_ciel_system_prompt`, `run`, `main`

## Opis
CIEL Local — lokalny model GGUF z CUDA jako offline fallback lub autonomiczny agent.

Użycie:
    python3 ciel_local.py "twoja wiadomość"
    echo "wiadomość" | python3 ciel_local.py
    python3 ciel_local.py --model tinyllama  # (domyślny)
    python3 ciel_local.py --model qwen05     # Qwen2.5-0.5B Q2_K (szybszy)
    python3 ciel_local.py --model qwen4      # Qwen3.5-4B Q8 (lepszy)

Stan orkiestr
