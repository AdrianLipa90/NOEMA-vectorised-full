# ciel_benchmark_retrieval.py — scripts/ciel_benchmark_retrieval.py

## Tożsamość
- **id_karty:** `REPO-CIEL_BENCHMARK_RETRI-9993`
- **ścieżka:** `scripts/ciel_benchmark_retrieval.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.372`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_benchmark_retrieval.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.372 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
CIEL Retrieval Benchmark — 4 warianty, tylko wewnętrzny pipeline.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load`, `_keywords_from_tags`, `_text_relevant`, `_build_query_set`, `_cyclic_dist`, `_cosine`, `_rank_ciel_full`, `_rank_phase_only`, `_rank_cosine`, `_rank_random`, `_precision_at_k`, `_reciprocal_rank`, `_phase_resonance`, `_mean_closure`, `_run_benchmark`, `main`

## Opis
CIEL Retrieval Benchmark — 4 warianty, tylko wewnętrzny pipeline.

Porównuje:
  CIEL-FULL       — holonomic_weight (faza + CP² + Poincaré + Hebbian spreading)
  CIEL-PHASE-ONLY — ranking po odległości fazowej |φ_berry − φ_query|
  CIEL-COSINE     — cosine similarity embeddingów (odpowiednik vector DB)
  CIEL-RANDOM     — null hypothesis

Ground truth: proxy relevance z tagów hunches + słów kluczow
