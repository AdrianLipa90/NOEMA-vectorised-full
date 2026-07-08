# manager.py — src/ciel_sot_agent/gguf_manager/manager.py

## Tożsamość
- **id_karty:** `REPO-MANAGER-EB70`
- **ścieżka:** `src/ciel_sot_agent/gguf_manager/manager.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.379`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/gguf_manager/manager.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.379 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
GGUF model manager — download and locate small quantised models on first startup.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ModelSpec, GGUFManager
- **funkcje:** `_default_models_dir`, `_sha256_file`, `get_model_path`, `download_default_model`, `list_models`, `is_installed`, `model_path`, `ensure_model`, `save_manifest`, `load_manifest`, `_download`

## Opis
GGUF model manager — download and locate small quantised models on first startup.

The manager is intentionally lightweight: it uses only Python stdlib so that the
core package does not require heavy ML dependencies at install time.  The actual
model runner (llama.cpp, ctransformers, etc.) is left to the calling layer.

Usage:
    from ciel_sot_agent.gguf_manager import GGUFManager, download_defau
