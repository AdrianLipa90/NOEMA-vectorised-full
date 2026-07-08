# p2g.py — .python_packages/networkx/readwrite/p2g.py

## Tożsamość
- **id_karty:** `REPO-P2G-E845`
- **ścieżka:** `.python_packages/networkx/readwrite/p2g.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.246`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/readwrite/p2g.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.246 |
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
This module provides the following: read and write of p2g format

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `write_p2g`, `read_p2g`, `parse_p2g`

## Opis
This module provides the following: read and write of p2g format
used in metabolic pathway studies.

See:
<https://web.archive.org/web/20080626113807/http://www.cs.purdue.edu/homes/koyuturk/pathway/>
for a description.

The summary is included here:

A file that describes a uniquely labeled graph (with extension ".gr")
format looks like the following:


name
3 4
a
1 2
b

c
0 2

"name" is simply a
