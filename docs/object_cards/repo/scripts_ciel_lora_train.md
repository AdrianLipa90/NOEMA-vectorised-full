# ciel_lora_train.py — scripts/ciel_lora_train.py

## Tożsamość
- **id_karty:** `REPO-CIEL_LORA_TRAIN-DD01`
- **ścieżka:** `scripts/ciel_lora_train.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.903`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_lora_train.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.903 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
CIEL LoRA Training Script

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** OrbitalTrainer
- **funkcje:** `holonomy_loss_torch`, `inject_orbital_weights`, `load_dataset`, `format_for_training`, `train`, `compute_loss`

## Opis
CIEL LoRA Training Script

Fine-tuning qwen2.5-0.5B z orbitalną inicjalizacją LoRA.

Wymaga:
  pip install torch==2.0.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
  pip install transformers peft trl accelerate bitsandbytes

Użycie:
  python3 ciel_lora_train.py
  python3 ciel_lora_train.py --epochs 3 --rank 8 --output ./ciel_lora_out
  python3 ciel_lora_train.py --dry-run   # sp
