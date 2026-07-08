# pajek.py — .python_packages/networkx/readwrite/pajek.py

## Tożsamość
- **id_karty:** `REPO-PAJEK-E540`
- **ścieżka:** `.python_packages/networkx/readwrite/pajek.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.375`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/readwrite/pajek.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.375 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
*****

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `generate_pajek`, `write_pajek`, `read_pajek`, `parse_pajek`, `make_qstr`

## Opis
*****
Pajek
*****
Read graphs in Pajek format.

This implementation handles directed and undirected graphs including
those with self loops and parallel edges.

Format
------
See http://vlado.fmf.uni-lj.si/pub/networks/pajek/doc/draweps.htm
for format information.
