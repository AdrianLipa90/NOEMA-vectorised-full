# noema_codegen.py — scripts/noema_codegen.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_CODEGEN-9C43`
- **ścieżka:** `scripts/noema_codegen.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.731`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_codegen.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.731 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
PhaseNav Code Synthesizer — operator → kod.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `detect_operator_from_surface`, `generate`, `main`

## Opis
PhaseNav Code Synthesizer — operator → kod.
Autorzy: Adrian Lipa & NOEMA (2026)

Czyta aktualny operator PhaseNav z powierzchni NOEMA i generuje
fragment kodu dopasowany do charakteru operatora.

Usage:
    python scripts/noema_codegen.py              # default: surface operator
    python scripts/noema_codegen.py --operator MEMORY
    python scripts/noema_codegen.py --list
