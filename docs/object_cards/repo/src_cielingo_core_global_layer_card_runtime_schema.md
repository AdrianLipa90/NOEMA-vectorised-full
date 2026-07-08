# card_runtime_schema.py — src/cielingo_core/global_layer/card_runtime_schema.py

## Tożsamość
- **id_karty:** `REPO-CARD_RUNTIME_SCHEMA-0626`
- **ścieżka:** `src/cielingo_core/global_layer/card_runtime_schema.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.341`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/card_runtime_schema.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.341 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
CIELingo card runtime schema v0.3.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CardOntologyClass, CardValidationStatus, ConsentEffect, MemoryEffect, RiskProfile, ResidueProfile, NoemaHolonomicMarker, RuntimeCardExtension, CielingoRuntimeCard
- **funkcje:** `_bounded01`, `validate`, `validate`, `validate`, `validate`, `validate`, `to_dict`

## Opis
CIELingo card runtime schema v0.3.

This module defines additive runtime/operator extensions for cards.

It does not replace lexical slots or language-local cards. It adds the
fields needed by GLOBAL v0.2/v0.3:
- operator bindings,
- semantic mass,
- affective charge,
- consent/memory/risk effects,
- residue profile,
- NOEMA holonomic marker.

No card is SOURCE or canon by default.
