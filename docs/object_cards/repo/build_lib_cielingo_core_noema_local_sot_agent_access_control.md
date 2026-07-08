# access_control.py — build/lib/cielingo_core/noema_local_sot_agent/access_control.py

## Tożsamość
- **id_karty:** `REPO-ACCESS_CONTROL-14FA`
- **ścieżka:** `build/lib/cielingo_core/noema_local_sot_agent/access_control.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.524`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/noema_local_sot_agent/access_control.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.524 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


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
