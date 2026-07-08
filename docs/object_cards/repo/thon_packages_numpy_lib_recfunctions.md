# recfunctions.py — .python_packages/numpy/lib/recfunctions.py

## Tożsamość
- **id_karty:** `REPO-RECFUNCTIONS-FA48`
- **ścieżka:** `.python_packages/numpy/lib/recfunctions.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.983`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/lib/recfunctions.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.983 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
Collection of utilities to manipulate structured arrays.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_recursive_fill_fields_dispatcher`, `recursive_fill_fields`, `_get_fieldspec`, `get_names`, `get_names_flat`, `flatten_descr`, `_zip_dtype`, `_zip_descr`, `get_fieldstructure`, `_izip_fields_flat`, `_izip_fields`, `_izip_records`, `_fix_output`, `_fix_defaults`, `_merge_arrays_dispatcher`, `merge_arrays`, `_drop_fields_dispatcher`, `drop_fields`, `_keep_fields`, `_rec_drop_fields_dispatcher`, `rec_drop_fields`, `_rename_fields_dispatcher`, `rename_fields`, `_append_fields_dispatcher`, `append_fields`, `_rec_append_fields_dispatcher`, `rec_append_fields`, `_repack_fields_dispatcher`, `repack_fields`, `_get_fields_and_offsets`

## Opis
Collection of utilities to manipulate structured arrays.

Most of these functions were initially implemented by John Hunter for
matplotlib.  They have been rewritten and extended for convenience.
