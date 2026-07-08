# object_cards.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/object_cards.py

## Tożsamość
- **id_karty:** `REPO-OBJECT_CARDS-CC50`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/object_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `1.040`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/object_cards.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 1.040 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

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
CIEL Object Cards — Keplerian semantic ontology.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** ObjectCard, FeatureCard, ClosureOp, AffectCard, SentenceEquation
- **funkcje:** `_pos_tag`, `_extract_concepts`, `_extract_features`, `_extract_closureops`, `_cyclic_dist`, `_circular_mean_std`, `_semantic_mass`, `_parse_orbital_powiazania`, `build_cards`, `build_features`, `build_closure_ops`, `affect_of`, `get_affects`, `parse_sentence`, `get_cards`, `get_features`, `related`, `opposites`, `phase_neighbors`, `attractors`, `adaptive_delta`, `process_and_stamp`, `to_dict`, `to_dict`, `to_dict`, `to_dict`, `to_dict`

## Opis
CIEL Object Cards — Keplerian semantic ontology.

Grammar-as-physics: parts of speech are dynamical roles in phase space.

  ┌─ ObjectCard (noun) ──────────────────────────────────────────────────────┐
  │  M(c) = freq × closure_mean × log1p(winding_mean) × phase_stability     │
  │  Asymmetric W_ij: W(A→B) = base × (M_B / (M_A + M_B))                  │
  │  Aharonov-Bohm links via mediating conc
