# _nanfunctions_impl.py — .python_packages/numpy/lib/_nanfunctions_impl.py

## Tożsamość
- **id_karty:** `REPO-_NANFUNCTIONS_IMPL-D491`
- **ścieżka:** `.python_packages/numpy/lib/_nanfunctions_impl.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.924`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/lib/_nanfunctions_impl.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.924 |
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
Functions that ignore NaN.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_nan_mask`, `_replace_nan`, `_copyto`, `_remove_nan_1d`, `_divide_by_count`, `_nanmin_dispatcher`, `nanmin`, `_nanmax_dispatcher`, `nanmax`, `_nanargmin_dispatcher`, `nanargmin`, `_nanargmax_dispatcher`, `nanargmax`, `_nansum_dispatcher`, `nansum`, `_nanprod_dispatcher`, `nanprod`, `_nancumsum_dispatcher`, `nancumsum`, `_nancumprod_dispatcher`, `nancumprod`, `_nanmean_dispatcher`, `nanmean`, `_nanmedian1d`, `_nanmedian`, `_nanmedian_small`, `_nanmedian_dispatcher`, `nanmedian`, `_nanpercentile_dispatcher`, `nanpercentile`

## Opis
Functions that ignore NaN.

Functions
---------

- `nanmin` -- minimum non-NaN value
- `nanmax` -- maximum non-NaN value
- `nanargmin` -- index of minimum non-NaN value
- `nanargmax` -- index of maximum non-NaN value
- `nansum` -- sum of non-NaN values
- `nanprod` -- product of non-NaN values
- `nancumsum` -- cumulative sum of non-NaN values
- `nancumprod` -- cumulative product of non-NaN values
-
