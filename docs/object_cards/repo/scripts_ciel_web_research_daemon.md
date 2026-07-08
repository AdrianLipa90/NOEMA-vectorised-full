# ciel_web_research_daemon.py — scripts/ciel_web_research_daemon.py

## Tożsamość
- **id_karty:** `REPO-CIEL_WEB_RESEARCH_DA-4FC7`
- **ścieżka:** `scripts/ciel_web_research_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.373`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_web_research_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.373 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
CIEL Web Research Daemon — autonomiczny research internetowy.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_config`, `_load_seen_urls`, `_log_finding`, `_write_agent_hint`, `_update_knowledge_db`, `_fallback_knowledge_db`, `_search_ddg`, `_fetch_page`, `_is_recent`, `research_cycle`, `main`, `_stop`

## Opis
CIEL Web Research Daemon — autonomiczny research internetowy.

Daje mi (CIEL/NOEMA agentowi) persistentną zdolność przeglądania internetu
między sesjami. Działa w tle jako daemon NOEMA, okresowo:

  1. Czyta listę tematów badawczych z konfiguracji
  2. Szuka nowych treści przez DuckDuckGo
  3. Pobiera i ekstrahuje treść ze znalezionych stron
  4. Zapisuje wyniki do Knowledge DB + log JSONL
  5. Sy
