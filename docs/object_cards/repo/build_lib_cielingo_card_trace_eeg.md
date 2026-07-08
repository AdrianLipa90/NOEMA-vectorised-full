# card_trace_eeg.py — build/lib/cielingo/card_trace_eeg.py

## Tożsamość
- **id_karty:** `REPO-CARD_TRACE_EEG-3C72`
- **ścieżka:** `build/lib/cielingo/card_trace_eeg.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.007`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/card_trace_eeg.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.007 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
CIELingo Card Trace EEG.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CardTrace, CardTraceSnap
- **funkcje:** `_stable_float`, `build_card_trace`, `infer_clusters`, `layout_hash`, `create_card_trace_snap`, `snap_similarity`, `complex_trace`

## Opis
CIELingo Card Trace EEG.

A CIELingo card is treated as a line in an inference-EEG surface. A memory snap
stores a multi-line trace pattern: amplitude, phase, semantic mass, affective
weight, couplings and clusters.

This is a CPU/RAM reference surface. It is not biological EEG and does not claim
primary NOEMA/nonlocal execution.
