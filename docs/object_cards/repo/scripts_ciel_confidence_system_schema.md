# schema.py — scripts/ciel_confidence_system/schema.py

## Tożsamość
- **id_karty:** `REPO-SCHEMA-D1F5`
- **ścieżka:** `scripts/ciel_confidence_system/schema.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.067`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_confidence_system/schema.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.067 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
ciel_schema_migrate.py — Migracja schematu Knowledge DB dla confidence/uncertainty.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `migrate`, `main`

## Opis
ciel_schema_migrate.py — Migracja schematu Knowledge DB dla confidence/uncertainty.

Dodaje:
  - Kolumny confidence do doc_analysis
  - Tabelę confidence_scores (rozbicie na składowe)
  - Tabelę uncertainty_log (śledzenie niskiej pewności)
  - Tabelę source_reliability (wagi źródeł)

Uruchom: python3 scripts/ciel_schema_migrate.py [--db /tmp/noema_knowledge.db]
