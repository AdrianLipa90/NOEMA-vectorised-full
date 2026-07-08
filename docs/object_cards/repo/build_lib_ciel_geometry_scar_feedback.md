# scar_feedback.py — build/lib/ciel_geometry/scar_feedback.py

## Tożsamość
- **id_karty:** `REPO-SCAR_FEEDBACK-54B5`
- **ścieżka:** `build/lib/ciel_geometry/scar_feedback.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.286`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/scar_feedback.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.286 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
SemanticScar → surface feedback loop — autonomiczny układ nerwowy NOEMY.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `compute_scar_feedback`, `apply_scar_feedback`

## Opis
SemanticScar → surface feedback loop — autonomiczny układ nerwowy NOEMY.

Czyta rzeczywiste wskaźniki blizn semantycznych z CIELingo (gravity[4-7])
i moduluje stan powierzchni NOEMA (phi, omega, flavor, g) w trzech warstwach:

  1. ω per-channel — semantic (M3) zwalnia bardziej niż percept (M0)
  2. φ divergence   — M3 rozjeżdża się przy niepewności, zbiega przy konsensusie
  3. g tightening   — M
