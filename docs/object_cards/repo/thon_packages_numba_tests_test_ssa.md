# test_ssa.py — .python_packages/numba/tests/test_ssa.py

## Tożsamość
- **id_karty:** `REPO-TEST_SSA-477C`
- **ścieżka:** `.python_packages/numba/tests/test_ssa.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.138`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_ssa.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.138 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Tests for SSA reconstruction

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SSABaseTest, TestSSA, TestReportedSSAIssues, TestSROAIssues, CustomPipeline, CheckSSAMinimal, CustomPipeline, SSACheck, SSACheckPipeline, CloneFoobarAssignments, CustomCompiler
- **funkcje:** `check_func`, `test_argument_name_reused`, `test_if_else_redefine`, `test_sum_loop`, `test_sum_loop_2vars`, `test_sum_2d_loop`, `check_undefined_var`, `test_undefined_var`, `test_phi_propagation`, `test_unhandled_undefined`, `test_issue2194`, `test_issue3094`, `test_issue3931`, `test_issue3976`, `test_issue3979`, `test_issue5219`, `test_issue5223`, `test_issue5243`, `test_issue5482_missing_variable_init`, `test_issue5482_objmode_expr_null_lowering`, `test_issue5493_unneeded_phi`, `test_issue5623_equal_statements_in_same_bb`, `test_issue5678_non_minimal_phi`, `test_issue9242_use_not_dom_def`, `test_issue7258_multiple_assignment_post_SSA`, `foo`, `foo`, `foo`, `foo`, `foo`

## Opis
Tests for SSA reconstruction
