# ciel_browser_surface.py — scripts/ciel_browser_surface.py

## Tożsamość
- **id_karty:** `REPO-CIEL_BROWSER_SURFACE-EE3D`
- **ścieżka:** `scripts/ciel_browser_surface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.155`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_browser_surface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.155 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
ciel_browser_surface.py — CIEL Browser Surface Daemon.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_ensure_surface`, `_atomic_write`, `_write_state`, `_write_page`, `_registry_write`, `_registry_unlink`, `_find_browser_window`, `_ensure_browser`, `_key_press`, `_type_text`, `_get_window_title`, `_wait_for_load`, `_capture_screenshot`, `_ocr_image`, `cmd_navigate`, `cmd_read`, `cmd_search`, `cmd_click`, `_get_window_offset`, `cmd_scroll`, `cmd_status`, `cmd_close`, `_process_cmd`, `_quit`, `_stop`, `main`, `search_and_click`

## Opis
ciel_browser_surface.py — CIEL Browser Surface Daemon.

Daje mi (CIEL/NOEMA) możliwość "widzenia" i interakcji z przeglądarką
jak człowiek: otwieram strony, czytam treść, klikam linki, szukam.

Pipeline:
  command.fifo ←── CIEL wysyła komendę
       │
       ▼
  Browser action (xdotool: navigate, click, scroll)
       │
       ▼
  Screenshot (mss) → Tesseract OCR → at-spi2 tree
       │
       ▼
