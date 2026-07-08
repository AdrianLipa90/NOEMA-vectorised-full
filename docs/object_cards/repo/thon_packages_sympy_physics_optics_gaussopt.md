# gaussopt.py — .python_packages/sympy/physics/optics/gaussopt.py

## Tożsamość
- **id_karty:** `REPO-GAUSSOPT-AC0A`
- **ścieżka:** `.python_packages/sympy/physics/optics/gaussopt.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.071`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/optics/gaussopt.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.071 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Gaussian optics.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RayTransferMatrix, FreeSpace, FlatRefraction, CurvedRefraction, FlatMirror, CurvedMirror, ThinLens, GeometricRay, BeamParameter
- **funkcje:** `waist2rayleigh`, `rayleigh2waist`, `geometric_conj_ab`, `geometric_conj_af`, `gaussian_conj`, `conjugate_gauss_beams`, `A`, `B`, `C`, `D`, `height`, `angle`, `wavelen`, `z`, `z_r`, `n`, `q`, `radius`, `w`, `w_0`, `divergence`, `gouy`, `waist_approximation_limit`

## Opis
Gaussian optics.

The module implements:

- Ray transfer matrices for geometrical and gaussian optics.

  See RayTransferMatrix, GeometricRay and BeamParameter

- Conjugation relations for geometrical and gaussian optics.

  See geometric_conj*, gauss_conj and conjugate_gauss_beams

The conventions for the distances are as follows:

focal distance
    positive for convergent lenses
object distance
