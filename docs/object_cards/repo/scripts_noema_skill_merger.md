# noema_skill_merger.py — scripts/noema_skill_merger.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SKILL_MERGER-06FF`
- **ścieżka:** `scripts/noema_skill_merger.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.306`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_skill_merger.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.306 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
noema_skill_merger.py — merge'owanie i tworzenie nowych skilli przez import.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `merge_skills`, `from_code`, `from_import`, `list_groups`

## Opis
noema_skill_merger.py — merge'owanie i tworzenie nowych skilli przez import.

Użycie:
  python3 scripts/noema_skill_merger.py --list                    # lista merge grup
  python3 scripts/noema_skill_merger.py --group lns-reports       # merge grupy
  python3 scripts/noema_skill_merger.py --custom "nazwa" --skills "skill1,skill2"  # custom merge
  python3 scripts/noema_skill_merger.py --from-code
