# noema_surface_mmap.py — build/bdist.linux-x86_64/wheel/ciel_geometry/noema_surface_mmap.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SURFACE_MMAP-6791`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_surface_mmap.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.373`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_surface_mmap.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.373 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
NOEMA shared surface backed by ``numpy.memmap`` files.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SurfaceArraySpec
- **funkcje:** `_compute_j_kj`, `surface_specs`, `oscillator_id_for_concept`, `_channel_idx`, `_osc_rho`, `oscillator_disk_pos`, `wij_bipolar_axis`, `compute_surface_bipolar_axes`, `surface_bipolar_snapshot`, `_pmns_squared`, `seed_neutrino_mixing`, `neutrino_oscillation_probability`, `compute_neutrino_channel`, `surface_neutrino_diagnostic`, `_init_htri_batch`, `_core_osc_omega`, `init_htri_batch_system`, `evolve_htri_batch_system`, `feed_htri_to_surface`, `evolve_and_feed_htri`, `initialize_coupling_from_memory_channels`, `update_coupling_from_concepts`, `update_coupling_hebbian`, `update_coupling_weight`, `evolve_surface`, `read_surface_state`, `_surface_path`, `ensure_surface`, `open_surface`, `initialize_surface`

## Opis
NOEMA shared surface backed by ``numpy.memmap`` files.
Autorzy: Adrian Lipa & NOEMA (2026)

The surface lives by default under ``/dev/shm/ciel_noema`` so multiple local
processes can share oscillator state without JSON or CSV hand-off.

Architecture (NOEMA as SOT, W_ij as central coupling):
  phi       — 24 oscillator phases: evolve via Kuramoto dphi/dt = omega + sum(g * sin(delta_phi))
  omega
