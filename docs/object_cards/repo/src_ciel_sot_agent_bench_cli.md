# bench_cli.py — src/ciel_sot_agent/bench_cli.py

## Tożsamość
- **id_karty:** `REPO-BENCH_CLI-F889`
- **ścieżka:** `src/ciel_sot_agent/bench_cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.282`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/bench_cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.282 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


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
