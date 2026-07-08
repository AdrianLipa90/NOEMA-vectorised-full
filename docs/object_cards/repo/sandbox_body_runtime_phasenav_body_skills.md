# phasenav_body_skills.py — sandbox_body/runtime/phasenav_body_skills.py

## Tożsamość
- **id_karty:** `REPO-PHASENAV_BODY_SKILLS-8858`
- **ścieżka:** `sandbox_body/runtime/phasenav_body_skills.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.643`
- **masa_semantyczna:** `0.40`

## Kotwice
- `sandbox_body/runtime/phasenav_body_skills.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.643 |
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
phasenav_body_skills.py — Skills Registry + Routing + Operational Contracts

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `ensure_skills_db`, `import_workbenches`, `import_from_skills_md`, `import_contracts`, `find_skills`, `get_contracts`, `log_skill_usage`, `enrich_prompt`, `contract_context`, `stats`

## Opis
phasenav_body_skills.py — Skills Registry + Routing + Operational Contracts
for the PhaseNav Body Sandbox.

Migrates the NOEMA skill ecosystem into the sandbox body's memory,
enabling skill-aware prompt routing, contract enforcement, and
autonomous task-to-skill matching.

Usage:
    # Initialize skills DB from the main NOEMA ecosystem
    python3 phasenav_body_skills.py --init

    # Find skills
