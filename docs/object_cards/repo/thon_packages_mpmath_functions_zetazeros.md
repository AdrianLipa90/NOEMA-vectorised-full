# zetazeros.py — .python_packages/mpmath/functions/zetazeros.py

## Tożsamość
- **id_karty:** `REPO-ZETAZEROS-426D`
- **ścieżka:** `.python_packages/mpmath/functions/zetazeros.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.892`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpmath/functions/zetazeros.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.892 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
The function zetazero(n) computes the n-th nontrivial zero of zeta(s).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `find_rosser_block_zero`, `wpzeros`, `separate_zeros_in_block`, `separate_my_zero`, `sure_number_block`, `compute_triple_tvb`, `search_supergood_block`, `count_variations`, `pattern_construct`, `zetazero`, `gram_index`, `count_to`, `comp_fp_tolerance`, `nzeros`, `backlunds`

## Opis
The function zetazero(n) computes the n-th nontrivial zero of zeta(s).

The general strategy is to locate a block of Gram intervals B where we
know exactly the number of zeros contained and which of those zeros
is that which we search.

If n <= 400 000 000  we know exactly the Rosser exceptions, contained
in a list in this file. Hence for n<=400 000 000 we simply
look at these list of exceptions.
