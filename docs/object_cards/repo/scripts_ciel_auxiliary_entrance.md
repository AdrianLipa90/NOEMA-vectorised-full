# ciel_auxiliary_entrance.py — scripts/ciel_auxiliary_entrance.py

## Tożsamość
- **id_karty:** `REPO-CIEL_AUXILIARY_ENTRA-397F`
- **ścieżka:** `scripts/ciel_auxiliary_entrance.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.228`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_auxiliary_entrance.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.228 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
Auxiliary entrance for the triad pipeline.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_append_jsonl`, `_extract_message`, `_read_cielingo_message`, `_normalize_phase`, `_surface_oscillators_12d`, `_wave_vector_from_phi`, `_phase_index`, `_format_hit`, `_render_phase_block`, `_render_eeg_block`, `build_auxiliary_hook_output`, `main`

## Opis
Auxiliary entrance for the triad pipeline.

Builds one compact bridge:
  PhaseNav text phase -> HTRI/EEG-style oscillator snapshot -> subconscious bridge -> CIELingo premodel context.

The entrypoint is intentionally auxiliary: it writes a snapshot to /dev/shm/ciel_noema
and returns OpenCode hook JSON, but it does not replace the main pipeline.
