# rt_subtype.py — .python_packages/mypyc/rt_subtype.py

## Tożsamość
- **id_karty:** `REPO-RT_SUBTYPE-1CF9`
- **ścieżka:** `.python_packages/mypyc/rt_subtype.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.663`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/rt_subtype.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.663 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
'Runtime subtype' check for RTypes.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RTSubtypeVisitor
- **funkcje:** `is_runtime_subtype`, `visit_rinstance`, `visit_rvec`, `visit_runion`, `visit_rprimitive`, `visit_rtuple`, `visit_rstruct`, `visit_rarray`, `visit_rvoid`

## Opis
'Runtime subtype' check for RTypes.

A type S is a runtime subtype of T if a value of type S can be used at runtime
when a value of type T is expected without requiring any runtime conversions.

For boxed types, runtime subtyping is the same as regular subtyping.
Unboxed subtypes, on the other hand, are not runtime subtypes of object
(since they require boxing to be used as an object), but short i
