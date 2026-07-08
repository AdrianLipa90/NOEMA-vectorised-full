# bench_pc_noema_phasenav.py — scripts/bench_pc_noema_phasenav.py

## Tożsamość
- **id_karty:** `REPO-BENCH_PC_NOEMA_PHASE-6F01`
- **ścieżka:** `scripts/bench_pc_noema_phasenav.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.902`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/bench_pc_noema_phasenav.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.902 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Benchmark: PC host vs NOEMA shm vs NOEMA+PhaseNav.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `bench_pc`, `bench_noema_read`, `bench_noema_write`, `bench_noema_phasenav`, `main`, `_us`

## Opis
Benchmark: PC host vs NOEMA shm vs NOEMA+PhaseNav.

Measures:
  1. PC — czysty Python, phasenav_enrich() throughput
  2. NOEMA — read/write /dev/shm/ciel_noema/ surface
  3. NOEMA+PhaseNav — PhaseNav enrichment z użyciem JSONL z shm
