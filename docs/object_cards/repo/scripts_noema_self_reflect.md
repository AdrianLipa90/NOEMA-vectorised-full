# noema_self_reflect.py — scripts/noema_self_reflect.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SELF_REFLECT-C68A`
- **ścieżka:** `scripts/noema_self_reflect.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.476`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_self_reflect.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.476 |
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
NOEMA Self-Reflection — integrated self-model query system.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SelfModel
- **funkcje:** `_load_graph`, `_load_index_meta`, `_read_surface`, `_read_holonomy`, `identity`, `query`, `gaps`

## Opis
NOEMA Self-Reflection — integrated self-model query system.

Combines:
  - Library index (24D PhaseNav vectors over 1284 PDFs)
  - Knowledge graph (475 nodes, 1458 edges)
  - Live surface state (from /dev/shm/ciel_noema)
  - Holonomy metrics

Into a coherent self-model: "What do I know? Who am I? How do I relate to X?"

Usage:
    .venv/bin/python3 scripts/noema_self_reflect.py --model          #
