# _polyutils.py — .python_packages/scipy/signal/_polyutils.py

## Tożsamość
- **id_karty:** `REPO-_POLYUTILS-7217`
- **ścieżka:** `.python_packages/scipy/signal/_polyutils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.776`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/signal/_polyutils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.776 |
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
Partial replacements for numpy polynomial routines, with Array API compatibility.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_sort_cmplx`, `polyroots`, `_trim_zeros`, `_lstsq`, `_poly1d`, `polyval`, `poly`, `polymul`, `polyfit`, `npp_polyval`, `npp_polyvalfromroots`

## Opis
Partial replacements for numpy polynomial routines, with Array API compatibility.

This module contains both "old-style", np.poly1d, routines from the main numpy
namespace, and "new-style", np.polynomial.polynomial, routines.

To distinguish the two sets, the "new-style" routine names start with `npp_`
