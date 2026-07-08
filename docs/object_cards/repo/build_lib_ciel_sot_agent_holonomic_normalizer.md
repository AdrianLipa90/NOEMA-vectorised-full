# holonomic_normalizer.py — build/lib/ciel_sot_agent/holonomic_normalizer.py

## Tożsamość
- **id_karty:** `REPO-HOLONOMIC_NORMALIZER-D32C`
- **ścieżka:** `build/lib/ciel_sot_agent/holonomic_normalizer.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.367`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/holonomic_normalizer.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.367 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Holonomic phase normalizer for the CIEL integration kernel.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** HolonomicCallbacks
- **funkcje:** `wrap`, `circular_barycenter`, `circular_distance`, `symmetrize_couplings`, `clip_couplings`, `renormalize_couplings`, `triplet_tension`, `_get`, `_set`, `_sector`, `_select_control_mode`, `holonomic_system_normalizer_v2`

## Opis
Holonomic phase normalizer for the CIEL integration kernel.

Provides circular-arithmetic utilities (phase wrapping, circular barycenter,
circular distance) and the HolonomicNormalizer class that applies weighted
renormalization across a map of named phase-carrying nodes.
