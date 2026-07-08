# galois_resolvents.py — .python_packages/sympy/polys/numberfields/galois_resolvents.py

## Tożsamość
- **id_karty:** `REPO-GALOIS_RESOLVENTS-1177`
- **ścieżka:** `.python_packages/sympy/polys/numberfields/galois_resolvents.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.394`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/numberfields/galois_resolvents.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.394 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Galois resolvents

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GaloisGroupException, ResolventException, Resolvent
- **funkcje:** `wrap`, `s_vars`, `sparse_symmetrize_resolvent_coeffs`, `define_resolvents`, `generate_lambda_lookup`, `get_resolvent_by_lookup`, `get_prec`, `approximate_roots_of_poly`, `round_mpf`, `round_roots_to_integers_for_poly`, `eval_for_poly`

## Opis
Galois resolvents

Each of the functions in ``sympy.polys.numberfields.galoisgroups`` that
computes Galois groups for a particular degree $n$ uses resolvents. Given the
polynomial $T$ whose Galois group is to be computed, a resolvent is a
polynomial $R$ whose roots are defined as functions of the roots of $T$.

One way to compute the coefficients of $R$ is by approximating the roots of $T$
to suff
