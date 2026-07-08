# neutrinotime14_fixed.py — src/ciel-omega-demo-main/docs/Studies/Metatime-main/neutrinotime14_fixed.py

## Tożsamość
- **id_karty:** `REPO-NEUTRINOTIME14_FIXED-B13E`
- **ścieżka:** `src/ciel-omega-demo-main/docs/Studies/Metatime-main/neutrinotime14_fixed.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.167`
- **masa_semantyczna:** `0.60`

## Kotwice
- `src/ciel-omega-demo-main/docs/Studies/Metatime-main/neutrinotime14_fixed.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.167 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.60 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `ciel_omega_core`.

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
Neutrinotime14 — poprawiona symulacja CP naruszenia

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** —
- **funkcje:** `build_pmns`, `berry_phase_approx`, `P_alpha_beta`, `build_trajectory`

## Opis
Neutrinotime14 — poprawiona symulacja CP naruszenia
====================================================
Naprawa Bug #1 (krytyczny): P_alpha_beta stosował globalną fazę Berry'ego
jako skalar np.exp(1j*gamma), który kasuje się w |·|² → ΔP_CP = 0.

FIX: Faza Berry'ego wchodzi WEWNĄTRZ macierzy fazowej, różnicowo
dla każdego eigenstanu masy, z wagami τᵢ z Metatime (Collatz):
  τ = [0.02, 0.05, 0.10]
