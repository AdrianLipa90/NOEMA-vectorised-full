# polish_j_components.py — src/cielingo_core/language_spaces/pl/polish_j_components.py

## Tożsamość
- **id_karty:** `REPO-POLISH_J_COMPONENTS-B931`
- **ścieżka:** `src/cielingo_core/language_spaces/pl/polish_j_components.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.996`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/language_spaces/pl/polish_j_components.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.996 |
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
