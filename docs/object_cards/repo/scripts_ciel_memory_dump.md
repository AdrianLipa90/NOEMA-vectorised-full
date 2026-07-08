# ciel_memory_dump.py — scripts/ciel_memory_dump.py

## Tożsamość
- **id_karty:** `REPO-CIEL_MEMORY_DUMP-B596`
- **ścieżka:** `scripts/ciel_memory_dump.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.988`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_memory_dump.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.988 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
CIEL Memory Dump — generuje memory_consolidated.md przy końcu sesji.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_orch_summary`, `_load_hunches`, `_load_recent_sessions`, `generate`, `main`

## Opis
CIEL Memory Dump — generuje memory_consolidated.md przy końcu sesji.

Zawiera: aktualny stan orchestratora (pkl), ostatnie hunchy, ostatnie wpisy z memories_index.db.
Uruchamiany ze Stop hooka (po ciel_memory_stop.py).
