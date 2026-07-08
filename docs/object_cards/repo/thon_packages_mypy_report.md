# report.py — .python_packages/mypy/report.py

## Tożsamość
- **id_karty:** `REPO-REPORT-C86D`
- **ścieżka:** `.python_packages/mypy/report.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.263`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/report.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.263 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
Classes for producing HTML reports about imprecision.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Reports, AbstractReporter, FuncCounterVisitor, LineCountReporter, AnyExpressionsReporter, LineCoverageVisitor, LineCoverageReporter, FileInfo, MemoryXmlReporter, CoberturaPackage, CoberturaXmlReporter, AbstractXmlReporter, XmlReporter, XsltHtmlReporter, XsltTxtReporter, LinePrecisionReporter
- **funkcje:** `register_reporter`, `alias_reporter`, `should_skip_path`, `iterate_python_lines`, `get_line_rate`, `add_report`, `file`, `finish`, `on_file`, `on_finish`, `visit_func_def`, `on_file`, `on_finish`, `on_file`, `on_finish`, `_write_out_report`, `_report_any_exprs`, `_report_types_of_anys`, `indentation_level`, `visit_func_def`, `on_file`, `on_finish`, `total`, `attrib`, `on_file`, `_get_any_info_for_line`, `on_finish`, `as_xml`, `add_packages`, `on_file`

## Opis
Classes for producing HTML reports about imprecision.
