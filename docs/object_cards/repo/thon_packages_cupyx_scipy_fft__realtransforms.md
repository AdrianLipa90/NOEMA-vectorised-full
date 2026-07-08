# _realtransforms.py — .python_packages/cupyx/scipy/fft/_realtransforms.py

## Tożsamość
- **id_karty:** `REPO-_REALTRANSFORMS-B2F2`
- **ścieżka:** `.python_packages/cupyx/scipy/fft/_realtransforms.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.171`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cupyx/scipy/fft/_realtransforms.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.171 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
Real-to-real transforms

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_promote_dtype`, `_get_dct_norm_factor`, `_reshuffle_dct2`, `_exp_factor_dct2`, `_dct_or_dst_type2`, `_reshuffle_dct3`, `_exp_factor_dct3`, `_dct_or_dst_type3`, `dct`, `dst`, `idct`, `idst`, `_iterable_of_int`, `_init_nd_shape_and_axes`, `dctn`, `idctn`, `dstn`, `idstn`

## Opis
Real-to-real transforms

cuFFT does not implement real-to-real FFTs. This module implements forward
and inverse DCT-II and DCT-III transforms using FFTs.

A length N DCT can be computed using a length N FFT and some additional
multiplications and reordering of entries.

The approach taken here is based on the work in [1]_, [2]_ and is discussed in
the freely-available online resources [3]_, [4]_.
