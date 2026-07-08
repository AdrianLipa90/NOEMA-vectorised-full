# command_prompt.py — build/lib/cielingo_core/noema_surface/command_prompt.py

## Tożsamość
- **id_karty:** `REPO-COMMAND_PROMPT-1EC0`
- **ścieżka:** `build/lib/cielingo_core/noema_surface/command_prompt.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.534`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/noema_surface/command_prompt.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.534 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Local NOEMA Surface command-prompt layer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NoemaSurfaceResult, NoemaSurface
- **funkcje:** `to_dict`, `path`, `command_registry`, `global_gadget_registry_path`, `install_global_gadget`, `list_global_gadgets`, `audit_global_gadgets`, `canonize_local_sot_agent`, `install_local_sot_access_standard`, `verify_local_sot_access_standard`, `check_write_permission`, `discover_local_sot_agent`, `verify_local_sot_agent`, `ls`, `read_text`, `write_text`, `read_json`, `write_json`, `sha256_file`, `zip_paths`, `zip_test`, `compileall`, `ast_imports`, `assert_router_boundary`, `run_pytest`, `is_excluded`

## Opis
Local NOEMA Surface command-prompt layer.

This is a local execution surface. It is not NOEMA SoT, not packet ACK,
not memory writeback, and not CURRENT update.
