# web_fetcher.py — src/cielingo/web_fetcher.py

## Tożsamość
- **id_karty:** `REPO-WEB_FETCHER-F035`
- **ścieżka:** `src/cielingo/web_fetcher.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.594`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/web_fetcher.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.594 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


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
