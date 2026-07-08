# kuramoto_sym.py — scripts/kuramoto_sym.py

## Tożsamość
- **id_karty:** `REPO-KURAMOTO_SYM-2939`
- **ścieżka:** `scripts/kuramoto_sym.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.064`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/kuramoto_sym.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.064 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Kuramoto 24-oscillator simulation — CIEL experiment tracker.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _NumpyEncoder
- **funkcje:** `intrinsic_frequencies`, `run_kuramoto`, `experiment_id`, `ensure_dirs`, `save_experiment`, `plot_results`, `sweep_kappa`, `main`, `default`

## Opis
Kuramoto 24-oscillator simulation — CIEL experiment tracker.

Usage:
    python3 scripts/kuramoto_sym.py                    # default: sweep kappa
    python3 scripts/kuramoto_sym.py --mode sweep       # sweep kappa from 0.0 to 2.0
    python3 scripts/kuramoto_sym.py --mode single      # single run with given kappa
    python3 scripts/kuramoto_sym.py --kappa 1.5        # single run at kappa=1.5
