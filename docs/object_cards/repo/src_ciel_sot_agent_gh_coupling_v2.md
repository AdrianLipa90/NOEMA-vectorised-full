# gh_coupling_v2.py — src/ciel_sot_agent/gh_coupling_v2.py

## Tożsamość
- **id_karty:** `REPO-GH_COUPLING_V2-FA51`
- **ścieżka:** `src/ciel_sot_agent/gh_coupling_v2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.444`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/gh_coupling_v2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.444 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


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
