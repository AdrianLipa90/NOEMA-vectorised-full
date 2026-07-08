# interpolative.py — .python_packages/scipy/linalg/interpolative.py

## Tożsamość
- **id_karty:** `REPO-INTERPOLATIVE-E25F`
- **ścieżka:** `.python_packages/scipy/linalg/interpolative.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.883`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/linalg/interpolative.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.883 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
======================================================================

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_C_contiguous_copy`, `_is_real`, `interp_decomp`, `reconstruct_matrix_from_id`, `reconstruct_interp_matrix`, `reconstruct_skel_matrix`, `id_to_svd`, `estimate_spectral_norm`, `estimate_spectral_norm_diff`, `svd`, `estimate_rank`

## Opis
======================================================================
Interpolative matrix decomposition (:mod:`scipy.linalg.interpolative`)
======================================================================

.. versionadded:: 0.13

.. versionchanged:: 1.15.0
    The underlying algorithms have been ported to Python from the original Fortran77
    code. See references below for more details.
