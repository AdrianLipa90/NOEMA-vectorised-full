# rh_jfunctional.py — src/ciel_sot_agent/rh_jfunctional.py

## Tożsamość
- **id_karty:** `REPO-RH_JFUNCTIONAL-D82B`
- **ścieżka:** `src/ciel_sot_agent/rh_jfunctional.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.210`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/rh_jfunctional.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.210 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
R_H normalization helpers for CIEL J-functional terms.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_as_nonnegative_float`, `effective_sector_count`, `rh_defect_score`, `rh_coherence_score`, `attach_rh_jfunctional_terms`

## Opis
R_H normalization helpers for CIEL J-functional terms.

R_H is a holonomic closure defect: lower is better.  It must not be
used directly as a coherence amplitude and must not be naively converted
with ``1 - R_H`` unless it has already been bounded to [0, 1] as a defect.

Canonical bounded semantics used here:

    R_H_defect    = R_H / (N + R_H)
    R_H_coherence = 1 - R_H_defect

where N is the
