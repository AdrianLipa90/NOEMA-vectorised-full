# infinitive_merge_audit.py — build/lib/cielingo/infinitive_merge_audit.py

## Tożsamość
- **id_karty:** `REPO-INFINITIVE_MERGE_AUD-A132`
- **ścieżka:** `build/lib/cielingo/infinitive_merge_audit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.744`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/infinitive_merge_audit.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.744 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
CIELingo infinitivization + residual-set merge audit.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** InfinitiveCandidate, ResidualAssignment, OwnedResidualSet
- **funkcje:** `utc_now`, `normalize_word`, `sha256_json`, `bounded`, `read_unknown_entries`, `is_direct_infinitive`, `infinitivize_word`, `merge_semantic_state`, `build_infinitive_candidates`, `residual_set_for_word`, `build_residual_assignments`, `build_owned_residual_sets`, `write_jsonl`, `generate_infinitive_merge_audit`, `as_dict`, `as_dict`, `as_dict`

## Opis
CIELingo infinitivization + residual-set merge audit.

This stage operates after ``unknown_word_audit``.  It tries to convert unknown
word surfaces to infinitive/action seeds where the local morphology heuristic is
safe enough, merges each infinitive candidate with the existing unknown-state
record, and assigns every remaining word to an owned residual set.

It never claims canonical morphology.
