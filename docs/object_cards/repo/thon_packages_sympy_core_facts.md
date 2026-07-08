# facts.py — .python_packages/sympy/core/facts.py

## Tożsamość
- **id_karty:** `REPO-FACTS-8F0E`
- **ścieżka:** `.python_packages/sympy/core/facts.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.281`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/core/facts.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.281 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
This is rule-based deduction system for SymPy

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TautologyDetected, Prover, FactRules, InconsistentAssumptions, FactKB
- **funkcje:** `_base_fact`, `_as_pair`, `transitive_closure`, `deduce_alpha_implications`, `apply_beta_to_alpha_route`, `rules_2prereq`, `split_alpha_beta`, `rules_alpha`, `rules_beta`, `process_rule`, `_process_rule`, `_to_python`, `_from_python`, `_defined_facts_lines`, `_full_implications_lines`, `_prereq_lines`, `_beta_rules_lines`, `print_rules`, `_tell`, `deduce_all_facts`

## Opis
This is rule-based deduction system for SymPy

The whole thing is split into two parts

 - rules compilation and preparation of tables
 - runtime inference

For rule-based inference engines, the classical work is RETE algorithm [1],
[2] Although we are not implementing it in full (or even significantly)
it's still worth a read to understand the underlying ideas.

In short, every rule in a system o
