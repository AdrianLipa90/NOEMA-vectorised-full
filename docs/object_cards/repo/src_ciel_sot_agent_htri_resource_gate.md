# htri_resource_gate.py — src/ciel_sot_agent/htri_resource_gate.py

## Tożsamość
- **id_karty:** `REPO-HTRI_RESOURCE_GATE-7D6C`
- **ścieżka:** `src/ciel_sot_agent/htri_resource_gate.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.163`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/htri_resource_gate.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.163 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


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
