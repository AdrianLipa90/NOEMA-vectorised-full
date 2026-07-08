# holonomic_normalizer.py — src/ciel_sot_agent/holonomic_normalizer.py

## Tożsamość
- **id_karty:** `REPO-HOLONOMIC_NORMALIZER-8332`
- **ścieżka:** `src/ciel_sot_agent/holonomic_normalizer.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.028`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/holonomic_normalizer.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.028 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
