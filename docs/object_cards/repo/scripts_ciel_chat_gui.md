# ciel_chat_gui.py — scripts/ciel_chat_gui.py

## Tożsamość
- **id_karty:** `REPO-CIEL_CHAT_GUI-458A`
- **ścieżka:** `scripts/ciel_chat_gui.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.777`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_chat_gui.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.777 |
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
CIEL Chat GUI — prosty działający interfejs

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_model`, `get_ciel_metrics`, `get_system_resources`, `load_memory_context`, `index`, `add_message`, `update_metrics`, `_infer`

## Opis
CIEL Chat GUI — prosty działający interfejs
NiceGUI + TinyLlama + metryki CIEL orbital

Uruchom: python scripts/ciel_chat_gui.py
Otwórz:  http://127.0.0.1:8080
