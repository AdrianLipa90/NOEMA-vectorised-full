# ciel_lora_init.py — scripts/ciel_lora_init.py

## Tożsamość
- **id_karty:** `REPO-CIEL_LORA_INIT-974A`
- **ścieżka:** `scripts/ciel_lora_init.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.090`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_lora_init.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.090 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
CIEL Orbital LoRA Initialization

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `get_berry_phases`, `compute_orbital_lora_seed`, `holonomy_loss`, `euler_constraint_check`, `save_lora_seed`, `analyze_coupling_geometry`

## Opis
CIEL Orbital LoRA Initialization

Inicjalizacja macierzy LoRA przez geometrię orbitalną CIEL:
  - LoRA A: eigenvektory J_kj (macierz sprzężeń Kuramoto) → struktua orbital
  - LoRA B: rotacja przez fazę Berry'ego → holonomiczny twist
  - Regularyzator: holonomy constraint w funkcji straty

Matematyka:
  J = COUPLING_MATRIX (8×8 Kuramoto)
  SVD: J = U·S·V^T
  A_seed = U[:r, :]  (top-r wiersze lewych
