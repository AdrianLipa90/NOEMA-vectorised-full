# semantic_scar.py — src/cielingo_core/global_layer/semantic_scar.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_SCAR-DBF2`
- **ścieżka:** `src/cielingo_core/global_layer/semantic_scar.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.111`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/semantic_scar.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.111 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Semantic scar model.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ScarType, SemanticScar
- **funkcje:** `_bounded01`, `validate`, `to_dict`

## Opis
Semantic scar model.

A scar is a preserved trace of unresolved or damaging semantic dynamics:
missing source, contradiction, unresolved word, false closure, etc.
It is not automatically memory writeback.
