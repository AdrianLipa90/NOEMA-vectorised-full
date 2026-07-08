# transform.py — .python_packages/fontTools/misc/transform.py

## Tożsamość
- **id_karty:** `REPO-TRANSFORM-68B0`
- **ścieżka:** `.python_packages/fontTools/misc/transform.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.412`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/misc/transform.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.412 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
Affine 2D transformation matrix class.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Transform, DecomposedTransform
- **funkcje:** `_normSinCos`, `Offset`, `Scale`, `transformPoint`, `transformPoints`, `transformVector`, `transformVectors`, `translate`, `scale`, `rotate`, `skew`, `transform`, `reverseTransform`, `inverse`, `toPS`, `toDecomposed`, `fromTransform`, `toTransform`

## Opis
Affine 2D transformation matrix class.

The Transform class implements various transformation matrix operations,
both on the matrix itself, as well as on 2D coordinates.

Transform instances are effectively immutable: all methods that operate on the
transformation itself always return a new instance. This has as the
interesting side effect that Transform instances are hashable, ie. they can be
use
