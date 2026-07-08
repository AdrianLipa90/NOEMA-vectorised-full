# infinitive_modal_potential.py — build/lib/cielingo/infinitive_modal_potential.py

## Tożsamość
- **id_karty:** `REPO-INFINITIVE_MODAL_POT-9AEA`
- **ścieżka:** `build/lib/cielingo/infinitive_modal_potential.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.881`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/infinitive_modal_potential.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.881 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


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
