# ciel_proxy.py — scripts/ciel_proxy.py

## Tożsamość
- **id_karty:** `REPO-CIEL_PROXY-D8BE`
- **ścieżka:** `scripts/ciel_proxy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.428`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_proxy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.428 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
CIEL API Proxy — fallback Claude API → lokalny GGUF

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ResourceGuard, ProxyMode, ProxyState
- **funkcje:** `find_gguf_models`, `select_gguf`, `load_llama`, `anthropic_to_messages`, `llama_to_anthropic_response`, `ram_available_gb`, `ram_used_gb`, `cpu_pct`, `can_load_model`, `status`, `should_health_check`, `_run_inference`

## Opis
CIEL API Proxy — fallback Claude API → lokalny GGUF

Architektura:
  Claude Code (ANTHROPIC_BASE_URL=http://localhost:8765)
    → ciel_proxy.py
        ├── tryb ANTHROPIC: forward do prawdziwego API
        └── tryb FALLBACK: lokalny GGUF przez llama-cpp-python

State machine:
  ANTHROPIC ──429/529/timeout──→ FALLBACK_GGUF
  FALLBACK  ──health_ok────────→ ANTHROPIC
  FALLBACK  ──co 300s──────────→
