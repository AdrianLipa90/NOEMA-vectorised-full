# bench_cli.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/bench_cli.py

## Tożsamość
- **id_karty:** `REPO-BENCH_CLI-6980`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/bench_cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.822`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/bench_cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.822 |
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
ciel-sot-bench — benchmark runner dla komponentów CIEL.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_project_root`, `_run_bench`, `_bench_orbital_bridge`, `_bench_global_pass`, `_bench_pipeline`, `main`

## Opis
ciel-sot-bench — benchmark runner dla komponentów CIEL.

Komendy:
  orbital-bridge [--runs N] [--profile]   mierzy build_orbital_bridge()
  global-pass    [--runs N] [--profile]   mierzy run_global_pass()
  pipeline       [--runs N] [--profile]   mierzy run_ciel_pipeline()
