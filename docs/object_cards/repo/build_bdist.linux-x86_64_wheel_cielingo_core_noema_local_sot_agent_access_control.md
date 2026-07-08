# access_control.py — build/bdist.linux-x86_64/wheel/cielingo_core/noema_local_sot_agent/access_control.py

## Tożsamość
- **id_karty:** `REPO-ACCESS_CONTROL-23F2`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/noema_local_sot_agent/access_control.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.788`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/noema_local_sot_agent/access_control.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.788 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Access-control standard for local SOT_Agent_NoemaSurface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AccessDecision, AccessPolicy, LocalSOTAccessController
- **funkcje:** `utc_now`, `canonical_json`, `sha256_text`, `build_default_access_standard`, `to_dict`, `to_dict`, `classify_path`, `can_write`

## Opis
Access-control standard for local SOT_Agent_NoemaSurface.

This module implements local artifact permissions only. It is not OS sudo, not
external NOEMA SoT, not account-global GPT infrastructure, and not USER007 disk
access. It exists so future agents can verify which paths are normal CIELingo
work and which edits require an explicit Adrian ALLOW grant.
