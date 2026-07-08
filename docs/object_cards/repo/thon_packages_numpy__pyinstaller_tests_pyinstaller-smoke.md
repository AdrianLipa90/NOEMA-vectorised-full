# pyinstaller-smoke.py — .python_packages/numpy/_pyinstaller/tests/pyinstaller-smoke.py

## Tożsamość
- **id_karty:** `REPO-PYINSTALLER_SMOKE-B0B1`
- **ścieżka:** `.python_packages/numpy/_pyinstaller/tests/pyinstaller-smoke.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.332`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/_pyinstaller/tests/pyinstaller-smoke.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.332 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
A crude *bit of everything* smoke test to verify PyInstaller compatibility.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
A crude *bit of everything* smoke test to verify PyInstaller compatibility.

PyInstaller typically goes wrong by forgetting to package modules, extension
modules or shared libraries. This script should aim to touch as many of those
as possible in an attempt to trip a ModuleNotFoundError or a DLL load failure
due to an uncollected resource. Missing resources are unlikely to lead to
arithmetic error
