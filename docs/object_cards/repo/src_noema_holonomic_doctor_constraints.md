# constraints.py — src/noema_holonomic_doctor/constraints.py

## Tożsamość
- **id_karty:** `REPO-CONSTRAINTS-0692`
- **ścieżka:** `src/noema_holonomic_doctor/constraints.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.658`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/noema_holonomic_doctor/constraints.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.658 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Constraint definitions for the NOEMA Holonomic Doctor.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DoctorConstraint
- **funkcje:** —

## Opis
Constraint definitions for the NOEMA Holonomic Doctor.

The constants here are not physical claims.  They are code-health analogues:

* ``D_lambda`` tracks slow global manifest drift between diagnostic cycles.
* ``epsilon_neutrino`` is the small local tolerance used when comparing
  phase-like closure scores across diagnostic flavours.

Values are derived from machine precision / observed manifest
