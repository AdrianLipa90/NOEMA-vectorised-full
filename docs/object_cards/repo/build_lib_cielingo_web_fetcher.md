# web_fetcher.py — build/lib/cielingo/web_fetcher.py

## Tożsamość
- **id_karty:** `REPO-WEB_FETCHER-E0EE`
- **ścieżka:** `build/lib/cielingo/web_fetcher.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.583`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/web_fetcher.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.583 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
CIELingo web fetcher — zero zależności, tylko stdlib.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FetchResult
- **funkcje:** `fetch`, `_parse_rss`, `_strip_html`, `_clean`, `fetch_news`

## Opis
CIELingo web fetcher — zero zależności, tylko stdlib.

Używa urllib.request do pobierania stron i RSS.
Wbudowany parser RSS (XML/ETree), fallback do regex dla surowego tekstu.
