# noema_search.py — scripts/noema_search.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SEARCH-EB20`
- **ścieżka:** `scripts/noema_search.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.932`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_search.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.932 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
NOEMA Search — combined web + local PhaseNav-powered search.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_tokenize`, `text_to_phase_vector`, `holonomy_between`, `enhance_with_operators`, `_load_index`, `search_local`, `search_web`, `search_all`

## Opis
NOEMA Search — combined web + local PhaseNav-powered search.

Search across:
  - Web: using internet search, results ranked by PhaseNav holonomy
  - Local: PhaseNav-indexed documents from NOEMA_LIBRARY/INDEX
  - PhaseNav: Berry curvature between query and documents

Usage:
    .venv/bin/python3 scripts/noema_search.py "quantum gravity phase transition"
    .venv/bin/python3 scripts/noema_search.py
