# ciel_graph_extractor.py — scripts/ciel_graph_extractor.py

## Tożsamość
- **id_karty:** `REPO-CIEL_GRAPH_EXTRACTOR-CC21`
- **ścieżka:** `scripts/ciel_graph_extractor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.304`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_graph_extractor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.304 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
CIEL Graph Extractor — draft/experimental

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Entity, Relation
- **funkcje:** `extract_entities`, `extract_relations`, `update_subject_file`, `update_graph_index`, `process_report`, `run_live`, `main`

## Opis
CIEL Graph Extractor — draft/experimental

Wyciąga podmioty i relacje z artykułów RSS i aktualizuje NEWS/GRAPH.md + subjects/*.md.

Słownik znaczeń, nie prawdopodobieństw:
  - węzeł = podmiot (państwo, osoba, organizacja, koncepcja)
  - krawędź = relacja (CONFLICT_WITH, ALLIED_WITH, NEGOTIATES_WITH, CAUSES, itd.)
  - waga krawędzi = liczba co-occurrence + typ relacji

EXPERIMENTAL = True  — nie wc
