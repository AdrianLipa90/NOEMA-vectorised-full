# canonization_audit.py — build/lib/cielingo/canonization_audit.py

## Tożsamość
- **id_karty:** `REPO-CANONIZATION_AUDIT-159D`
- **ścieżka:** `build/lib/cielingo/canonization_audit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.793`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/canonization_audit.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.793 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


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
