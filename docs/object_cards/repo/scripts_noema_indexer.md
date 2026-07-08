# noema_indexer.py — scripts/noema_indexer.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_INDEXER-B971`
- **ścieżka:** `scripts/noema_indexer.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.235`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_indexer.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.235 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
NOEMA PhaseNav Indexer — build search index from documents to phase vectors.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_tokenize`, `text_to_phase_vector`, `phase_vector_to_disk`, `holonomy_between`, `_collect_documents`, `_read_text`, `build_index`, `load_index`, `search`, `probe_index`

## Opis
NOEMA PhaseNav Indexer — build search index from documents to phase vectors.

Indexes documents (PDF, txt, md, jsonl) into N_OSCILLATORS (36) phase vectors stored as
binary mmap files in the INDEX library. Each document gets:
  - N_OSCILLATORS-D phase vector (normalized sum of term→oscillator projections)
  - metadata (path, size, term count, dominant oscillator)

Search: encode query as N_OSCILLA
