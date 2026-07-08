# dataflow.py — .python_packages/mypyc/analysis/dataflow.py

## Tożsamość
- **id_karty:** `REPO-DATAFLOW-4B7C`
- **ścieżka:** `.python_packages/mypyc/analysis/dataflow.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.416`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/analysis/dataflow.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.416 |
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
Data-flow analyses.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CFG, AnalysisResult, BaseAnalysisVisitor, DefinedVisitor, BorrowedArgumentsVisitor, UndefinedVisitor, LivenessVisitor
- **funkcje:** `get_cfg`, `get_real_target`, `cleanup_cfg`, `analyze_maybe_defined_regs`, `analyze_must_defined_regs`, `analyze_borrowed_arguments`, `non_trivial_sources`, `analyze_live_regs`, `run_analysis`, `visit_goto`, `visit_register_op`, `visit_assign`, `visit_assign_multi`, `visit_set_mem`, `visit_inc_ref`, `visit_dec_ref`, `visit_call`, `visit_method_call`, `visit_load_error_value`, `visit_load_literal`, `visit_get_attr`, `visit_set_attr`, `visit_load_static`, `visit_init_static`, `visit_tuple_get`, `visit_tuple_set`, `visit_box`, `visit_unbox`, `visit_cast`, `visit_raise_standard_error`

## Opis
Data-flow analyses.
