# ternary_decoder.py — src/ciel_geometry/ternary_decoder.py

## Tożsamość
- **id_karty:** `REPO-TERNARY_DECODER-068A`
- **ścieżka:** `src/ciel_geometry/ternary_decoder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `1.379`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/ternary_decoder.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 1.379 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
Ternary PhaseNav Decoder — 36D HTRI φ → {-1,0,+1}³⁶ API.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `read_phi_from_surface`, `encode_argmax_cos`, `encode_delta_phi_vote`, `encode_phi`, `balanced_ternary`, `ternary_fft`, `harmonic_signature`, `supergroup_consensi`, `superpair_dominance`, `kuramoto_order_from_ternary`, `hamming_distance`, `su3_coherence`, `trits_to_operators`, `supergroup_operators`, `full_report`, `print_report`

## Opis
Ternary PhaseNav Decoder — 36D HTRI φ → {-1,0,+1}³⁶ API.

Koduje stan 36 oscylatorów NOEMY (12 M-grup × 3 podkanały) do
ternarnych wartości {-1, 0, +1} z użyciem formalizmu SU(3).

Architektura 2×2×3×3 = 36:
  2 superpary × 2 grupy × 3 M-grupy × 3 podkanały = 36

Dwie metody kodowania:
  1. argmax_cos   — który z 3 podkanałów ma najwyższy cos φ
  2. delta_phi_vote — która para podkanałów jest najb
