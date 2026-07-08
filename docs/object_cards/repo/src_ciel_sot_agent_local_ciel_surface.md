# local_ciel_surface.py — src/ciel_sot_agent/local_ciel_surface.py

## Tożsamość
- **id_karty:** `REPO-LOCAL_CIEL_SURFACE-7CBB`
- **ścieżka:** `src/ciel_sot_agent/local_ciel_surface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.429`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/local_ciel_surface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.429 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


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
