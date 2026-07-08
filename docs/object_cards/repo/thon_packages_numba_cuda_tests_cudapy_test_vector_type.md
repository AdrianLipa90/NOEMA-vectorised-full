# test_vector_type.py — .python_packages/numba/cuda/tests/cudapy/test_vector_type.py

## Tożsamość
- **id_karty:** `REPO-TEST_VECTOR_TYPE-459A`
- **ścieżka:** `.python_packages/numba/cuda/tests/cudapy/test_vector_type.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.653`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/tests/cudapy/test_vector_type.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.653 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
CUDA vector type tests. Note that this test file imports

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestCudaVectorType
- **funkcje:** `make_kernel`, `make_fancy_creation_kernel`, `kernel_1elem`, `kernel_2elem`, `kernel_3elem`, `kernel_4elem`, `kernel`, `test_basic`, `test_creation_readout`, `test_fancy_creation_readout`, `test_vector_type_alias`, `kernel`

## Opis
CUDA vector type tests. Note that this test file imports
`cuda.vector_type` module to programmatically test all the
vector types. However, `vector_type` module is internal
and should not be imported by user, user should only import the
corresponding vector type from `cuda` module in kernel to use them.
