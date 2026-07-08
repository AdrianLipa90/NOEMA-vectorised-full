# _linprog_ip.py — .python_packages/scipy/optimize/_linprog_ip.py

## Tożsamość
- **id_karty:** `REPO-_LINPROG_IP-332C`
- **ścieżka:** `.python_packages/scipy/optimize/_linprog_ip.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.012`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_linprog_ip.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.012 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Interior-point method for linear programming

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_get_solver`, `_get_delta`, `_sym_solve`, `_get_step`, `_get_message`, `_do_step`, `_get_blind_start`, `_indicators`, `_display_iter`, `_ip_hsd`, `_linprog_ip`, `r_p`, `r_d`, `r_g`, `mu`, `norm`, `eta`, `eta`, `solve`, `solve`, `solve`, `solve`

## Opis
Interior-point method for linear programming

The *interior-point* method uses the primal-dual path following algorithm
outlined in [1]_. This algorithm supports sparse constraint matrices and
is typically faster than the simplex methods, especially for large, sparse
problems. Note, however, that the solution returned may be slightly less
accurate than those of the simplex methods and will not, in
