# catalog_zips_noema.py — scripts/catalog_zips_noema.py

## Tożsamość
- **id_karty:** `REPO-CATALOG_ZIPS_NOEMA-0925`
- **ścieżka:** `scripts/catalog_zips_noema.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.059`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/catalog_zips_noema.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.059 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
NOEMA ZIP Catalog — indeksuje zawartość archiwów CIEL bez wypakowywania.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_walk_zips`, `find_zips`, `catalog_zip`, `_lang_from_ext`, `write_catalog`, `_merge_counts`, `main`

## Opis
NOEMA ZIP Catalog — indeksuje zawartość archiwów CIEL bez wypakowywania.

Kataloguje strukturę wszystkich ZIPów w REPO/*.zip, zapisuje indeks do
/dev/shm/ciel_noema/zip_catalog/ jako JSONL + PhaseNav enrichment per plik.

Usage (dry-run):
    python scripts/catalog_zips_noema.py --dry-run

Usage (real):
    python scripts/catalog_zips_noema.py

Wymagane: python3 -c "import zipfile"  (stdlib)
