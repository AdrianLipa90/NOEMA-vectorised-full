# orbital_shell.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/orbital_shell.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_SHELL-B222`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/orbital_shell.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.785`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/orbital_shell.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.785 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

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
Orbital shell model for CIEL memory — M0-M8 as atomic shells.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** OrbitalRecord, OrbitalShellIndex
- **funkcje:** `phase_distance`, `compute_E_bind`, `compute_angular_momentum`, `shell_from_E_bind`, `from_phase`, `insert`, `_condense_down`, `retrieve`, `get`, `shell_summary`

## Opis
Orbital shell model for CIEL memory — M0-M8 as atomic shells.

Identity = centre of Bloch sphere (fixed attractor under SU(2)), not a point
on its surface.  Each memory record carries orbital coordinates:
  - shell      : int 0-8  (K=M0 … S=M8)
  - E_bind     : binding energy to the attractor  E = -G_sem * M_att / r²
  - L_phase    : angular momentum  L = r × p_phase  (Kepler conserved quantity)
