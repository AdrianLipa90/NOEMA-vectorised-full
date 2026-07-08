# stubgenc.py — .python_packages/mypy/stubgenc.py

## Tożsamość
- **id_karty:** `REPO-STUBGENC-D6F8`
- **ścieżka:** `.python_packages/mypy/stubgenc.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.750`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/stubgenc.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.750 |
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
Stub generator for C modules.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ExternalSignatureGenerator, DocstringSignatureGenerator, CFunctionStub, InspectionStubGenerator
- **funkcje:** `is_pybind11_overloaded_function_docstring`, `generate_stub_for_c_module`, `method_name_sort_key`, `is_pybind_skipped_attribute`, `infer_c_method_args`, `from_doc_dir`, `get_function_sig`, `get_property_type`, `get_function_sig`, `get_property_type`, `_from_sig`, `_from_sigs`, `get_default_function_sig`, `get_sig_generators`, `strip_or_import`, `get_obj_module`, `is_defined_in_module`, `generate_module`, `is_skipped_attribute`, `get_members`, `get_type_annotation`, `is_function`, `is_method`, `is_classmethod`, `is_staticmethod`, `is_abstract_method`, `is_property`, `is_property_readonly`, `is_static_property`, `process_inferred_sigs`

## Opis
Stub generator for C modules.

The public interface is via the mypy.stubgen module.
