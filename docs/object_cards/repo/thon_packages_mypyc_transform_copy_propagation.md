# copy_propagation.py — .python_packages/mypyc/transform/copy_propagation.py

## Tożsamość
- **id_karty:** `REPO-COPY_PROPAGATION-E537`
- **ścieżka:** `.python_packages/mypyc/transform/copy_propagation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.285`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/transform/copy_propagation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.285 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Simple copy propagation optimization.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CopyPropagationTransform
- **funkcje:** `do_copy_propagation`, `visit_assign`

## Opis
Simple copy propagation optimization.

Example input:

    x = f()
    y = x

The register x is redundant and we can directly assign its value to y:

    y = f()

This can optimize away registers that are assigned to once.
