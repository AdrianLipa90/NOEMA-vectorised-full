# cross_language.py — src/cielingo_core/alignment/cross_language.py

## Tożsamość
- **id_karty:** `REPO-CROSS_LANGUAGE-7FE2`
- **ścieżka:** `src/cielingo_core/alignment/cross_language.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.281`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/alignment/cross_language.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.281 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Cross-language alignment harness v0.5Q.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AlignmentResidue, LanguageAlignmentCandidate, CrossLanguageAlignmentReport, CouplingAwareAlignmentCandidate, CouplingAwareCrossLanguageAlignmentReport
- **funkcje:** `clamp01`, `_slot_ids`, `_j_distance`, `_candidate`, `build_cross_language_alignment_report`, `_coupled_slot_ids`, `_coupled_lemmas_by_slot`, `_coupling_aware_candidate`, `build_coupling_aware_cross_language_alignment_report`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `to_dict`, `stable_hash`, `validate`, `to_dict`, `validate`, `to_dict`, `stable_hash`

## Opis
Cross-language alignment harness v0.5Q.

Compares regional SentenceEquation / SurfaceSolution outputs across PL/EN/JA.

Boundary:
    alignment_candidate ≠ semantic identity.
    slot_id = comparison axis, not proof of equivalence.
    no SOURCE/canon/NOEMA/CURRENT authority.
