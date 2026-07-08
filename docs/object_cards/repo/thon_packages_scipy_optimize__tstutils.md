# _tstutils.py — .python_packages/scipy/optimize/_tstutils.py

## Tożsamość
- **id_karty:** `REPO-_TSTUTILS-E021`
- **ścieżka:** `.python_packages/scipy/optimize/_tstutils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.349`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_tstutils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.349 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Parameters used in test and benchmark methods.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `f1`, `f1_fp`, `f1_fpp`, `f2`, `f2_fp`, `f2_fpp`, `f3`, `f3_fp`, `f3_fpp`, `f4`, `f5`, `f6`, `aps01_f`, `aps01_fp`, `aps01_fpp`, `aps02_f`, `aps02_fp`, `aps02_fpp`, `aps03_f`, `aps03_fp`, `aps03_fpp`, `aps04_f`, `aps04_fp`, `aps04_fpp`, `aps05_f`, `aps05_fp`, `aps05_fpp`, `aps06_f`, `aps06_fp`, `aps06_fpp`

## Opis
Parameters used in test and benchmark methods.

Collections of test cases suitable for testing 1-D root-finders
  'original': The original benchmarking functions.
     Real-valued functions of real-valued inputs on an interval
     with a zero.
     f1, .., f3 are continuous and infinitely differentiable
     f4 has a left- and right- discontinuity at the root
     f5 has a root at 1 replacing a 1
