# semantic_calculator.py — src/ciel_sot_agent/semantic_calculator.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_CALCULATOR-7047`
- **ścieżka:** `src/ciel_sot_agent/semantic_calculator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.943`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/semantic_calculator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.943 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


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
