# gml.py — .python_packages/networkx/readwrite/gml.py

## Tożsamość
- **id_karty:** `REPO-GML-CEBE`
- **ścieżka:** `.python_packages/networkx/readwrite/gml.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.101`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/readwrite/gml.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.101 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Read graphs in GML format.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Pattern, Token
- **funkcje:** `escape`, `unescape`, `literal_destringizer`, `read_gml`, `parse_gml`, `parse_gml_lines`, `literal_stringizer`, `generate_gml`, `write_gml`, `fixup`, `fixup`, `filter_lines`, `decode_line`, `filter_lines`, `tokenize`, `unexpected`, `consume`, `parse_kv`, `parse_dict`, `parse_graph`, `pop_attr`, `stringize`, `stringize`, `clean_dict_value`

## Opis
Read graphs in GML format.

"GML, the Graph Modelling Language, is our proposal for a portable
file format for graphs. GML's key features are portability, simple
syntax, extensibility and flexibility. A GML file consists of a
hierarchical key-value lists. Graphs can be annotated with arbitrary
data structures. The idea for a common file format was born at the
GD'95; this proposal is the outcome of
