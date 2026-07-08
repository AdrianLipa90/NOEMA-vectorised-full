# noema_learn_file.py — scripts/noema_learn_file.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_LEARN_FILE-6030`
- **ścieżka:** `scripts/noema_learn_file.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.803`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_learn_file.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.803 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
Pełny pipeline: plik → PhaseNav koncept → biblioteka → surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_normalize`, `_nearest_operator`, `learn_file`

## Opis
Pełny pipeline: plik → PhaseNav koncept → biblioteka → surface.

Usage:
    .venv/bin/python3 scripts/noema_learn_file.py <ścieżka_do_pliku>

Kroki:
  1. Czyta plik, wyciąga tekst
  2. Przez phasenav_enrich → 24D vector + operator
  3. Dodaje do library_index.npy + library_meta.npy
  4. Rebuild zip_catalog/index.jsonl
  5. Restartuje PhaseNav cold (przez systemd)
  6. Opcjonalnie: pyta agent backe
