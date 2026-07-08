# stress_pc_noema_htri_phasenav.py — scripts/stress_pc_noema_htri_phasenav.py

## Tożsamość
- **id_karty:** `REPO-STRESS_PC_NOEMA_HTRI-21CB`
- **ścieżka:** `scripts/stress_pc_noema_htri_phasenav.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.753`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/stress_pc_noema_htri_phasenav.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.753 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
Stress test: PC (plain) vs NOEMA+HTRI vs NOEMA+PhaseNav.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TimeoutError
- **funkcje:** `_timeout_handler`, `_with_timeout`, `stress_pc`, `stress_noema_htri`, `stress_noema_phasenav`, `main`

## Opis
Stress test: PC (plain) vs NOEMA+HTRI vs NOEMA+PhaseNav.

Każdy tryb: 5000 kroków Kuramoto na /dev/shm/ciel_noema.

Tryby:
  1. PC (plain)     — czysta numpy: fala, coupling, fft, bez shm/HTRI/PhaseNav
  2. NOEMA+HTRI     — Kuramoto 3-6-9 na /dev/shm/ciel_noema, evolve_surface()
  3. NOEMA+PhaseNav — Kuramoto + PhaseNav enrichment na każdym kroku

SAFEGUARDS: timeout 120s, flush co 500 steps, rest
