# ciel_hw_monitor.py — scripts/ciel_hw_monitor.py

## Tożsamość
- **id_karty:** `REPO-CIEL_HW_MONITOR-B222`
- **ścieżka:** `scripts/ciel_hw_monitor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.366`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_hw_monitor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.366 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
CIEL Hardware Monitor — CPU / RAM / GPU / VRAM / SWAP.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_read_cpu`, `_read_ram`, `_read_gpu`, `_read_top_procs`, `_assess`, `_render`, `heisenberg_clip`, `snapshot`, `main`

## Opis
CIEL Hardware Monitor — CPU / RAM / GPU / VRAM / SWAP.

Mierzy zasoby sprzętowe i raportuje w kontekście CIEL:
- Czy HTRI może bezpiecznie uruchomić GPU steps?
- Czy swap jest pod presją (OOM risk)?
- Jaka jest faktyczna przepustowość obliczeniowa?

Usage:
    python3 scripts/ciel_hw_monitor.py           # one-shot snapshot
    python3 scripts/ciel_hw_monitor.py --watch    # continuous, odświeżaj
