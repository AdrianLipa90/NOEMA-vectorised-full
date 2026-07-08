# noema_proc_watch_daemon.py — scripts/noema_proc_watch_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_PROC_WATCH_DAE-5AB3`
- **ścieżka:** `scripts/noema_proc_watch_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.759`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_proc_watch_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.759 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Proc watch daemon — inotify-like /proc change detector.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `log`, `_init_dirs`, `_read_proc_stats`, `_scan`, `_write_surface`, `signal_handler`, `main`

## Opis
Proc watch daemon — inotify-like /proc change detector.

Monitoruje narodziny i śmierci procesów przez skanowanie /proc/[pid]/stat,
detekcję nowych PIDs, i raportowanie na surface.

Zamiast inotify (wymaga ctypes/bindings), używa szybkiego pollingu
przez os.listdir("/proc") + diff z poprzednim stanem.

Surface output (/dev/shm/ciel_noema/proc_watch/):
  new_pids.jsonl  — ostatnie 64 narodzin (PID,
