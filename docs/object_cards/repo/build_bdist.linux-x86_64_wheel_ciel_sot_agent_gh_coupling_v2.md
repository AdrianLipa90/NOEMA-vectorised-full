# gh_coupling_v2.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/gh_coupling_v2.py

## Tożsamość
- **id_karty:** `REPO-GH_COUPLING_V2-2874`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/gh_coupling_v2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.605`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/gh_coupling_v2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.605 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
GitHub coupling subsystem (v2) — enhanced upstream coupling with v2 schema.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `resolve_runtime_paths`, `build_live_coupling`, `main`

## Opis
GitHub coupling subsystem (v2) — enhanced upstream coupling with v2 schema.

Extends the v1 GitHub coupling with richer upstream metadata, rate-limit
handling, and a structured v2 coupling report.  Invoked via
``ciel-sot-gh-coupling-v2``.
