# phasenav_24d_bridge.py — runtime/phasenav_24d_bridge.py

## Tożsamość
- **id_karty:** `REPO-PHASENAV_24D_BRIDGE-F2EC`
- **ścieżka:** `runtime/phasenav_24d_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.861`
- **masa_semantyczna:** `0.40`

## Kotwice
- `runtime/phasenav_24d_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.861 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
PhaseNav24DBridge — łączy 24D bibliotekę z pulpitu z PhaseNav i CIELingo.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LibraryEntry24D, Library24D
- **funkcje:** `load_24d_library`, `bridge_to_phasenav`, `bridge_to_cielingo`, `bridge_to_subconscious`, `full_bridge`, `phase_24d`, `n_entries`

## Opis
PhaseNav24DBridge — łączy 24D bibliotekę z pulpitu z PhaseNav i CIELingo.

Źródło: /home/adrian/new_volume_rw/NOEMA_PHASE_DATA/PHASE_INDEX/
  - library_index.npy: 1287 × 24D wektory
  - library_meta.npy: metadane (id, filename, author, topic)
  - knowledge_graph.json: graf wiedzy (operatory, topic, autorzy)
  - adrian_composite_24d.npy: 24D kompozyt Adriana

Funkcje:
  1. load_24d_library() — wczy
