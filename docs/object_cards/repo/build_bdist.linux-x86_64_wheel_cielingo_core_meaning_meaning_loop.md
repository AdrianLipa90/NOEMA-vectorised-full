# meaning_loop.py — build/bdist.linux-x86_64/wheel/cielingo_core/meaning/meaning_loop.py

## Tożsamość
- **id_karty:** `REPO-MEANING_LOOP-A03B`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/meaning/meaning_loop.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.354`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/meaning/meaning_loop.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.354 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
MeaningLoop / SemanticScar integration v0.7A.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LoopState, SemanticScarType, SemanticScar, MeaningLoop
- **funkcje:** `clamp01`, `_scar`, `build_meaning_loop_from_coupling_alignment`, `validate`, `to_dict`, `validate`, `to_dict`, `stable_hash`

## Opis
MeaningLoop / SemanticScar integration v0.7A.

Integrates sentence-card coupling and coupling-aware cross-language alignment
with explicit closure/debt/scar diagnostics.

Boundaries:
- SemanticScar is a diagnostic trace, not punishment;
- MeaningLoop is a closure/debt model, not memory writeback;
- no SOURCE/canon/NOEMA/CURRENT authority.
