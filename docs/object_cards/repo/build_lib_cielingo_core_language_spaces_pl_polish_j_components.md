# polish_j_components.py — build/lib/cielingo_core/language_spaces/pl/polish_j_components.py

## Tożsamość
- **id_karty:** `REPO-POLISH_J_COMPONENTS-ECCD`
- **ścieżka:** `build/lib/cielingo_core/language_spaces/pl/polish_j_components.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.909`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/language_spaces/pl/polish_j_components.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.909 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
Polish J components v0.2.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PolishJComponent
- **funkcje:** `clamp01`, `compute_polish_j_components`, `polish_j_components_to_notes`, `to_dict`

## Opis
Polish J components v0.2.

Maps PL surface diagnostics into bounded scalar J components. These are not
physical Kuramoto measurements.
