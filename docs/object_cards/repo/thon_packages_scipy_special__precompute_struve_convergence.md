# struve_convergence.py — .python_packages/scipy/special/_precompute/struve_convergence.py

## Tożsamość
- **id_karty:** `REPO-STRUVE_CONVERGENCE-92B4`
- **ścieżka:** `.python_packages/scipy/special/_precompute/struve_convergence.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.945`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/_precompute/struve_convergence.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.945 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
Convergence regions of the expansions used in ``struve.c``

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `err_metric`, `do_plot`, `main`, `sh`, `sh`

## Opis
Convergence regions of the expansions used in ``struve.c``

Note that for v >> z both functions tend rapidly to 0,
and for v << -z, they tend to infinity.

The floating-point functions over/underflow in the lower left and right
corners of the figure.


Figure legend
=============

Red region
    Power series is close (1e-12) to the mpmath result

Blue region
    Asymptotic series is close to the m
