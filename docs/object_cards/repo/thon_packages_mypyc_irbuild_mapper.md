# mapper.py — .python_packages/mypyc/irbuild/mapper.py

## Tożsamość
- **id_karty:** `REPO-MAPPER-7743`
- **ścieżka:** `.python_packages/mypyc/irbuild/mapper.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.693`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/mapper.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.693 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Maintain a mapping from mypy concepts to IR/compiled concepts.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Mapper
- **funkcje:** `type_to_rtype`, `get_arg_rtype`, `fdef_to_sig`, `is_native_module`, `is_native_ref_expr`, `is_native_module_ref_expr`

## Opis
Maintain a mapping from mypy concepts to IR/compiled concepts.
