# tfmLib.py — .python_packages/fontTools/tfmLib.py

## Tożsamość
- **id_karty:** `REPO-TFMLIB-48DA`
- **ścieżka:** `.python_packages/fontTools/tfmLib.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.488`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/tfmLib.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.488 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Module for reading TFM (TeX Font Metrics) files.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TFMException, TFM
- **funkcje:** `_read`, `char_info`, `width_index`, `noneexistent`, `height_index`, `depth_index`, `italic_index`, `tag`, `remainder`, `width`, `height`, `depth`, `italic`, `exten`, `lig_step`, `lig_kern_command`, `kern`, `param`, `read_fixed`

## Opis
Module for reading TFM (TeX Font Metrics) files.

The TFM format is described in the TFtoPL WEB source code, whose typeset form
can be found on `CTAN <http://mirrors.ctan.org/info/knuth-pdf/texware/tftopl.pdf>`_.

        >>> from fontTools.tfmLib import TFM
        >>> tfm = TFM("Tests/tfmLib/data/cmr10.tfm")
        >>>
        >>> # Accessing an attribute gets you metadata.
        >>> tfm.chec
