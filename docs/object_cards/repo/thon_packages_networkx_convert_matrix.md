# convert_matrix.py — .python_packages/networkx/convert_matrix.py

## Tożsamość
- **id_karty:** `REPO-CONVERT_MATRIX-55C7`
- **ścieżka:** `.python_packages/networkx/convert_matrix.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.809`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/convert_matrix.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.809 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
Functions to convert NetworkX graphs to and from common data containers

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `to_pandas_adjacency`, `from_pandas_adjacency`, `to_pandas_edgelist`, `from_pandas_edgelist`, `to_scipy_sparse_array`, `_csr_gen_triples`, `_csc_gen_triples`, `_coo_gen_triples`, `_dok_gen_triples`, `_generate_weighted_edges`, `from_scipy_sparse_array`, `to_numpy_array`, `from_numpy_array`

## Opis
Functions to convert NetworkX graphs to and from common data containers
like numpy arrays, scipy sparse arrays, and pandas DataFrames.

The preferred way of converting data to a NetworkX graph is through the
graph constructor.  The constructor calls the `~networkx.convert.to_networkx_graph`
function which attempts to guess the input type and convert it automatically.

Examples
--------
Create a 10
