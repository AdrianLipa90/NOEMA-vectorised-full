# card_ontology.py — src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/card_ontology.py

## Tożsamość
- **id_karty:** `REPO-CARD_ONTOLOGY-5177`
- **ścieżka:** `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/card_ontology.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.785`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/card_ontology.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.785 |
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
Card ontology utilities for CIELingo v1.7.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CardTypeSpec
- **funkcje:** `load_card_ontology`, `card_type_specs`, `infer_card_type_from_path`, `validate_payload_shape`, `ontology_required_paths`, `required_path_status`, `classify_repository_files`

## Opis
Card ontology utilities for CIELingo v1.7.

The ontology protects the core distinction:
concept cards are semantic masses; operator cards are forces/functions;
grammar, case, TAM-E, scope, deixis, and event frames are typed control layers.
