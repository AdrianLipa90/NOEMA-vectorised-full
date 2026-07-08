# linguistic_database.py — build/lib/cielingo/polish/linguistic_database.py

## Tożsamość
- **id_karty:** `REPO-LINGUISTIC_DATABASE-E589`
- **ścieżka:** `build/lib/cielingo/polish/linguistic_database.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.523`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/polish/linguistic_database.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.523 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Polish linguistic database for CIELingo.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Lexeme, PolishLinguisticDatabase
- **funkcje:** `load_polish_database`, `case_for`, `lookup_form`, `parts_of_speech`, `sentence_parts`, `morphology`, `semantic_mass_axes`, `semantic_mass`, `punctuation_operator`, `database_summary`

## Opis
Polish linguistic database for CIELingo.

This is a compact runtime database and adapter. It does not pretend to be a
complete Polish grammar; it gives the executable surface required by CIELingo:
parts of speech, sentence parts, morphology, punctuation, word order,
semantic mass axes, vocabulary seed and links to lingophysics LNS.
