# auto_verify.py — src/cielingo_core/bridge/auto_verify.py

## Tożsamość
- **id_karty:** `REPO-AUTO_VERIFY-F237`
- **ścieżka:** `src/cielingo_core/bridge/auto_verify.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.325`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/bridge/auto_verify.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.325 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
AutoVerify — CIELingo internet autoweryfikacja i autolearning.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AutoVerifyResult, AutoVerify
- **funkcje:** `_load_known_words`, `extract_unknown_words`, `_load_stored_cards`, `_card_id`, `_search_word`, `_try_dictionaryapi_dev`, `_try_sjp_pl`, `_try_wiktionary_lookup`, `_try_wikipedia_lookup`, `_infer_language`, `_pos_suffix_heuristic`, `generate_card_from_search`, `to_dict`, `verify_and_learn`, `inventory`

## Opis
AutoVerify — CIELingo internet autoweryfikacja i autolearning.

Detects unknown words in prompts, looks them up via web search,
generates word cards, stores in semantic memory lane, returns
enrichment context.

Protocol:
  av = AutoVerify()
  result = av.verify_and_learn(prompt_text)
  # result.enrichment -> goes into CIEL inject / context
