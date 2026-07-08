# crackfortran.py — .python_packages/numpy/f2py/crackfortran.py

## Tożsamość
- **id_karty:** `REPO-CRACKFORTRAN-8997`
- **ścieżka:** `.python_packages/numpy/f2py/crackfortran.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.660`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/f2py/crackfortran.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.660 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
crackfortran --- read fortran (77,90) code and extract declaration information.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `reset_global_f2py_vars`, `outmess`, `rmbadname1`, `rmbadname`, `undo_rmbadname1`, `undo_rmbadname`, `openhook`, `is_free_format`, `readfortrancode`, `split_by_unquoted`, `_simplifyargs`, `crackline`, `markouterparen`, `markoutercomma`, `unmarkouterparen`, `appenddecl`, `_is_intent_callback`, `_resolvetypedefpattern`, `parse_name_for_bind`, `_resolvenameargspattern`, `analyzeline`, `appendmultiline`, `cracktypespec0`, `removespaces`, `markinnerspaces`, `updatevars`, `cracktypespec`, `setattrspec`, `setkindselector`, `setcharselector`

## Opis
crackfortran --- read fortran (77,90) code and extract declaration information.

Copyright 1999 -- 2011 Pearu Peterson all rights reserved.
Copyright 2011 -- present NumPy Developers.
Permission to use, modify, and distribute this software is given under the
terms of the NumPy License.

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.


Usage of crackfortran:
======================
Comm
