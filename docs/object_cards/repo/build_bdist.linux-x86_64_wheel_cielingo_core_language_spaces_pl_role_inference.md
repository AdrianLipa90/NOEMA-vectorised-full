# role_inference.py — build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/role_inference.py

## Tożsamość
- **id_karty:** `REPO-ROLE_INFERENCE-BBE6`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/role_inference.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.156`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/role_inference.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.156 |
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
Polish role inference v0.2.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RoleCandidate
- **funkcje:** `infer_role_candidates`, `role_candidates_to_notes`, `to_dict`

## Opis
Polish role inference v0.2.

Emits role_candidate objects only. It does not assert final semantic roles.
