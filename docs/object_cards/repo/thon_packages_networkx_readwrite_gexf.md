# gexf.py — .python_packages/networkx/readwrite/gexf.py

## Tożsamość
- **id_karty:** `REPO-GEXF-13A6`
- **ścieżka:** `.python_packages/networkx/readwrite/gexf.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.378`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/readwrite/gexf.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.378 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Read and write graphs in GEXF format.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GEXF, GEXFWriter, GEXFReader
- **funkcje:** `write_gexf`, `generate_gexf`, `read_gexf`, `relabel_gexf_graph`, `construct_types`, `set_version`, `add_graph`, `add_nodes`, `add_edges`, `add_attributes`, `get_attr_id`, `add_viz`, `add_parents`, `add_slices`, `add_spells`, `alter_graph_mode_timeformat`, `write`, `indent`, `make_graph`, `add_node`, `add_start_end`, `add_viz`, `add_parents`, `add_slices`, `add_spells`, `add_edge`, `decode_attr_elements`, `find_gexf_attributes`, `edge_key_data`

## Opis
Read and write graphs in GEXF format.

.. warning::
    This parser uses the standard xml library present in Python, which is
    insecure - see :external+python:mod:`xml` for additional information.
    Only parse GEFX files you trust.

GEXF (Graph Exchange XML Format) is a language for describing complex
network structures, their associated data and dynamics.

This implementation does not suppor
