# llvm_bindings.py — .python_packages/numba/core/llvm_bindings.py

## Tożsamość
- **id_karty:** `REPO-LLVM_BINDINGS-3AD9`
- **ścieżka:** `.python_packages/numba/core/llvm_bindings.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.112`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/llvm_bindings.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.112 |
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
Useful options to debug LLVM passes

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_inlining_threshold`, `create_pass_builder`

## Opis
Useful options to debug LLVM passes

llvm.set_option("test", "-debug-pass=Details")
llvm.set_option("test", "-debug-pass=Executions")
llvm.set_option("test", "-debug-pass=Arguments")
llvm.set_option("test", "-debug-pass=Structure")
llvm.set_option("test", "-debug-only=loop-vectorize")
llvm.set_option("test", "-help-hidden")
