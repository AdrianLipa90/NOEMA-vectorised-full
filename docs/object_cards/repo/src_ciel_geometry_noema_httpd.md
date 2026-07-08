# noema_httpd.py — src/ciel_geometry/noema_httpd.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_HTTPD-3395`
- **ścieżka:** `src/ciel_geometry/noema_httpd.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `5.249`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/noema_httpd.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 5.249 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
NOEMA HTTP Server — własny, zero-zależnościowy serwer HTTP na raw socket.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** Request, Response, Route, NOEMAServer
- **funkcje:** `example_sse_gen`, `path_clean`, `json`, `html`, `text`, `error`, `sse`, `redirect`, `match`, `route`, `_find_handler`, `_parse_request`, `_send_response`, `_handle_sse`, `stop_sse_clients`, `_serve_static`, `_handle_client`, `start`, `stop`, `hello`, `get_time`, `echo`, `stream`, `decorator`

## Opis
NOEMA HTTP Server — własny, zero-zależnościowy serwer HTTP na raw socket.

Architektura:
- Thread-per-connection (accept → spawn thread)
- SSE przez długie połączenia z okresowym heartbeat
- Routing: dekorator @server.route(method, path) lub dict
- Static file serving z katalogu

Usage:
    from ciel_geometry.noema_httpd import NOEMAServer

    server = NOEMAServer(host="0.0.0.0", port=18888, stat
