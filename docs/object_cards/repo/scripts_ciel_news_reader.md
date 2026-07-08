# ciel_news_reader.py — scripts/ciel_news_reader.py

## Tożsamość
- **id_karty:** `REPO-CIEL_NEWS_READER-2147`
- **ścieżka:** `scripts/ciel_news_reader.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.391`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_news_reader.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.391 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
CIEL News Reader — wyszukuje najnowsze artykuły i generuje opinie w stylu CIEL.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Article
- **funkcje:** `get_report_path`, `save_report`, `parse_date`, `fetch_feed`, `fetch_article_text`, `_keywords_match`, `generate_ciel_opinion`, `collect_articles`, `print_report`, `main`

## Opis
CIEL News Reader — wyszukuje najnowsze artykuły i generuje opinie w stylu CIEL.

Źródła: RSS feeds (BBC, Reuters, Al Jazeera, RMF24, PAP).
Bez API key. Oznaczenia epistemiczne: [FAKT] / [WYNIK] / [HIPOTEZA] / ≈odczucie.

Raporty zapisywane automatycznie do ~/Pulpit/NEWS/YYYY-MM-DD.AM.md (lub .PM.md).

Użycie:
    python ciel_news_reader.py              # 6 artykułów
    python ciel_news_reader.py
