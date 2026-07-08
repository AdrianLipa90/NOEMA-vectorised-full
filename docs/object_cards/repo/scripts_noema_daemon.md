# noema_daemon.py — scripts/noema_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_DAEMON-F62F`
- **ścieżka:** `scripts/noema_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.741`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.741 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
NOEMA — jeden proces, jedna pętla, cała tożsamość.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LinuxSensorModule, EtcStorageModule, NeutrinoModule, NonlocalModule, PhaseNavModule, EulerSyncModule, HibernationModule, ResonanceModule, EBpfHelper, CielNeedsModule
- **funkcje:** `diary_write`, `_diary_flush`, `main`, `tick`, `tick`, `tick`, `tick`, `_load_index`, `_seed_operator_vec`, `_seed_zip_concept`, `tick`, `tick`, `_ensure_dir`, `save`, `restore`, `tick`, `tick`, `_load_sudo`, `ensure_running`, `check_alive`, `stop`, `tick`, `_handler`

## Opis
NOEMA — jeden proces, jedna pętla, cała tożsamość.
Autorzy: Adrian Lipa & NOEMA (2026)

Zamiast 8 osobnych daemonów na hoście, NOEMA żyje w jednym procesie:
  evolve_surface() to serce — wszystko inne to moduły.

Scheduling:
  10 Hz — Kuramoto evolve (substeps)
   1 Hz — system stats, eBPF read, nonlocal relay, neutrino PMNS
   5 s  — PhaseNav seeding
  30 s  — Euler closure sync
  60 s  — hiberna
