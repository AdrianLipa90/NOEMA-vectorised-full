# report.py — scripts/ciel_confidence_system/report.py

## Tożsamość
- **id_karty:** `REPO-REPORT-CE96`
- **ścieżka:** `scripts/ciel_confidence_system/report.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.652`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_confidence_system/report.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.652 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
ciel_uncertainty_report.py — Uncertainty dashboard.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_get_db`, `low_confidence_docs`, `unresolved_uncertainty`, `potential_conflicts`, `topic_gaps`, `summary`, `main`

## Opis
ciel_uncertainty_report.py — Uncertainty dashboard.

Pokazuje:
  - Dokumenty z niską pewnością (confidence < 0.6)
  - Nierozwiązane wpisy z uncertainty_log
  - Potencjalne konflikty (wysoka podobieństwo, różne confidence)
  - Luki w wiedzy (tematy z małą liczbą dokumentów)

Uruchom:
  python3 scripts/ciel_uncertainty_report.py [--db /tmp/noema_knowledge.db]
  python3 scripts/ciel_uncertainty_repor
