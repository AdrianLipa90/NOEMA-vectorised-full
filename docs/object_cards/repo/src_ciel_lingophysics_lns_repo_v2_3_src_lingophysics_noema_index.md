# noema_index.py — src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/noema_index.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_INDEX-1D9F`
- **ścieżka:** `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/noema_index.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.346`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/noema_index.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.346 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
NOEMA index primitives for CIELingo v2.2.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NoemaCard
- **funkcje:** `tokenize`, `load_noema_index`, `cards_from_index`, `score_card`, `search_noema`, `compact_context_bundle`, `from_dict`, `all_label_tokens`, `has_language`

## Opis
NOEMA index primitives for CIELingo v2.2.

The index is intentionally lightweight: it routes queries to concept/operator/
grammar cards before any model is invoked. It is not a vector database yet; it
is a deterministic seed layer that can later be backed by embeddings or graph
indices.
