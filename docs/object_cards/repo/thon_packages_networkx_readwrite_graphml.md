# graphml.py — .python_packages/networkx/readwrite/graphml.py

## Tożsamość
- **id_karty:** `REPO-GRAPHML-D896`
- **ścieżka:** `.python_packages/networkx/readwrite/graphml.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.614`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/readwrite/graphml.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.614 |
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
*******

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GraphML, GraphMLWriter, IncrementalElement, GraphMLWriterLxml, GraphMLReader
- **funkcje:** `write_graphml_xml`, `write_graphml_lxml`, `generate_graphml`, `read_graphml`, `parse_graphml`, `construct_types`, `get_xml_type`, `attr_type`, `get_key`, `add_data`, `add_attributes`, `add_nodes`, `add_edges`, `add_graph_element`, `add_graphs`, `dump`, `indent`, `append`, `add_graph_element`, `add_attributes`, `dump`, `make_graph`, `add_node`, `add_edge`, `decode_data_elements`, `find_graphml_keys`

## Opis
*******
GraphML
*******
Read and write graphs in GraphML format.

.. warning::

    This parser uses the standard xml library present in Python, which is
    insecure - see :external+python:mod:`xml` for additional information.
    Only parse GraphML files you trust.

This implementation does not support mixed graphs (directed and unidirected
edges together), hyperedges, nested graphs, or ports.
