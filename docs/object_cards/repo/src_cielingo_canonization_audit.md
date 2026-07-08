# canonization_audit.py — src/cielingo/canonization_audit.py

## Tożsamość
- **id_karty:** `REPO-CANONIZATION_AUDIT-A38F`
- **ścieżka:** `src/cielingo/canonization_audit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.324`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/canonization_audit.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.324 |
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
CIELingo local canonization audit.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CanonizationDecision
- **funkcje:** `utc_now`, `sha256_json`, `read_jsonl`, `write_jsonl`, `decide_infinitive`, `decide_residual_assignment`, `generate_canonization_audit`, `as_dict`

## Opis
CIELingo local canonization audit.

This module checks the results of the unknown-word and infinitive-merge stages
and canonizes only what can be canonized locally without pretending dictionary
truth.

Canonicalization levels used here:

* ``external_canon``: requires imported/open-source lexical evidence. This patch
  does not create any external canon entries because no Wiktionary/SGJP/
  Morfeu
