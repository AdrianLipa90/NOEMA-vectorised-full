# _matfuncs_inv_ssq.py — .python_packages/scipy/linalg/_matfuncs_inv_ssq.py

## Tożsamość
- **id_karty:** `REPO-_MATFUNCS_INV_SSQ-AF50`
- **ścieżka:** `.python_packages/scipy/linalg/_matfuncs_inv_ssq.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.516`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/linalg/_matfuncs_inv_ssq.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.516 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Matrix functions that use Pade approximation with inverse scaling and squaring.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LogmRankWarning, LogmExactlySingularWarning, LogmNearlySingularWarning, LogmError, FractionalMatrixPowerError, _MatrixM1PowerOperator
- **funkcje:** `_onenormest_m1_power`, `_unwindk`, `_briggs_helper_function`, `_fractional_power_superdiag_entry`, `_logm_superdiag_entry`, `_inverse_squaring_helper`, `_fractional_power_pade_constant`, `_fractional_power_pade`, `_remainder_matrix_power_triu`, `_remainder_matrix_power`, `_fractional_matrix_power`, `_logm_triu`, `_logm_force_nonsingular_triangular_matrix`, `_logm`, `_matvec`, `_rmatvec`, `_matmat`, `_adjoint`

## Opis
Matrix functions that use Pade approximation with inverse scaling and squaring.
