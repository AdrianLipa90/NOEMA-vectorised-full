# eexec.py — .python_packages/fontTools/misc/eexec.py

## Tożsamość
- **id_karty:** `REPO-EEXEC-88CF`
- **ścieżka:** `.python_packages/fontTools/misc/eexec.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.254`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/misc/eexec.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.254 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
PostScript Type 1 fonts make use of two types of encryption: charstring

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_decryptChar`, `_encryptChar`, `decrypt`, `encrypt`, `hexString`, `deHexString`

## Opis
PostScript Type 1 fonts make use of two types of encryption: charstring
encryption and ``eexec`` encryption. Charstring encryption is used for
the charstrings themselves, while ``eexec`` is used to encrypt larger
sections of the font program, such as the ``Private`` and ``CharStrings``
dictionaries. Despite the different names, the algorithm is the same,
although ``eexec`` encryption uses a fixed
