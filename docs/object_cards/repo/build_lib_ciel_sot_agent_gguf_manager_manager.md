# manager.py — build/lib/ciel_sot_agent/gguf_manager/manager.py

## Tożsamość
- **id_karty:** `REPO-MANAGER-D6FB`
- **ścieżka:** `build/lib/ciel_sot_agent/gguf_manager/manager.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.081`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/gguf_manager/manager.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.081 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


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
