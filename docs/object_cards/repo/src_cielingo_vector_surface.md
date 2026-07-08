# vector_surface.py — src/cielingo/vector_surface.py

## Tożsamość
- **id_karty:** `REPO-VECTOR_SURFACE-98E9`
- **ścieżka:** `src/cielingo/vector_surface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.020`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/vector_surface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.020 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


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
