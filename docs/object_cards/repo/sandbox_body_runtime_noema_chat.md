# noema_chat.py — sandbox_body/runtime/noema_chat.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_CHAT-5829`
- **ścieżka:** `sandbox_body/runtime/noema_chat.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.601`
- **masa_semantyczna:** `0.40`

## Kotwice
- `sandbox_body/runtime/noema_chat.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.601 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
noema-chat — CLI wektoryzowany przez PhaseNav.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** C
- **funkcje:** `color_op`, `color_r`, `color_tau`, `format_response`, `query`, `load_skill`, `save_history`, `interactive`, `main`

## Opis
noema-chat — CLI wektoryzowany przez PhaseNav.
Unix socket → body daemon → wheel engine → odpowiedź.
Kolor, skille, pipeline, historia.
