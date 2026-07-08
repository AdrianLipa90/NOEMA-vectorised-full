# noema_query_cache.py — scripts/noema_query_cache.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_QUERY_CACHE-35D8`
- **ścieżka:** `scripts/noema_query_cache.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.957`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_query_cache.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.957 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
NOEMA Query Cache — SQLite database of search queries, results, and PhaseNav metrics.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_connect`, `log_query`, `log_surface_snapshot`, `recent_queries`, `stats`

## Opis
NOEMA Query Cache — SQLite database of search queries, results, and PhaseNav metrics.

Usage:
    .venv/bin/python3 scripts/noema_query_cache.py --log "quantum gravity" gamma=0.95
    .venv/bin/python3 scripts/noema_query_cache.py --recent 20
    .venv/bin/python3 scripts/noema_query_cache.py --stats
