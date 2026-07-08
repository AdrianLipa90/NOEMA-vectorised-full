# infinitive_modal_potential.py — build/bdist.linux-x86_64/wheel/cielingo/infinitive_modal_potential.py

## Tożsamość
- **id_karty:** `REPO-INFINITIVE_MODAL_POT-37B3`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/infinitive_modal_potential.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.629`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/infinitive_modal_potential.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.629 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Infinitive -> modality potential layer for CIELingo.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** InfinitiveSeed, ModalitySeed, ModalMapping
- **funkcje:** `_bounded`, `_phase_from_id`, `_oscillator_id`, `_angle_delta`, `_mass_from_axes`, `_collatz_summary`, `_is_polish_infinitive`, `_infinitive_from_card`, `load_infinitive_seeds`, `load_modality_seeds`, `_axis_affinity`, `_lexical_phase_affinity`, `map_infinitive_to_modalities`, `infinitive_modal_report`, `write_report`, `as_dict`, `as_dict`, `as_dict`

## Opis
Infinitive -> modality potential layer for CIELingo.

This module models words before full sentence inference:

    infinitive seed -> modality map -> Collatz seed -> HTRI phase bus

The layer is deliberately scalar/diagnostic.  A Polish infinitive and a
modality receive rest semantic mass and an information potential measured in
``kappa_info = ln(2)/(24*pi)`` units.  Their semantic-linguistic pot
