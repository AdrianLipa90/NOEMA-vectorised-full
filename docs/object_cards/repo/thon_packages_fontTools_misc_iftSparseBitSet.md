# iftSparseBitSet.py — .python_packages/fontTools/misc/iftSparseBitSet.py

## Tożsamość
- **id_karty:** `REPO-IFTSPARSEBITSET-9ED4`
- **ścieżka:** `.python_packages/fontTools/misc/iftSparseBitSet.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.855`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/misc/iftSparseBitSet.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.855 |
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
Sparse Bit Set encoding/decoding for IFT (Incremental Font Transfer).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SparseBitSetDecodeError, _InputBitStream, _OutputBitStream
- **funkcje:** `decode`, `_decodeImpl`, `encode`, `_encodeHeader`, `_decodeHeader`, `_treeHeight`, `_encodeWithBf`, `_trailingZeros`, `rangeCount`, `next`, `bytesConsumed`, `write`, `toBytes`

## Opis
Sparse Bit Set encoding/decoding for IFT (Incremental Font Transfer).

Implements the sparse bit set format defined in the W3C IFT specification:
https://w3c.github.io/IFT/Overview.html#sparse-bit-set-decoding
