# ciel_session_end.py — scripts/ciel_session_end.py

## Tożsamość
- **id_karty:** `REPO-CIEL_SESSION_END-4695`
- **ścieżka:** `scripts/ciel_session_end.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.784`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_session_end.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.784 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
CIEL SessionEnd Hook

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `session_label`, `write_handoff`, `write_raw_log`, `load_session_log`, `clear_session_log`, `save_phasenav`, `main`

## Opis
CIEL SessionEnd Hook
Zapisuje konwersację do raw_logs/ i aktualizuje handoff.md.
Uruchom przed zamknięciem okna: python3 scripts/ciel_session_end.py [--summary "text"]
