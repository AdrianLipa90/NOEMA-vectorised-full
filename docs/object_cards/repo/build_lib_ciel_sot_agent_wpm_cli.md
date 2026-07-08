# wpm_cli.py — build/lib/ciel_sot_agent/wpm_cli.py

## Tożsamość
- **id_karty:** `REPO-WPM_CLI-66E8`
- **ścieżka:** `build/lib/ciel_sot_agent/wpm_cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.838`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/wpm_cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.838 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
ciel-sot-wpm — CLI do Wave Phase Memory (WPM).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_wpm_path`, `_load_all`, `_cmd_list`, `_cmd_show`, `_cmd_search`, `_cmd_network`, `_cmd_export`, `main`, `_s`

## Opis
ciel-sot-wpm — CLI do Wave Phase Memory (WPM).

Komendy:
  list              tabela wszystkich wspomnień
  show <id>         pełna treść wpisu (UUID lub prefix 8 znaków)
  search <query>    szukaj po treści D_sense
  network           graf skojarzeń między wspomnieniami
  export            JSON dump wszystkich wpisów
