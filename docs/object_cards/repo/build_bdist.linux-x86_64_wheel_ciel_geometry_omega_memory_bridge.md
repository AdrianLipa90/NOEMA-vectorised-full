# omega_memory_bridge.py — build/bdist.linux-x86_64/wheel/ciel_geometry/omega_memory_bridge.py

## Tożsamość
- **id_karty:** `REPO-OMEGA_MEMORY_BRIDGE-C6DA`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/omega_memory_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.708`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/omega_memory_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.708 |
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
CIEL Omega Memory Bridge — łączy agenta z TSM ledgerem pamięci.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
