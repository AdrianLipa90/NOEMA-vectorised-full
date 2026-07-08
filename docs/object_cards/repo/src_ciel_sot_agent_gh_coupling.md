# gh_coupling.py — src/ciel_sot_agent/gh_coupling.py

## Tożsamość
- **id_karty:** `REPO-GH_COUPLING-1DB1`
- **ścieżka:** `src/ciel_sot_agent/gh_coupling.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.362`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/gh_coupling.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.362 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
GitHub coupling subsystem (v1) — live upstream-aware phase coupling.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `build_live_coupling`, `main`

## Opis
GitHub coupling subsystem (v1) — live upstream-aware phase coupling.

Fetches current upstream HEAD SHAs for registered repositories, propagates
phase shifts through the coupling map, and emits a refreshed JSON coupling
report.  Invoked via the ``ciel-sot-gh-coupling`` console script.
