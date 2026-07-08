# information_flow.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/integration/information_flow.py

## Tożsamość
- **id_karty:** `REPO-INFORMATION_FLOW-5B14`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/integration/information_flow.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.585`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/integration/information_flow.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.585 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
CIEL/Ω — High-level information flow pipeline.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** InformationFlow
- **funkcje:** `step`

## Opis
CIEL/Ω — High-level information flow pipeline.

Stitches bio, emotion, field and memory into a reproducible pipeline.
Single step() method: sensor signal → filter → intention → emotion → memory.

Cross-references:
  bio/           → EEGProcessor, CrystalFieldReceiver
  emotion/       → EmotionCore, EEGEmotionMapper
  fields/        → IntentionField, SoulInvariant
  memory/        → LongTermMemory
