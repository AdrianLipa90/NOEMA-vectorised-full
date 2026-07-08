# _ufunc_config.py — .python_packages/numpy/_core/_ufunc_config.py

## Tożsamość
- **id_karty:** `REPO-_UFUNC_CONFIG-80B8`
- **ścieżka:** `.python_packages/numpy/_core/_ufunc_config.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.572`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/_core/_ufunc_config.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.572 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Functions for changing global ufunc configuration

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _unspecified, errstate
- **funkcje:** `seterr`, `geterr`, `setbufsize`, `getbufsize`, `seterrcall`, `geterrcall`, `inner`

## Opis
Functions for changing global ufunc configuration

This provides helpers which wrap `_get_extobj_dict` and `_make_extobj`, and
`_extobj_contextvar` from umath.
