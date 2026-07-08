# noema_httpd.py — build/lib/ciel_geometry/noema_httpd.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_HTTPD-4B67`
- **ścieżka:** `build/lib/ciel_geometry/noema_httpd.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.349`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/noema_httpd.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.349 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
NOEMA HTTP Server — własny, zero-zależnościowy serwer HTTP na raw socket.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
