# __init__.py — build/lib/ciel_geometry/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-A437`
- **ścieżka:** `build/lib/ciel_geometry/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.725`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.725 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
ciel_geometry — Poincaré disk geometry engine for CIEL orbital system.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
ciel_geometry — Poincaré disk geometry engine for CIEL orbital system.

Exports are loaded lazily so module CLIs like
``python -m ciel_geometry.noema_surface_mmap`` do not trigger duplicate-import
warnings via eager package side effects.
