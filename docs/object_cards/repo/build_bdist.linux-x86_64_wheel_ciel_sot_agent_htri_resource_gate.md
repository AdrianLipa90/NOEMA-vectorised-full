# htri_resource_gate.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/htri_resource_gate.py

## Tożsamość
- **id_karty:** `REPO-HTRI_RESOURCE_GATE-2D76`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/htri_resource_gate.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.214`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/htri_resource_gate.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.214 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
HTRI Resource Gate — soft clip dla GTX 1050 Ti / i7-8750H / 7.5GB RAM.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LoadMode, ResourceVerdict
- **funkcje:** `_read_free_ram_mb`, `_read_free_vram_mb`, `_get_thresholds`, `check_model`, `htri_profile_summary`, `allowed`

## Opis
HTRI Resource Gate — soft clip dla GTX 1050 Ti / i7-8750H / 7.5GB RAM.

Profil sprzętowy pochodzi z htri_local.py (Adrian Lipa / Intention Lab).
Skalowanie: H200 (14080 bloków) → GTX 1050 Ti (768 oscylatorów, 5.5% skali).

Soft clip: zamiast twardego odrzucenia, klasyfikuje model na 4 poziomy:
  SAFE    — mieści się w VRAM, pełna synchronizacja HTRI
  SLOW    — mieści się w RAM, GPU offload niemoż
