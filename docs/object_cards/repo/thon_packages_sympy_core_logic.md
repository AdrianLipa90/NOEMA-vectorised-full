# logic.py — .python_packages/sympy/core/logic.py

## Tożsamość
- **id_karty:** `REPO-LOGIC-1F2C`
- **ścieżka:** `.python_packages/sympy/core/logic.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.951`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/core/logic.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.951 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Logic expressions handling

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Logic, AndOr_Base, And, Or, Not
- **funkcje:** `_torf`, `_fuzzy_group`, `fuzzy_bool`, `fuzzy_and`, `fuzzy_not`, `fuzzy_or`, `fuzzy_xor`, `fuzzy_nand`, `fromstring`, `flatten`, `_eval_propagate_not`, `expand`, `_eval_propagate_not`, `arg`

## Opis
Logic expressions handling

NOTE
----

at present this is mainly needed for facts.py, feel free however to improve
this stuff for general purpose.
