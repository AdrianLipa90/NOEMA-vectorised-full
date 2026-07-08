# _scipy_spectral_test_shim.py — .python_packages/scipy/signal/tests/_scipy_spectral_test_shim.py

## Tożsamość
- **id_karty:** `REPO-_SCIPY_SPECTRAL_TEST-6C4C`
- **ścieżka:** `.python_packages/scipy/signal/tests/_scipy_spectral_test_shim.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.073`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/signal/tests/_scipy_spectral_test_shim.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.073 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Helpers to utilize existing stft / istft tests for testing `ShortTimeFFT`.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_stft_wrapper`, `_istft_wrapper`, `stft_compare`, `istft_compare`

## Opis
Helpers to utilize existing stft / istft tests for testing `ShortTimeFFT`.

This module provides the functions stft_compare() and istft_compare(), which,
compares the output between the existing (i)stft() and the shortTimeFFT based
_(i)stft_wrapper() implementations in this module.

For testing add the following imports to the file ``tests/test_spectral.py``::

    from ._scipy_spectral_test_shim
