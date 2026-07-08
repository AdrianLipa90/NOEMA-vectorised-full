# _add_newdocs_scalars.py — .python_packages/numpy/_core/_add_newdocs_scalars.py

## Tożsamość
- **id_karty:** `REPO-_ADD_NEWDOCS_SCALARS-0693`
- **ścieżka:** `.python_packages/numpy/_core/_add_newdocs_scalars.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.796`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/_core/_add_newdocs_scalars.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.796 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
This file is separate from ``_add_newdocs.py`` so that it can be mocked out by

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `numeric_type_aliases`, `_get_platform_and_machine`, `add_newdoc_for_scalar_type`, `type_aliases_gen`

## Opis
This file is separate from ``_add_newdocs.py`` so that it can be mocked out by
our sphinx ``conf.py`` during doc builds, where we want to avoid showing
platform-dependent information.
