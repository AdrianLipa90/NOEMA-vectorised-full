# noema_holonomy.py — src/cielingo_core/global_layer/noema_holonomy.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_HOLONOMY-230A`
- **ścieżka:** `src/cielingo_core/global_layer/noema_holonomy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.902`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/noema_holonomy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.902 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
NOEMA holonomic marker generation for CIELingo cards v0.3.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_clamp01`, `_phase_from_text`, `stable_card_projection`, `stable_card_fingerprint`, `build_noema_holonomic_marker`, `attach_noema_marker`

## Opis
NOEMA holonomic marker generation for CIELingo cards v0.3.

The marker is deterministic and public-safe. It is a commitment to semantic
card structure, not a NOEMA writeback and not runtime proof.
