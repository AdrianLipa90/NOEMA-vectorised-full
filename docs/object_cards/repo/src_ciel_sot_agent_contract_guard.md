# contract_guard.py — src/ciel_sot_agent/contract_guard.py

## Tożsamość
- **id_karty:** `REPO-CONTRACT_GUARD-DC3B`
- **ścieżka:** `src/ciel_sot_agent/contract_guard.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.161`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/contract_guard.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.161 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
Hard contract guard for AI-SAPIENS interaction packets.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ContractViolation, GuardResult
- **funkcje:** `_require`, `validate_surface_policy`, `validate_inference_contract`, `validate_sapiens_packet`

## Opis
Hard contract guard for AI-SAPIENS interaction packets.

This module turns the relational-formal contract into executable checks.  It is
intentionally strict: missing truth discipline is a runtime error, not a note.
