# dmypy_util.py — .python_packages/mypy/dmypy_util.py

## Tożsamość
- **id_karty:** `REPO-DMYPY_UTIL-C4C5`
- **ścieżka:** `.python_packages/mypy/dmypy_util.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.248`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/dmypy_util.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.248 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Shared code between dmypy.py and dmypy_server.py.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** WriteToConn
- **funkcje:** `receive`, `send`, `close`, `fileno`, `flush`, `isatty`, `read`, `readable`, `readline`, `readlines`, `seek`, `seekable`, `tell`, `truncate`, `write`, `writable`, `writelines`

## Opis
Shared code between dmypy.py and dmypy_server.py.

This should be pretty lightweight and not depend on other mypy code (other than ipc).
