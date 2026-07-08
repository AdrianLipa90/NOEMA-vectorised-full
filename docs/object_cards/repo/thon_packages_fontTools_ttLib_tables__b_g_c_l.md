# _b_g_c_l.py — .python_packages/fontTools/ttLib/tables/_b_g_c_l.py

## Tożsamość
- **id_karty:** `REPO-_B_G_C_L-9819`
- **ścieżka:** `.python_packages/fontTools/ttLib/tables/_b_g_c_l.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.895`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/ttLib/tables/_b_g_c_l.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.895 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
Support for the `bgcl` (Apple Color Emoji background) table.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** table__b_g_c_l
- **funkcje:** `decompile`, `compile`, `toXML`, `fromXML`

## Opis
Support for the `bgcl` (Apple Color Emoji background) table.

This table stores a JSON blob. We decode it to a Python object on
decompile and emit human readable JSON in the TTX via a <json> element.
On compile we re-encode the JSON to UTF-8 bytes which is what Apple code
reads via CTFontCopyTable then JSONDecoder.

On iOS 16 and later the `bgcl` payload is used as the wallpaper
background when th
