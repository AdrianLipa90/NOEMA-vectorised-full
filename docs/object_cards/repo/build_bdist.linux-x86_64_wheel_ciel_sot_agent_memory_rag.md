# memory_rag.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/memory_rag.py

## Tożsamość
- **id_karty:** `REPO-MEMORY_RAG-4FB3`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/memory_rag.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.280`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/memory_rag.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.280 |
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
CIEL Memory RAG — retrieval-augmented generation from wave_archive + chat history.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_keywords`, `_score`, `search_wave_archive`, `search_chat_history`, `build_memory_context`, `rd`

## Opis
CIEL Memory RAG — retrieval-augmented generation from wave_archive + chat history.

Searches memories for content relevant to the current query and returns
a context block to inject into the system prompt before model inference.

This is inference-time learning: the model sees its own memories on every response.
Actual weight updates (LoRA) are separate — see scripts/train_lora.py.
