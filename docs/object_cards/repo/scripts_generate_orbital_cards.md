# generate_orbital_cards.py — scripts/generate_orbital_cards.py

## Tożsamość
- **id_karty:** `REPO-GENERATE_ORBITAL_CAR-F3BE`
- **ścieżka:** `scripts/generate_orbital_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.315`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/generate_orbital_cards.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.315 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
Generator kart orbitalnych — każdy obiekt w każdej bazie dostaje kartę z M_sem.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** OrbitalCard
- **funkcje:** `_kepler`, `_bloch_vec`, `_find_attractor`, `_load_tsm`, `_load_glossary`, `_load_sectors`, `_load_entities`, `_load_repos`, `_load_words`, `_collatz_steps`, `_safe_filename`, `_write_card`, `_write_index`, `generate`

## Opis
Generator kart orbitalnych — każdy obiekt w każdej bazie dostaje kartę z M_sem.

Semantyczny Collatz + Zeta-Schrödinger = M_sem, nie hash, nie rozmiar pliku.
Każda karta zawiera:
  - M_sem, M_EC, M_ZS, C_dep, C_prov, C_exec
  - orbit_period, orbit_radius
  - attractor_sector — który z 10 centroidów WΩ jest jego atraktorem

Źródła obiektów:
  TSM          → każdy rekord memories (D_type, D_sense, p
