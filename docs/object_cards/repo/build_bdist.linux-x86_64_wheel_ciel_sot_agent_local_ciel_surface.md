# local_ciel_surface.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/local_ciel_surface.py

## Tożsamość
- **id_karty:** `REPO-LOCAL_CIEL_SURFACE-EB64`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/local_ciel_surface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.767`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/local_ciel_surface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.767 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Canonical local CIEL/Ω test surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LocalCielSurface
- **funkcje:** `_omega_root`, `_ensure_omega_path`, `build_arg_parser`, `main`, `shutdown`, `handshake`, `status`, `process`, `communicate`

## Opis
Canonical local CIEL/Ω test surface.

This module bridges the packaged integration repo (`ciel_sot_agent`) with the
canonical local Omega surface living under:
    src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/

Goal:
- provide one stable, package-facing CLI for local tests
- expose orchestrator and client through one consistent interface
- keep local invocation deterministic and lightweight
