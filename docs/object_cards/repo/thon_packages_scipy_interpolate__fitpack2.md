# _fitpack2.py — .python_packages/scipy/interpolate/_fitpack2.py

## Tożsamość
- **id_karty:** `REPO-_FITPACK2-FEAB`
- **ścieżka:** `.python_packages/scipy/interpolate/_fitpack2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.664`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/interpolate/_fitpack2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.664 |
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
fitpack --- curve and surface fitting with splines

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UnivariateSpline, InterpolatedUnivariateSpline, LSQUnivariateSpline, _BivariateSplineBase, BivariateSpline, _DerivedBivariateSpline, SmoothBivariateSpline, LSQBivariateSpline, RectBivariateSpline, SphereBivariateSpline, SmoothSphereBivariateSpline, LSQSphereBivariateSpline, RectSphereBivariateSpline
- **funkcje:** `_calc_b`, `_calc_e`, `_curfit`, `_surfit_smth`, `_surfit_lsq`, `_regrid_smth`, `_spherfit_smth`, `_spherfit_lsq`, `_regrid_smth_spher`, `validate_input`, `_from_tck`, `_reset_class`, `_set_class`, `_reset_nest`, `set_smoothing_factor`, `get_knots`, `get_coeffs`, `get_residual`, `integral`, `derivatives`, `roots`, `derivative`, `antiderivative`, `_from_tck`, `get_residual`, `get_knots`, `get_coeffs`, `partial_derivative`, `ev`, `integral`

## Opis
fitpack --- curve and surface fitting with splines

fitpack is based on a collection of Fortran routines DIERCKX
by P. Dierckx (see http://www.netlib.org/dierckx/) transformed
to double routines by Pearu Peterson.
