# ciel_noema_doc_embedder.py — scripts/ciel_noema_doc_embedder.py

## Tożsamość
- **id_karty:** `REPO-CIEL_NOEMA_DOC_EMBED-933A`
- **ścieżka:** `scripts/ciel_noema_doc_embedder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.393`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_noema_doc_embedder.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.393 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
CIELingo Document Embedder — Knowledge DB → 36D PhaseNav embedding.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_kb`, `_load_tfidf`, `_compute_channel_weights`, `_compute_affect_valence`, `_doc_to_phi`, `_embed_docs`, `_build_index`, `save`, `load`, `query`, `main`

## Opis
CIELingo Document Embedder — Knowledge DB → 36D PhaseNav embedding.

Czyta Knowledge DB SQLite (545 dokumenty, 562k termów TF-IDF).
Każdy dokument → 36D wektor fazowy kompatybilny z NOEMA PhaseNav:
  12 kanałów pamięci × 3 oscylatory = 36D

Kanały:
  M0 Perceptual       (0-2)   — term frequency, percept density
  M1 Working          (3-5)   — operator density, syntax weight
  M2 Episodic         (
