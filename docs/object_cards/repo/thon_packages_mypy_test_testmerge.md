# testmerge.py — .python_packages/mypy/test/testmerge.py

## Tożsamość
- **id_karty:** `REPO-TESTMERGE-327F`
- **ścieżka:** `.python_packages/mypy/test/testmerge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.143`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/testmerge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.143 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
Test cases for AST merge (used for fine-grained incremental checking)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ASTMergeSuite
- **funkcje:** `setup`, `run_case`, `build`, `build_increment`, `dump`, `dump_asts`, `dump_symbol_tables`, `dump_symbol_table`, `format_symbol_table_node`, `dump_typeinfos`, `dump_typeinfos_recursive`, `dump_typeinfo`, `dump_types`, `format_type`

## Opis
Test cases for AST merge (used for fine-grained incremental checking)
