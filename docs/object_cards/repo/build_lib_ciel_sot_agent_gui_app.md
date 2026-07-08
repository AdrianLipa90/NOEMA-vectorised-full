# app.py — build/lib/ciel_sot_agent/gui/app.py

## Tożsamość
- **id_karty:** `REPO-APP-E721`
- **ścieżka:** `build/lib/ciel_sot_agent/gui/app.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.176`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/gui/app.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.176 |
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
Flask application factory and entry-point for the CIEL Quiet Orbital Control GUI.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `create_app`, `main`

## Opis
Flask application factory and entry-point for the CIEL Quiet Orbital Control GUI.

The GUI is intentionally a *consumer* of prepared state — it reads manifests,
reports, and session files written by backend modules rather than performing
heavy computation itself.  This follows the "GUI consumes state; GUI does not
impersonate runtime" principle from the CIEL GUI Identity Brief.

Entry-point usage:
