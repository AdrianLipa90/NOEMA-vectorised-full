# test_cdflib.py — .python_packages/scipy/special/tests/test_cdflib.py

## Tożsamość
- **id_karty:** `REPO-TEST_CDFLIB-A6A7`
- **ścieżka:** `.python_packages/scipy/special/tests/test_cdflib.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.777`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/tests/test_cdflib.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.777 |
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
Test cdflib functions versus mpmath, if available.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ProbArg, EndpointFilter, _CDFData, TestCDFlib, TestNoncentralTFunctions, TestNegativeBinomialFunctions, TestNoncentralChiSquaredFunctions, TestPdtrik
- **funkcje:** `_assert_inverts`, `_binomial_cdf`, `_f_cdf`, `_student_t_cdf`, `_noncentral_chi_pdf`, `_noncentral_chi_cdf`, `_tukey_lmbda_quantile`, `test_nonfinite`, `test_chndtrix_gh2158`, `test_nctdtrinc_gh19896`, `test_stdtr_stdtrit_neg_inf`, `test_bdtrik_nbdtrik_inf`, `test_ncfdtr_ncfdtri`, `test_ncfdtri_domain_error`, `test_chdtriv_p_equals_1_returns_0`, `test_gdtrix_edge_cases`, `test_gdtria_edge_cases`, `test_bdtrik`, `test_nrdtrimn_edge_cases`, `test_nrdtrisd_edge_cases`, `values`, `idmap`, `get_param_filter`, `check`, `test_bdtrin`, `test_btdtria`, `test_btdtrib`, `test_fdtridfd`, `test_gdtria`, `test_gdtrib`

## Opis
Test cdflib functions versus mpmath, if available.

The following functions still need tests:

- ncfdtridfn
- ncfdtridfd
- ncfdtrinc
- nctdtridf
- nctdtrinc
