# triadic_output_vector.py — src/cielingo/triadic_output_vector.py

## Tożsamość
- **id_karty:** `REPO-TRIADIC_OUTPUT_VECTO-8B71`
- **ścieżka:** `src/cielingo/triadic_output_vector.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.317`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/triadic_output_vector.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.317 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
CIELingo triadic output vectorization.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TriadicOutputVector, OnVivoOutputTestReport
- **funkcje:** `_bounded`, `_round`, `_mean_vectors`, `_digest_payload`, `_phase_alignment_to_bus`, `_cards_for_phase_report`, `_comprehension_lane`, `_expression_lane`, `vectorize_triadic_output`, `on_vivo_output_test`, `write_output_test_report`, `as_dict`, `as_dict`

## Opis
CIELingo triadic output vectorization.

The output triad turns parsed phase sense into a runtime-ready 3-lane vector:

1. comprehension lane: word-to-phase understanding and confidence;
2. inference lane: shared CIELingo vector/HTRI/J/CQCL transport;
3. expression lane: output readiness through tensor-scalar resistance/thinning.

Each lane is 24D to remain compatible with the CIELingo vector surfa
