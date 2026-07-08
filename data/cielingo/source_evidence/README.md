# CIELingo source evidence extracts

Place local JSONL extracts here for unresolved-word candidate generation.

Each line may contain:

```json
{
  "source_id": "wiktionary-pl-dump:example",
  "source_kind": "open_source_dictionary_extract",
  "source_name": "Wiktionary",
  "license_hint": "check exact dump/license before canon",
  "retrieval_mode": "local_jsonl_no_network",
  "lemma": "przykład",
  "language": "pl",
  "definition": "...",
  "part_of_speech": "noun",
  "synonyms": [],
  "antonyms": [],
  "register": "neutral",
  "emotional_colour": "neutral",
  "emotional_intensity": 0.0,
  "evidence_confidence": 0.5
}
```

The runtime never fetches the network. Candidate cards start at confidence 0.5 only when local evidence exists. Promotion to canon requires review.
