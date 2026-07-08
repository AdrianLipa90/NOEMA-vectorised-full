# wpm_cli.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/wpm_cli.py

## Tożsamość
- **id_karty:** `REPO-WPM_CLI-9503`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/wpm_cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.007`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/wpm_cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.007 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


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
