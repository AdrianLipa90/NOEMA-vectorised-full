# wpm_cli.py — src/ciel_sot_agent/wpm_cli.py

## Tożsamość
- **id_karty:** `REPO-WPM_CLI-D1F5`
- **ścieżka:** `src/ciel_sot_agent/wpm_cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.114`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/wpm_cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.114 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


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
