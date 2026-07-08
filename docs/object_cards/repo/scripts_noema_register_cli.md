# noema_register_cli.py — scripts/noema_register_cli.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_REGISTER_CLI-A8F4`
- **ścieżka:** `scripts/noema_register_cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.396`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_register_cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.396 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
CLI for NOEMA Registry — manage daemon registration tokens.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `cmd_register`, `cmd_list`, `cmd_heartbeat`, `cmd_unregister`, `cmd_check`, `cmd_cleanup`, `main`

## Opis
CLI for NOEMA Registry — manage daemon registration tokens.

Usage:
    python scripts/noema_register_cli.py register <name> [--claims ...]
    python scripts/noema_register_cli.py list [--timeout 30]
    python scripts/noema_register_cli.py heartbeat <token>
    python scripts/noema_register_cli.py unregister <token>
    python scripts/noema_register_cli.py check <token> <file>
    python scripts
