# local_ciel_surface.py — build/lib/ciel_sot_agent/local_ciel_surface.py

## Tożsamość
- **id_karty:** `REPO-LOCAL_CIEL_SURFACE-954B`
- **ścieżka:** `build/lib/ciel_sot_agent/local_ciel_surface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.577`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/local_ciel_surface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.577 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


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
