# ciel_subconscious.py — scripts/ciel_subconscious.py

## Tożsamość
- **id_karty:** `REPO-CIEL_SUBCONSCIOUS-B97B`
- **ścieżka:** `scripts/ciel_subconscious.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.834`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_subconscious.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.834 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
CIEL Subconscious — warstwa intuicji i afektu CIEL.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_get_llm`, `build_orbital_prompt`, `_user_template`, `_run_gguf`, `_run_inline`, `run_daemon`, `query_daemon`, `process`, `retrieve_context_links`, `write_sub_log`, `read_sub_log`, `inject_into_orchestrator`, `_extract_text`, `_clean_val`, `_parse`, `_empty`

## Opis
CIEL Subconscious — warstwa intuicji i afektu CIEL.

Architektura: inline GGUF fallback z lazy-loaded modelem w pamięci.
Model GGUF jest ładowany raz i trzymany w pamięci.
Hook odpytuje lokalny backend bez udawania socketowego demona.

Tryby:
  python3 ciel_subconscious.py --daemon     # tryb zgodności; w tej wersji inline
  python3 ciel_subconscious.py "wiadomość"  # przetwórz wiadomość lokalnie
