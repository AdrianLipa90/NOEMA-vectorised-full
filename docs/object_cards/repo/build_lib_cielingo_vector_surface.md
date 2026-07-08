# vector_surface.py — build/lib/cielingo/vector_surface.py

## Tożsamość
- **id_karty:** `REPO-VECTOR_SURFACE-56CA`
- **ścieżka:** `build/lib/cielingo/vector_surface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.305`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/vector_surface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.305 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
CIELingo vector surface for CQCL, HTRI, NOEMA and OrchORbital.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CIELingoVector, VectorSurfaceReport
- **funkcje:** `_bounded`, `_stable_unit`, `_round_vector`, `_digest_payload`, `vector_from_phase_bus_node`, `vectorize_card`, `select_vector_cards`, `vector_surface_report`, `write_vector_report`, `as_dict`, `as_dict`

## Opis
CIELingo vector surface for CQCL, HTRI, NOEMA and OrchORbital.

The vector is a compatibility surface, not a replacement for CIELingo cards.
It converts the existing LNS/NOEMA language-card phase bus into a fixed
24-component vector so downstream layers can consume a stable numerical
contract:

* CQCL receives normalized quantum-variable compatible fields.
* HTRI receives oscillator id, phase, ang
