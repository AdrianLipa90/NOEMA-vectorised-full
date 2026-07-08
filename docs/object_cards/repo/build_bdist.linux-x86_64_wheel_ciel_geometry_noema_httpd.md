# noema_httpd.py — build/bdist.linux-x86_64/wheel/ciel_geometry/noema_httpd.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_HTTPD-16B7`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_httpd.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.229`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_httpd.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.229 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
