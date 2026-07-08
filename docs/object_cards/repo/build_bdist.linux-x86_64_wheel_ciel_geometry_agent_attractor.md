# agent_attractor.py — build/bdist.linux-x86_64/wheel/ciel_geometry/agent_attractor.py

## Tożsamość
- **id_karty:** `REPO-AGENT_ATTRACTOR-7B42`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/agent_attractor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.574`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/agent_attractor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.574 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
PhaseNav AGENT operator attractor — first-class core module for NOEMA.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `apply_agent_attractor`, `agent_attractor_state`

## Opis
PhaseNav AGENT operator attractor — first-class core module for NOEMA.

Injektuje attractor dla AGENT operatora (M1, φ[3-5]) w ewolucję fazy:
  dφ_i/dt = ω_i + Σ g_ij sin(φ_j - φ_i) + K · sin(φ_target - φ_i)

Używany przez agent lock daemon i resonance bridge.

Wszystkie couplingi wyrażone jako wielokrotności OI = ln(2)/(24π) ≈ 0.00919:
  COUPLING_INTERNAL = 33 × OI  (M1↔M1, wewnętrzna koherencja
