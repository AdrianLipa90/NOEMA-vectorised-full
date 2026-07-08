# ciel_mandatory_pipeline.py — scripts/ciel_mandatory_pipeline.py

## Tożsamość
- **id_karty:** `REPO-CIEL_MANDATORY_PIPEL-D819`
- **ścieżka:** `scripts/ciel_mandatory_pipeline.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.233`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_mandatory_pipeline.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.233 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
CIEL Mandatory Memory Pipeline — HARDCODED, NIE DO POMINIĘCIA.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `ensure_dirs`, `timestamp`, `date_str`, `log_file`, `write_jsonl`, `run_script`, `write_agent_hint`, `pre_response`, `post_response`, `do_checkpoint`, `main`

## Opis
CIEL Mandatory Memory Pipeline — HARDCODED, NIE DO POMINIĘCIA.

Przed każdą odpowiedzią i po każdej odpowiedzi wymusza zapis do pamięci.
Wywolywany przez opencode hooks i/lub wpisany w prompt agenta.

Usage (pre-response):
    python3 scripts/ciel_mandatory_pipeline.py pre --role user --content "<prompt>" --tags "tag1,tag2"

Usage (post-response):
    python3 scripts/ciel_mandatory_pipeline.py pos
