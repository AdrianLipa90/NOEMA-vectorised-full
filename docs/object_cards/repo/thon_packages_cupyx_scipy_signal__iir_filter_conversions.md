# _iir_filter_conversions.py — .python_packages/cupyx/scipy/signal/_iir_filter_conversions.py

## Tożsamość
- **id_karty:** `REPO-_IIR_FILTER_CONVERSI-9519`
- **ścieżka:** `.python_packages/cupyx/scipy/signal/_iir_filter_conversions.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.805`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cupyx/scipy/signal/_iir_filter_conversions.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.805 |
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
IIR filter conversion utilities.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** BadCoefficients
- **funkcje:** `_trim_zeros`, `_align_nums`, `_polycoeffs_from_zeros`, `_nearest_real_complex_idx`, `_single_zpksos`, `zpk2sos`, `_cplxreal`, `normalize`, `_relative_degree`, `bilinear_zpk`, `lp2lp_zpk`, `lp2hp_zpk`, `lp2bp_zpk`, `lp2bs_zpk`, `bilinear`, `lp2lp`, `lp2hp`, `lp2bp`, `lp2bs`, `zpk2tf`, `tf2zpk`, `tf2sos`, `sos2tf`, `sos2zpk`, `tf2ss`, `ss2tf`, `zpk2ss`, `ss2zpk`, `buttap`, `cheb1ap`

## Opis
IIR filter conversion utilities.

Split off _filter_design.py
