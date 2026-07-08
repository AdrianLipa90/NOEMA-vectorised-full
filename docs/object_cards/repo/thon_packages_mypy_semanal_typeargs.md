# semanal_typeargs.py — .python_packages/mypy/semanal_typeargs.py

## Tożsamość
- **id_karty:** `REPO-SEMANAL_TYPEARGS-06C7`
- **ścieżka:** `.python_packages/mypy/semanal_typeargs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.025`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/semanal_typeargs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.025 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Verify properties of type arguments, like 'int' in C[int] being valid.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypeArgumentAnalyzer
- **funkcje:** `visit_mypy_file`, `visit_func`, `visit_class_def`, `visit_block`, `visit_type_alias_type`, `visit_tuple_type`, `visit_callable_type`, `visit_instance`, `check_non_paramspec`, `validate_args`, `visit_unpack_type`, `check_type_var_values`, `fail`, `note`

## Opis
Verify properties of type arguments, like 'int' in C[int] being valid.

This must happen after semantic analysis since there can be placeholder
types until the end of semantic analysis, and these break various type
operations, including subtype checks.
