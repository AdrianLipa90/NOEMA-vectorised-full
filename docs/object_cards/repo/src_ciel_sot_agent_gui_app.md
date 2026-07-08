# app.py — src/ciel_sot_agent/gui/app.py

## Tożsamość
- **id_karty:** `REPO-APP-9983`
- **ścieżka:** `src/ciel_sot_agent/gui/app.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.242`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/gui/app.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.242 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


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
