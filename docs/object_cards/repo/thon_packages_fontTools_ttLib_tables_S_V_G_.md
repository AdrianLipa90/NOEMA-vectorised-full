# S_V_G_.py — .python_packages/fontTools/ttLib/tables/S_V_G_.py

## Tożsamość
- **id_karty:** `REPO-S_V_G_-6E36`
- **ścieżka:** `.python_packages/fontTools/ttLib/tables/S_V_G_.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.128`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/ttLib/tables/S_V_G_.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.128 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
Compiles/decompiles SVG table.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** table_S_V_G_, DocumentIndexEntry, SVGDocument
- **funkcje:** `decompile`, `compile`, `toXML`, `fromXML`

## Opis
Compiles/decompiles SVG table.

https://docs.microsoft.com/en-us/typography/opentype/spec/svg

The XML format is:

.. code-block:: xml

        <SVG>
                <svgDoc endGlyphID="1" startGlyphID="1">
                        <![CDATA[ <complete SVG doc> ]]
                </svgDoc>
        ...
                <svgDoc endGlyphID="n" startGlyphID="m">
                        <![CDATA[ <complet
