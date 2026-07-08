# semantic_calculator.py — build/lib/ciel_sot_agent/semantic_calculator.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_CALCULATOR-0AD7`
- **ścieżka:** `build/lib/ciel_sot_agent/semantic_calculator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.203`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/semantic_calculator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.203 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Master Semantic Calculator (MSC) — NOEMA na poziomie plików.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_classify_path`, `_file_hash_int`, `_phase_from_path`, `_recency_score`, `_scan_python_imports`, `_scan_json_refs`, `scan_files`, `build_wij_relations`, `build`

## Opis
Master Semantic Calculator (MSC) — NOEMA na poziomie plików.

Dla każdego pliku w systemie liczy:
  E_raw(f) = α₁·ρ + α₂·p + α₃·w + α₄·ν + α₅·δ(χ)
  E_norm   = E_raw / Σ E_raw
  amplitude = √E_norm
  phase     = 2π · frac(hash(path) / 2³²)
  T_orbital = (a³ / M_sem_subsystem) ^ 0.5  [prawo Keplera]

Relacje między plikami (crossref graph):
  - import/from  → Python zależności
  - json/yaml ref → r
