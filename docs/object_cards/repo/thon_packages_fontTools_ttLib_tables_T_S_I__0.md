# T_S_I__0.py — .python_packages/fontTools/ttLib/tables/T_S_I__0.py

## Tożsamość
- **id_karty:** `REPO-T_S_I__0-E07D`
- **ścieżka:** `.python_packages/fontTools/ttLib/tables/T_S_I__0.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.883`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/ttLib/tables/T_S_I__0.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.883 |
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
TSI{0,1,2,3,5} are private tables used by Microsoft Visual TrueType (VTT)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** table_T_S_I__0
- **funkcje:** `fixlongs`, `decompile`, `compile`, `set`, `toXML`

## Opis
TSI{0,1,2,3,5} are private tables used by Microsoft Visual TrueType (VTT)
tool to store its hinting source data.

TSI0 is the index table containing the lengths and offsets for the glyph
programs and 'extra' programs ('fpgm', 'prep', and 'cvt') that are contained
in the TSI1 table.

See also https://learn.microsoft.com/en-us/typography/tools/vtt/tsi-tables
