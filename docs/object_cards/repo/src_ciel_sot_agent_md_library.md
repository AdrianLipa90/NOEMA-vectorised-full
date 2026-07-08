# md_library.py — src/ciel_sot_agent/md_library.py

## Tożsamość
- **id_karty:** `REPO-MD_LIBRARY-A257`
- **ścieżka:** `src/ciel_sot_agent/md_library.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.247`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/md_library.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.247 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
MD Library — System Informacji o Systemie (SIS).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_categorize`, `_extract_title`, `_extract_tags`, `scan`, `build`

## Opis
MD Library — System Informacji o Systemie (SIS).

Skanuje wszystkie pliki .md w CIEL1 i buduje indeks z kategoryzacją,
tytułami i tagami. Wynik zapisuje do integration/registries/md_library_index.json.

Usage:
    python -m ciel_sot_agent.md_library
