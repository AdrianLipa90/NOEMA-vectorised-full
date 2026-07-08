# secondquant.py — .python_packages/sympy/physics/secondquant.py

## Tożsamość
- **id_karty:** `REPO-SECONDQUANT-18D3`
- **ścieżka:** `.python_packages/sympy/physics/secondquant.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.496`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/secondquant.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.496 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Second quantization operators and states for bosons.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SecondQuantizationError, AppliesOnlyToSymbolicIndex, ContractionAppliesOnlyToFermions, ViolationOfPauliPrinciple, SubstitutionOfAmbigousOperatorFailed, WicksTheoremDoesNotApply, Dagger, TensorSymbol, AntiSymmetricTensor, SqOperator, BosonicOperator, Annihilator, Creator, AnnihilateBoson, CreateBoson, FermionicOperator, AnnihilateFermion, CreateFermion, FockState, BosonState
- **funkcje:** `_apply_Mul`, `apply_operators`, `matrix_rep`, `contraction`, `_sqkey_operator`, `_sqkey_index`, `_sort_anticommuting_fermions`, `evaluate_deltas`, `substitute_dummies`, `_get_ordered_dummies`, `_determine_ambiguous`, `_get_contractions`, `wicks`, `simplify_index_permutations`, `eval`, `_dagger_`, `_latex`, `symbol`, `upper`, `lower`, `state`, `is_symbolic`, `apply_operator`, `_dagger_`, `apply_operator`, `_latex`, `_dagger_`, `apply_operator`, `_latex`, `is_restricted`

## Opis
Second quantization operators and states for bosons.

This follow the formulation of Fetter and Welecka, "Quantum Theory
of Many-Particle Systems."
