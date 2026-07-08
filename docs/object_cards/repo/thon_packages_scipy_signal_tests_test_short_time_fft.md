# test_short_time_fft.py — .python_packages/scipy/signal/tests/test_short_time_fft.py

## Tożsamość
- **id_karty:** `REPO-TEST_SHORT_TIME_FFT-8B7C`
- **ścieżka:** `.python_packages/scipy/signal/tests/test_short_time_fft.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.839`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/signal/tests/test_short_time_fft.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.839 |
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
Unit tests for module `_short_time_fft`.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `test__calc_dual_canonical_window_roundtrip`, `test__calc_dual_canonical_window_exceptions`, `test_closest_STFT_dual_window_exceptions`, `test_closest_STFT_dual_window_roundtrip`, `test_closest_STFT_dual_window_STFT_roundtrip`, `test_closest_STFT_dual_window_STFT_roundtrip_complex`, `test_closest_STFT_dual_window_cola`, `test_invalid_initializer_parameters`, `test_exceptions_properties_methods`, `test_exceptions_fft_mode_complex_win`, `test_invalid_fft_mode_RuntimeError`, `test_from_window`, `test_from_win_equals_dual_exceptions`, `test_from_win_equals_dual_params`, `test_from_win_equals_dual_roundtrip`, `test_from_win_equals_dual_unitary`, `test_dual_win_roundtrip`, `test_scaling`, `test_scale_to`, `test_x_slices_padding`, `test_invertible`, `test_border_values`, `test_border_values_exotic`, `test_t`, `test_f`, `test_extent`, `test_spectrogram`, `test_fft_func_roundtrip`, `test_impulse_roundtrip`, `test_asymmetric_window_roundtrip`

## Opis
Unit tests for module `_short_time_fft`.

This file's structure loosely groups the tests into the following sequential
categories:

1. Test function `_calc_dual_canonical_window`.
2. Test for invalid parameters and exceptions in `ShortTimeFFT` (until the
    `test_from_window` function).
3. Test algorithmic properties of STFT/ISTFT. Some tests were ported from
   ``test_spectral.py``.

Notes
-----
