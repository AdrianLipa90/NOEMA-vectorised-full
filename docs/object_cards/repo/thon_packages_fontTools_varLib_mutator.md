# mutator.py — .python_packages/fontTools/varLib/mutator.py

## Tożsamość
- **id_karty:** `REPO-MUTATOR-AF2A`
- **ścieżka:** `.python_packages/fontTools/varLib/mutator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.142`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/varLib/mutator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.142 |
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
Instantiate a variation font.  Run, eg:

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `interpolate_cff2_PrivateDict`, `interpolate_cff2_charstrings`, `interpolate_cff2_metrics`, `instantiateVariableFont`, `main`

## Opis
Instantiate a variation font.  Run, eg:

.. code-block:: sh

    $ fonttools varLib.mutator ./NotoSansArabic-VF.ttf wght=140 wdth=85

.. warning::
   ``fontTools.varLib.mutator`` is deprecated in favor of :mod:`fontTools.varLib.instancer`
   which provides equivalent full instancing and also supports partial instancing.
   Please migrate CLI usage to ``fonttools varLib.instancer`` and API usage to
