# cross_language.py — build/bdist.linux-x86_64/wheel/cielingo_core/alignment/cross_language.py

## Tożsamość
- **id_karty:** `REPO-CROSS_LANGUAGE-2B77`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/alignment/cross_language.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.569`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/alignment/cross_language.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.569 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


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
