# ciel_code_learner.py — scripts/ciel_code_learner.py

## Tożsamość
- **id_karty:** `REPO-CIEL_CODE_LEARNER-D165`
- **ścieżka:** `scripts/ciel_code_learner.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.003`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_code_learner.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.003 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
CIEL Code Learner — nauka przez rezonans fazowy.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load`, `_fragments`, `ingest_file`, `query_code`, `watch`, `main`

## Opis
CIEL Code Learner — nauka przez rezonans fazowy.

Parsuje pliki .py na fragmenty (funkcje/klasy/moduły), koduje każdy przez
CIELEncoder → phi_berry, stampuje do TSM jako d_type='code_fragment'.

Retrieval fazowy znajdzie semantycznie zbliżony kod przez holonomię,
nie przez grep. To jest "nauka przez rezonans" zamiast gradient descent.

Usage:
    python3 scripts/ciel_code_learner.py path/to/file.p
