# omega_memory_bridge.py — src/ciel_geometry/omega_memory_bridge.py

## Tożsamość
- **id_karty:** `REPO-OMEGA_MEMORY_BRIDGE-75E0`
- **ścieżka:** `src/ciel_geometry/omega_memory_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `6.138`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/omega_memory_bridge.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 6.138 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

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
CIEL Omega Memory Bridge — łączy agenta z TSM ledgerem pamięci.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_conn`, `_ensure_schema`, `store`, `retrieve`, `recent`, `store_exchange`, `integrate_with_agent`, `stats`

## Opis
CIEL Omega Memory Bridge — łączy agenta z TSM ledgerem pamięci.

Używa bezpośrednio SQLite na memory_ledger.db (95 istniejących wpisów)
oraz PhaseMemory z CIELingo. Nie wymaga pełnego importu Omega.

API:
    store(memorise_id, content, D_associations="")
    retrieve(query, top_k=5) -> list[dict]
    recent(n=10) -> list[dict]
    stats() -> dict
    integrate_with_agent(state_db) -> None
