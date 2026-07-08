# filters.py — .python_packages/h5py/_hl/filters.py

## Tożsamość
- **id_karty:** `REPO-FILTERS-FA2A`
- **ścieżka:** `.python_packages/h5py/_hl/filters.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.351`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/h5py/_hl/filters.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.351 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Implements support for HDF5 compression filters via the high-level

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FilterRefBase, Gzip
- **funkcje:** `_gen_filter_tuples`, `_external_entry`, `_normalize_external`, `fill_dcpl`, `get_filter_name`, `get_filters`, `guess_chunk`, `_kwargs`, `rq_tuple`

## Opis
Implements support for HDF5 compression filters via the high-level
interface.  The following types of filter are available:

"gzip"
    Standard DEFLATE-based compression, at integer levels from 0 to 9.
    Built-in to all public versions of HDF5.  Use this if you want a
    decent-to-good ratio, good portability, and don't mind waiting.

"lzf"
    Custom compression filter for h5py.  This filter
