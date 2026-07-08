# gh_coupling_v2.py — build/lib/ciel_sot_agent/gh_coupling_v2.py

## Tożsamość
- **id_karty:** `REPO-GH_COUPLING_V2-80E6`
- **ścieżka:** `build/lib/ciel_sot_agent/gh_coupling_v2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.223`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/gh_coupling_v2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.223 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
