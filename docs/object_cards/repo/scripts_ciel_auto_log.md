# ciel_auto_log.py — scripts/ciel_auto_log.py

## Tożsamość
- **id_karty:** `REPO-CIEL_AUTO_LOG-D05A`
- **ścieżka:** `scripts/ciel_auto_log.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.653`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_auto_log.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.653 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
CIEL Auto-Log — konstytutywny logger rozmów.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_get_session_info`, `_get_log_path`, `_ensure_raw_db_schema`, `_write_live_raw_db`, `log_entry`, `batch_import`

## Opis
CIEL Auto-Log — konstytutywny logger rozmów.

Usage:
    # Log odpowiedź (ostatnia rzecz przed wysłaniem tekstu)
    python3 scripts/ciel_auto_log.py --role assistant --content "To jest odpowiedź" --tags "trigger-rebuild,settings-fix"

    # Log wiadomość usera
    python3 scripts/ciel_auto_log.py --role user --content "Zrób X" --tags "command"

    # Batch log: stdin JSONL
    cat entries.jsonl |
