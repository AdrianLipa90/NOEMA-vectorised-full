# web_fetcher.py — build/bdist.linux-x86_64/wheel/cielingo/web_fetcher.py

## Tożsamość
- **id_karty:** `REPO-WEB_FETCHER-6069`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/web_fetcher.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.337`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/web_fetcher.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.337 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


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
