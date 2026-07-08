# noema_key_inject.py — scripts/noema_key_inject.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_KEY_INJECT-04AC`
- **ścieżka:** `scripts/noema_key_inject.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.307`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_key_inject.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.307 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
NOEMA Key Inject — XTEST injection do okna opencode.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `open_display`, `close_display`, `get_keysym`, `keysym_to_keycode`, `key_press`, `key_release`, `flush`, `inject_text`, `main`

## Opis
NOEMA Key Inject — XTEST injection do okna opencode.
Wstrzykuje tekst przez XTEST (symulacja klawiatury) do aktywnego okna.

Usage:
    python3 scripts/noema_key_inject.py "tekst do wpisania"
    python3 scripts/noema_key_inject.py --enter "tekst z enterem na końcu"
    python3 scripts/noema_key_inject.py --file /tmp/ciel_inject.txt  # stdin/pipe
