# htri_bench.py — scripts/htri_bench.py

## Tożsamość
- **id_karty:** `REPO-HTRI_BENCH-650A`
- **ścieżka:** `scripts/htri_bench.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.740`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/htri_bench.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.740 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
HTRI Benchmark — porównanie inference z n_threads=4 (baseline) vs HTRI-optimal.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_post`, `_reset`, `run_round`, `stats`, `main`

## Opis
HTRI Benchmark — porównanie inference z n_threads=4 (baseline) vs HTRI-optimal.

Metodologia:
  Runda A: POST /api/chat/message, n_threads=4 (hardcoded baseline)
  Runda B: POST /api/chat/message, n_threads=htri_optimal (z Kuramoto)

Mierzy: czas odpowiedzi (ms), długość odpowiedzi (chars), chars/ms.
Wynik: tabela A vs B z avg ± std.

Wymagania: serwis ciel-gui aktywny (port 2435), model załadowan
