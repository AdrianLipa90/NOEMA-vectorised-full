# test_stats.py — .python_packages/scipy/stats/tests/test_stats.py

## Tożsamość
- **id_karty:** `REPO-TEST_STATS-87FB`
- **ścieżka:** `.python_packages/scipy/stats/tests/test_stats.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.374`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/stats/tests/test_stats.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.374 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Test functions for stats module

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestTrimmedStats, TestPearsonrWilkinson, TestPearsonr, TestFisherExact, TestCorrSpearmanr, TestCorrSpearmanr2, TestKendallTau, TestKendallTauAlternative, TestWeightedTau, TestRegression, HistFunctionsTest, TestCumfreq, TestRelfreq, TestScoreatpercentile, TestMode, TestSEM, TestZmap, TestZscore, TestGZscore, TestMedianAbsDeviation
- **funkcje:** `ttest_data_axis_strategy`, `test_ttest_ci_iv`, `_desc_stats`, `check_equal_xmean`, `check_equal_gmean`, `check_equal_hmean`, `check_equal_pmean`, `quantile_test_reference`, `test_chk_asarray`, `test_rename_mode_method`, `test_tmean`, `test_tvar`, `test_tstd`, `test_tmin`, `test_tmin_tmax_scalar_input`, `test_tmin_tmax_nanpolicy`, `test_tmax`, `test_tmin_tmax_int_dtype`, `test_gh_22626`, `test_tsem`, `test_pXX`, `test_pXBIG`, `test_pXLITTLE`, `test_pXHUGE`, `test_pXTINY`, `test_pXROUND`, `test_pBIGBIG`, `test_pBIGLITTLE`, `test_pBIGHUGE`, `test_pBIGTINY`

## Opis
Test functions for stats module

WRITTEN BY LOUIS LUANGKESORN <lluang@yahoo.com> FOR THE STATS MODULE
BASED ON WILKINSON'S STATISTICS QUIZ
https://www.stanford.edu/~clint/bench/wilk.txt

Additional tests by a host of SciPy developers.
