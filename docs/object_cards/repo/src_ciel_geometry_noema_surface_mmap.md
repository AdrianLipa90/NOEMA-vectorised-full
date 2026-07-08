# noema_surface_mmap.py — src/ciel_geometry/noema_surface_mmap.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SURFACE_MMAP-6558`
- **ścieżka:** `src/ciel_geometry/noema_surface_mmap.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `1.597`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/noema_surface_mmap.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 1.597 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

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
NOEMA shared surface backed by ``numpy.memmap`` files.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** SurfaceArraySpec
- **funkcje:** `_compute_j_kj`, `surface_specs`, `oscillator_id_for_concept`, `_channel_idx`, `_osc_rho`, `oscillator_disk_pos`, `wij_bipolar_axis`, `compute_surface_bipolar_axes`, `surface_bipolar_snapshot`, `_pmns_squared`, `seed_neutrino_mixing`, `neutrino_oscillation_probability`, `compute_neutrino_channel`, `surface_neutrino_diagnostic`, `_init_htri_batch`, `_core_osc_omega`, `init_htri_batch_system`, `evolve_htri_batch_system`, `feed_htri_to_surface`, `evolve_and_feed_htri`, `initialize_coupling_from_memory_channels`, `update_coupling_from_concepts`, `update_coupling_hebbian`, `update_coupling_weight`, `evolve_surface`, `read_surface_state`, `read_ciel_internal_state`, `_surface_path`, `ensure_surface`, `open_surface`

## Opis
NOEMA shared surface backed by ``numpy.memmap`` files.
Autorzy: Adrian Lipa & NOEMA (2026)

The surface lives by default under ``/dev/shm/ciel_noema`` so multiple local
processes can share oscillator state without JSON or CSV hand-off.

Architecture (NOEMA as SOT, W_ij as central coupling):
  phi       — 36 oscillator phases: evolve via Kuramoto dphi/dt = omega + sum(g * sin(delta_phi))
  omega
