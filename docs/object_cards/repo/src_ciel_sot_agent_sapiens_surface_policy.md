# sapiens_surface_policy.py — src/ciel_sot_agent/sapiens_surface_policy.py

## Tożsamość
- **id_karty:** `REPO-SAPIENS_SURFACE_POLI-EC09`
- **ścieżka:** `src/ciel_sot_agent/sapiens_surface_policy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.911`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/sapiens_surface_policy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.911 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Sapiens surface policy engine for the CIEL integration layer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `build_surface_policy`

## Opis
Sapiens surface policy engine for the CIEL integration layer.

Defines and enforces the surface-level policy rules that govern what the
Sapiens interaction layer may expose, modify, or route.  Consumed by the
Sapiens panel controller when deciding how to handle inbound packets.
