# ast.py — .python_packages/sympy/codegen/ast.py

## Tożsamość
- **id_karty:** `REPO-AST-D5D0`
- **ścieżka:** `.python_packages/sympy/codegen/ast.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.669`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/codegen/ast.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.669 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Types used to represent a full function/module as an Abstract Syntax Tree.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CodegenAST, Token, BreakToken, ContinueToken, NoneToken, AssignmentBase, Assignment, AugmentedAssignment, AddAugmentedAssignment, SubAugmentedAssignment, MulAugmentedAssignment, DivAugmentedAssignment, ModAugmentedAssignment, CodeBlock, For, String, QuotedString, Comment, Node, Type
- **funkcje:** `_mk_Tuple`, `aug_assign`, `is_Atom`, `_get_constructor`, `_construct`, `_hashable_content`, `_joiner`, `_indented`, `_sympyrepr`, `kwargs`, `_hashable_content`, `lhs`, `rhs`, `_check_args`, `op`, `_sympyrepr`, `free_symbols`, `topological_sort`, `cse`, `_construct_body`, `_construct_iterable`, `_construct_text`, `_sympystr`, `kwargs`, `func`, `_latex`, `attr_params`, `_sympystr`, `from_expr`, `_check`

## Opis
Types used to represent a full function/module as an Abstract Syntax Tree.

Most types are small, and are merely used as tokens in the AST. A tree diagram
has been included below to illustrate the relationships between the AST types.


AST Type Tree
-------------
::

  *Basic*
       |
       |
   CodegenAST
       |
       |--->AssignmentBase
       |             |--->Assignment
       |
