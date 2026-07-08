# visitors.py — .python_packages/mypy/test/visitors.py

## Tożsamość
- **id_karty:** `REPO-VISITORS-3E17`
- **ścieżka:** `.python_packages/mypy/test/visitors.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.047`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/visitors.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.047 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
Visitor classes pulled out from different tests

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SkippedNodeSearcher, TypeAssertTransformVisitor
- **funkcje:** `ignore_node`, `visit_assignment_stmt`, `visit_name_expr`, `visit_int_expr`, `type`

## Opis
Visitor classes pulled out from different tests

These are here because we don't currently support having interpreted
classes subtype compiled ones but pytest grabs the python file
even if the test was compiled.
