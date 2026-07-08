# ciel_knowledge_query.py — scripts/ciel_knowledge_query.py

## Tożsamość
- **id_karty:** `REPO-CIEL_KNOWLEDGE_QUERY-0F33`
- **ścieżka:** `scripts/ciel_knowledge_query.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.917`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_knowledge_query.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.917 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
ciel_knowledge_query.py — Direct Knowledge DB access from opencode.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_get_db`, `_load_embeddings`, `_cosine_sim`, `_query_to_embedding`, `_load_confidence`, `embed_search`, `tfidf_search`, `sql_query`, `info`, `search`, `main`

## Opis
ciel_knowledge_query.py — Direct Knowledge DB access from opencode.

Ładuje dane z Knowledge DB (/tmp/noema_knowledge.db) + embeddingów (.npy)
i pozwala na trzy tryby zapytania:

  python3 scripts/ciel_knowledge_query.py "twoje pytanie"      # embed search
  python3 scripts/ciel_knowledge_query.py --sql "SELECT ..."   # direct SQL
  python3 scripts/ciel_knowledge_query.py --info                # s
