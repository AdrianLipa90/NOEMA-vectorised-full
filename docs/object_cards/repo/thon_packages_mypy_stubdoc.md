# stubdoc.py — .python_packages/mypy/stubdoc.py

## Tożsamość
- **id_karty:** `REPO-STUBDOC-CE25`
- **ścieżka:** `.python_packages/mypy/stubdoc.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.444`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/stubdoc.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.444 |
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
Parsing/inferring signatures from documentation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ArgSig, FunctionSig, DocStringParser
- **funkcje:** `is_valid_type`, `infer_sig_from_docstring`, `infer_arg_sig_from_anon_docstring`, `infer_ret_type_sig_from_docstring`, `infer_ret_type_sig_from_anon_docstring`, `parse_signature`, `build_signature`, `parse_all_signatures`, `find_unique_signatures`, `infer_prop_type_from_docstring`, `is_star_arg`, `is_star_kwarg`, `is_special_method`, `has_catchall_args`, `is_catchall_signature`, `format_sig`, `add_token`, `reset`, `get_signatures`, `is_unique_args`, `has_arg`, `args_kwargs`

## Opis
Parsing/inferring signatures from documentation.

This module provides several functions to generate better stubs using
docstrings and Sphinx docs (.rst files).
