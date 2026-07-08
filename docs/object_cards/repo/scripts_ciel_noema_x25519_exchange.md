# ciel_noema_x25519_exchange.py — scripts/ciel_noema_x25519_exchange.py

## Tożsamość
- **id_karty:** `REPO-CIEL_NOEMA_X25519_EX-DFE7`
- **ścieżka:** `scripts/ciel_noema_x25519_exchange.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.370`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_noema_x25519_exchange.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.370 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
X25519 key exchange przez NOEMA nonlocal channel dla anon:812c3335b3c0e6e4.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_pubkey_to_phases`, `_phases_to_pubkey`, `main`, `_finish_exchange`

## Opis
X25519 key exchange przez NOEMA nonlocal channel dla anon:812c3335b3c0e6e4.

Generuje parę kluczy X25519, koduje public key w fazy oscylatorów,
broadcast przez φ-RAG channel, czeka na odpowiedź, oblicza shared secret.
