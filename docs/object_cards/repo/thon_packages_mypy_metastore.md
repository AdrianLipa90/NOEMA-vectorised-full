# metastore.py — .python_packages/mypy/metastore.py

## Tożsamość
- **id_karty:** `REPO-METASTORE-DA98`
- **ścieżka:** `.python_packages/mypy/metastore.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.319`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/metastore.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.319 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Interfaces for accessing metadata.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MetadataStore, FilesystemMetadataStore, SqliteMetadataStore
- **funkcje:** `random_string`, `connect_db`, `getmtime`, `read`, `write`, `remove`, `commit`, `commit_path`, `list_all`, `close`, `getmtime`, `read`, `write`, `remove`, `commit`, `list_all`, `close`, `_shard_index`, `_db_for`, `_query`, `getmtime`, `read`, `write`, `remove`, `commit`, `commit_path`, `list_all`, `close`

## Opis
Interfaces for accessing metadata.

We provide two implementations.
 * The "classic" file system implementation, which uses a directory
   structure of files.
 * A hokey sqlite backed implementation, which basically simulates
   the file system in an effort to work around poor file system performance
   on OS X.
