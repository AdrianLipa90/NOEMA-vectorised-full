# experimental_lambdify.py — .python_packages/sympy/plotting/experimental_lambdify.py

## Tożsamość
- **id_karty:** `REPO-EXPERIMENTAL_LAMBDIF-A886`
- **ścieżka:** `.python_packages/sympy/plotting/experimental_lambdify.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.560`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/plotting/experimental_lambdify.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.560 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
rewrite of lambdify - This stuff is not stable at all.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** vectorized_lambdify, lambdify, Lambdifier
- **funkcje:** `experimental_lambdify`, `get_dict_str`, `get_dict_fun`, `str2tree`, `tree2str`, `tree2str_translate`, `translate_str`, `translate_func`, `sympy_expression_namespace`, `sympy_atoms_namespace`

## Opis
rewrite of lambdify - This stuff is not stable at all.

It is for internal use in the new plotting module.
It may (will! see the Q'n'A in the source) be rewritten.

It's completely self contained. Especially it does not use lambdarepr.

It does not aim to replace the current lambdify. Most importantly it will never
ever support anything else than SymPy expressions (no Matrices, dictionaries
and so
