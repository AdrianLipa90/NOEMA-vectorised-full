# test_mstats_basic.py — .python_packages/scipy/stats/tests/test_mstats_basic.py

## Tożsamość
- **id_karty:** `REPO-TEST_MSTATS_BASIC-401D`
- **ścieżka:** `.python_packages/scipy/stats/tests/test_mstats_basic.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.593`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/stats/tests/test_mstats_basic.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.593 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Tests for the stats.mstats module (support for masked arrays)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestMquantiles, TestGeoMean, TestHarMean, TestRanking, TestCorr, TestTrimming, TestMoments, TestMode, TestPercentile, TestVariability, TestMisc, TestTheilslopes, TestNormalitytests, TestFOneway, TestMannwhitneyu, TestKruskal, TestTtest_rel, TestTtest_ind, TestTtest_1samp, TestDescribe
- **funkcje:** `check_equal_gmean`, `check_equal_hmean`, `test_regress_simple`, `test_linregress_identical_x`, `test_siegelslopes`, `test_siegelslopes_namedtuple_consistency`, `test_sen_seasonal_slopes`, `test_plotting_positions`, `test_mquantiles_limit_keyword`, `test_1d`, `test_1d_ma`, `test_1d_ma_value`, `test_1d_ma0`, `test_1d_ma_inf`, `test_1d_float96`, `test_2d_ma`, `test_1d`, `test_1d_float96`, `test_2d`, `test_ranking`, `test_pearsonr`, `test_pearsonr_misaligned_mask`, `test_spearmanr`, `test_spearmanr_alternative`, `test_kendalltau`, `test_overflow_gh6061`, `test_kendalltau_vs_mstats_basic`, `test_kendalltau_large`, `test_kendalltau_seasonal`, `test_kendalltau_mstats_vs_stats`

## Opis
Tests for the stats.mstats module (support for masked arrays)
