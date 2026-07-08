# semanal_newtype.py — .python_packages/mypy/semanal_newtype.py

## Tożsamość
- **id_karty:** `REPO-SEMANAL_NEWTYPE-F05B`
- **ścieżka:** `.python_packages/mypy/semanal_newtype.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.630`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/semanal_newtype.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.630 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Semantic analysis of NewType definitions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NewTypeAnalyzer
- **funkcje:** `process_newtype_declaration`, `analyze_newtype_declaration`, `check_newtype_args`, `build_newtype_typeinfo`, `make_argument`, `fail`

## Opis
Semantic analysis of NewType definitions.

This is conceptually part of mypy.semanal (semantic analyzer pass 2).
