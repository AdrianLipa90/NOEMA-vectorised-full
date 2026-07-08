# psCharStrings.py — .python_packages/fontTools/misc/psCharStrings.py

## Tożsamość
- **id_karty:** `REPO-PSCHARSTRINGS-609A`
- **ścieżka:** `.python_packages/fontTools/misc/psCharStrings.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.592`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/misc/psCharStrings.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.592 |
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
psCharStrings.py -- module implementing various kinds of CharStrings:

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CharStringCompileError, SimpleT2Decompiler, T2StackUseExtractor, T2WidthExtractor, T2OutlineExtractor, T1OutlineExtractor, T2CharString, T1CharString, DictDecompiler
- **funkcje:** `read_operator`, `read_byte`, `read_smallInt1`, `read_smallInt2`, `read_shortInt`, `read_longInt`, `read_fixed1616`, `read_reserved`, `read_realNumber`, `buildOperatorDict`, `getIntEncoder`, `encodeFixed`, `encodeFloat`, `calcSubrBias`, `encodeInt`, `reset`, `execute`, `pop`, `popall`, `push`, `op_return`, `op_endchar`, `op_ignore`, `op_callsubr`, `op_callgsubr`, `op_hstem`, `op_vstem`, `op_hstemhm`, `op_vstemhm`, `op_hintmask`

## Opis
psCharStrings.py -- module implementing various kinds of CharStrings:
CFF dictionary data and Type1/Type2 CharStrings.
