# noema_knowledge_graph.py — scripts/noema_knowledge_graph.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_KNOWLEDGE_GRAP-1951`
- **ścieżka:** `scripts/noema_knowledge_graph.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.935`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_knowledge_graph.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.935 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
NOEMA Knowledge Graph — maps PhaseNav operators ↔ PDF topics ↔ relational ontology.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** KnowledgeGraph
- **funkcje:** `build_graph`, `add_node`, `add_edge`, `get`, `neighbors`, `find_path`, `to_dict`, `save`

## Opis
NOEMA Knowledge Graph — maps PhaseNav operators ↔ PDF topics ↔ relational ontology.

Builds a directed graph from:
  - PhaseNav operators (35 total)
  - Library topics (432 from catalog)
  - Author entities
  - Relational edges (influence, describes, defines, references, implements)

Output: PHASE_INDEX/knowledge_graph.json (nodes + edges + adjacency)

Usage:
    .venv/bin/python3 scripts/noema_kn
