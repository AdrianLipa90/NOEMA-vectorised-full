# CIELingo Linguistic Topology

## Overview

CIELingo is a linguistic topology engine for Polish. It maps natural language text onto the NOEMA 24-oscillator HTRI surface via phase-token encoding. It uses a card-based radical lexicon, infinitive/modal grammar analysis, Collatz-based semantic synchronization, and tensor-scalar context fields. CIELingo is the language carrier of the CIEL system — it translates between human language and the oscillatory phase topology of NOEMA.

**Primary language:** Polish (full radical card set, inflection handling, infinitive grammar).  
**Experimental:** English, Japanese (via alignment cards in `cards/cielingo_alignments/`).

**Source package:** `src/cielingo/` — ~30 modules, zero external NLP dependencies (stdlib + numpy only).

---

## Architecture

```
Polish text
    │
    ▼
tokenize_surface()          phase_sense_parser.py
    │                           regex split, Unicode NFKC normalization
    ▼
card lookup                  lns_language_cards.py
    │                           radical cards → slot_id → oscillator mapping
    ▼
phase offset                 infinitive_modal_potential.py
    │                           infinitive seed → modality map → phase shift
    ▼
Collatz sync                 collatz_semantic_htri_sync.py
    │                           per-token Collatz trajectory → oscillator index
    ▼
HTRI phase bus               htri_phase_bus.py
    │                           24D phase bus binding, alignment, tension
    ▼
Vector surface               vector_surface.py
    │                           24-component fixed-dimension vector
    ▼
Tensor-scalar field          tensor_scalar_field.py
    │                           3×3 tensor + scalar affect channels
    ▼
Triadic output               triadic_output_vector.py
    │                           3 × 24D = 72D output (comprehension, inference, expression)
    ▼
OrchORbital router           orchorbital_router.py
                                → NOEMA surface / SoT / nonlocal execution
```

---

## Key Components

### card_trace_eeg.py

Traces word cards through an EEG-layered card space, producing a `CardTrace` per word — a multi-line trace pattern with amplitude, phase, semantic mass, affective weight, and orbital position. A `CardTraceSnap` captures the full window as a memory snapshot for later comparison via `snap_similarity()`.

**Input:** Polish text string.  
**Output:** List of `{card_id, amplitude, phase, semantic_mass, affective_weight, orbital_position, channel}` per token.

Seven default trace channels: semantic, memory, affective, procedural, ethical, orbital, pipeline.

### htri_brain_map.py

Maps 24 HTRI oscillators to brain regions and cognitive domains. Each oscillator has:
- `id` (0–23), `brain_region` (dlPFC, vmPFC, OFC, SMA, M1, S1, IPL, STG, MTG, V1, Hippocampus, Amygdala, ACC, Insula, BG, Cerebellum, Thalamus, Hypothalamus, VTA, LC, PCC, AG, TPJ, dACC)
- `domain` (executive, ethics, affect, procedural, motor, sensory, spatial, phonological, lexical, visual, episodic, conflict, self, habit, timing, gate, drive, reward, arousal, dmn, semantic, social, salience)
- `base_freq_hz` (~7.47–7.98 Hz range)
- `default_couplings` (target oscillator + weight tuples)
- `affect_sensitivity` (none/low/medium/high)
- `logic_role` (e.g. operator_composition, ethical_valuation, lexical_semantics)

The `oscillator_for_card()` function assigns a card to the best-matching oscillator by keyword match + phase proximity + domain affinity.

Returns full topology via `brain_phase_topology()` with all 24 nodes, domains, couplings, and edge counts.

### htri_phase_bus.py

Binds CIELingo language cards to the shared HTRI phase carrier. A `PhaseBusNode` records per-card: oscillator_id, base frequency, omega0, semantic mass, semantic phase, HTRI phase, phase alignment, phase tension, Collatz trajectory stats, J-functional costs (phase, semantic, Collatz, total), CQCL quantum variables, NOEMA provenance tags, OrchORbital channel, and phase lane.

The bus computes `phase_alignment = cos(semantic_phase - htri_phase)` and `phase_tension = 1 - alignment^2`.

**Input:** Query string + concept tokens.  
**Output:** `PhaseBusReport` with card_count, oscillator count, mean alignment, mean tension, bus actions.

Main functions: `bind_card_to_phase_bus()`, `phase_bus_report()`, `select_phase_bus_cards()`.

### collatz_semantic_htri_sync.py

Deterministic synchronization layer. Each CIELingo card receives a Collatz trajectory from its semantic seed. The trajectory index maps to an oscillator index for the 24-oscillator HTRI grid.

`CardSyncState` holds: card_id, oscillator_id, base frequency, semantic phase, oscillator phase, phase alignment, Collatz stats (seed, steps, reduce_count, expand_count), mode bias (favour reduction vs expansion), sync pressure, and recommended action (hold/reduce/expand).

Constants: `BASE_FREQUENCY_HZ = 7.83`, `DEFAULT_OSCILLATORS = 24`.

### lexical_holonomy.py

Establishes relations between words via Berry phase accumulation. As words are processed, their semantic phase accumulates geometric holonomy from word-to-word transitions.

Implements four relation layers:
1. Card-internal seed relations (synonyms, antonyms, forms, examples)
2. Batch relation CSV edges (supports/opposes/contains between concepts)
3. Cross-card semantic proximity (shared axes, phase distance, vector distance)
4. Per-word knowledge notes (confidence, provenance, verification state)

Tracks open-source lexical sources as descriptors (Wiktionary, plWordNet, SGJP/Morfeusz) without importing them.

### vector_surface.py

Converts the LNS/NOEMA language-card phase bus into a fixed 24-component vector. Each component maps to a specific field:

| Index | Component | Source |
|---|---|---|
| 0 | semantic_mass | Card semantic mass |
| 1–2 | semantic_phase sin/cos | Phase encoding |
| 3–4 | htri_phase sin/cos | Bus phase |
| 5 | phase_alignment | cos(Δφ) |
| 6 | phase_tension | 1 − alignment² |
| 7–9 | collatz ratio/balance | Reduce/expand fractions |
| 10–13 | J-functional costs | phase, semantic, collatz, total |
| 14–16 | CQCL variables | Normalized fields |
| 17–18 | lexical spans | Norms |
| 19 | label entropy | Diversity proxy |
| 20 | htri oscillator norm | Amplitude envelope |
| 21 | card_kind_operator | Operator flag |
| 22 | noema provenance norm | Source diversity |
| 23 | kappa_potential | KAPPA_INFO = ln(2)/(24π) |

### tensor_scalar_field.py

Adds a field-theoretic interpretation to the 24D vector surface:
- **Real information exchange:** rank-2 tensor-like 3×3 matrix with axes: semantic_mass_phase, collatz_jfunctional_transport, lexical_holonomy_exchange
- **Contextual/affective scalar medium:** scalar channels density, viscosity, colour, saturation
- **Affect proxies:** sarcasm, excitement, tension, relief, fear — treated as scalar-context proxies via keyword matching (PL/EN keywords per channel)

### phase_sense_parser.py

Parses Polish text into phase-tagged sense units. Pipeline:
1. Unicode NFKC normalization and whitespace collapsing
2. Tokenization via regex `[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+`
3. Per-token card lookup in LNS language cards
4. Phase computation: each token gets a deterministic phase from `blake2b(text) → [0, 2π)`
5. Vector encoding via `vectorize_card()`
6. Tensor-scalar context via `tensor_scalar_state_from_card()`
7. Word knowledge notes from `lexical_holonomy.py`

Handles inflection, aspect, negation, and modality through the grammatical analysis pipeline.

### meaning_debt_word_cards.py

Tracks unresolved words that have no card match. The "meaning debt" system:
- Reads a CIEL-POL meaning-debt index
- Converts unknown words into `DebtCandidateWordCard` entries with confidence 0.5
- Assigns grammatical designation (infinitive detection, POS candidates)
- Each candidate requires evidence + supervised review before canonization
- Supports deferred resolution protocol

### infinitive_modal_potential.py

Analyzes Polish verb aspect, tense, and mood. Core flow:
1. `load_infinitive_seeds()` → load Polish infinitive seeds from `polish/linguistic_database.py`
2. `load_modality_seeds()` → load modality operators (necessity, possibility, permission, obligation, volition)
3. `map_infinitive_to_modalities()` → N-body interaction via kappa_info = ln(2)/(24π)
4. Each infinitive seed gets: semantic axes, rest semantic mass, potential phi, Collatz seed, phase, HTRI oscillator ID
5. Each modality gets: modality type (necessity/possibility/permission/obligation/volition), gravitational-like interaction with infinitive seeds

### triadic_output_vector.py

Produces the final 3-lane (emotion, ethics, identity) output:
- **Comprehension lane (24D):** word-to-phase understanding and confidence
- **Inference lane (24D):** shared CIELingo vector/HTRI/J/CQCL transport
- **Expression lane (24D):** output readiness through tensor-scalar resistance/thinning

Full output: 72D vector (`TRIAD_VECTOR_DIM = 72`). Includes `on_vivo_output_test()` for runtime verification.

### canonization_audit.py

Validates card coverage for any input text. Levels:
- `external_canon`: requires imported dictionary evidence (none created locally)
- `local_morphology_canon_candidate`: deterministic local infinitive mapping
- `local_residual_set_canon`: owned residual set membership as CIELingo workflow fact
- `deferred`: insufficient evidence

### orchorbital_router.py

Routes CIELingo output to the orbital bridge. Consumes current card-trace EEG snap, memory snaps, and Semantic Collatz route, then emits an association/reduction/expansion decision.

`OrchORbitalDecision` includes: operator (associate/reduce/expand), selected memory snap, association score, route summary, execution layer flag.

---

## Phase Encoding Process (Detailed)

### Step 1: Tokenization

`phase_sense_parser.tokenize_surface(text)` — regex split on Unicode word boundaries, NFKC normalization, lowercasing. Returns a list of surface tokens.

### Step 2: Radical Card Lookup

For each token, `lns_language_cards.search_language_cards(token)` looks up the token's lemma in the loaded card set. Radical cards at `cards/cielingo_radicals/radical_cards_seed_v0_1.jsonl` map slot_id (1–24) to semantic primitives. The slot_id directly maps to oscillator_id = slot_id − 1.

### Step 3: Grammatical Phase Offset

`infinitive_modal_potential.map_infinitive_to_modalities()` — if the token is a Polish verb, its infinitive seed is looked up in the Polish linguistic database. The modality operator (necessity, possibility, etc.) adds a phase offset proportional to the interaction potential.

### Step 4: Collatz Trajectory

`collatz_semantic_htri_sync.synchronize_card()` — computes a Collatz trajectory from the card's semantic seed:
```python
seed → Collatz(seed) → trajectory lengths → reduce_count / expand_count
→ mode_bias → sync_pressure → oscillator alignment
```

The trajectory index modulo 24 selects the oscillator for synchronization.

### Step 5: HTRI Bus Binding

`htri_phase_bus.bind_card_to_phase_bus()` — writes the card's phase, mass, and J-functional costs onto the shared phase bus. Each bound card produces a `PhaseBusNode` with all alignment metrics.

### Step 6: Vector Surface

`vector_surface.vectorize_card()` — converts the `PhaseBusNode` into a 24D float vector per the VECTOR_COMPONENTS schema.

### Step 7: Tensor-Scalar Context

`tensor_scalar_field.tensor_scalar_state_from_card()` — builds a 3×3 tensor from token-to-token phase differences and a 4-channel scalar field (density, viscosity, colour, saturation) plus 5 affect proxies.

### Step 8: Triadic Output

`triadic_output_vector.vectorize_triadic_output()` — combines comprehension, inference, and expression lanes into a single 72D output vector.

### Step 9: Orbital Routing

`orchorbital_router.route_orchorbital()` — feeds the triadic output and card trace snap into the orbital bridge for potential surface writeback.

---

## Language Support

### Polish (Primary)

- Full radical card set (24 radicals mapped to 24 HTRI oscillators)
- Inflection handling through `polish/grammar_algorithms.py` and `polish/linguistic_database.py`
- Infinitive detection via `infinitive_modal_potential.py`
- Grammatical designation via `meaning_debt_word_cards.py`
- J-functional computation via `polish/j_functionals.py`
- Semantic mass assignment via `polish/semantic_mass.py`
- Holonomy accumulation via `polish/holonomies.py`
- Lingophysics bridge (`polish/lingophysics_bridge.py`) connects linguistic features to HTRI phase topology

### English, Japanese (Experimental)

- Alignment cards at `cards/cielingo_alignments/alignment_seed_en_ja_v0_1.jsonl` (24 alignment records)
- Slot entries at `cards/cielingo_languages/en/` and `cards/cielingo_languages/ja/`
- Language-local J-functionals preserve local holonomy
- `lns_language_cards.py` loads language-specific entries and alignment records
- Japanese entries marked `needs_native_review: true`

---

## Radical Card Schema

Radical cards are stored at `cards/cielingo_radicals/radical_cards_seed_v0_1.jsonl` (JSONL format, one card per line):

```json
{
  "slot_id": 1,
  "radical_id": "rad_entity",
  "label": "ENTITY",
  "primitive_family": ["ONTOLOGY"],
  "gloss": "A distinguishable being/object/participant in a linguistic equation.",
  "relation_axes": ["HAS_IDENTITY"],
  "runtime_axes": ["reference"],
  "source_binding": "ARTIFACT_GROUNDED",
  "validation_status": "draft",
  "confidence": 0.7,
  "notes": ["Stage 0 radical seed; universal anchor, not a claim of semantic identity across languages."]
}
```

| Field | Description |
|---|---|
| `slot_id` | 1–24, maps to oscillator (slot_id − 1) |
| `radical_id` | Unique identifier prefixed `rad_` |
| `label` | Uppercase semantic label (e.g. ENTITY, ACTION) |
| `primitive_family` | Ontological category (ONTOLOGY, EVENT, EPISTEMIC, etc.) |
| `gloss` | English definition |
| `relation_axes` | Typed relations this radical participates in |
| `runtime_axes` | Runtime behaviours (reference, action_intent, consent_gate, etc.) |
| `source_binding` | Provenance level (ARTIFACT_GROUNDED, HYPOTHESIS, POETIC_SYMBOLIC, etc.) |
| `validation_status` | draft, candidate, present, rejected, etc. |
| `confidence` | 0.0–1.0 |
| `notes` | Documentation and caveats |

Valid `source_binding` values: SOURCE, ARTIFACT_GROUNDED, PROXY_VERIFIED, HYPOTHESIS, SIMULATION, INTERPRETATION, POETIC_SYMBOLIC, UNKNOWN.

Valid `alignment_type` values: exact_formal, near_functional, broad_overlap, idiomatic_equivalent, cultural_analogue, false_friend, untranslatable_residue, slot_correspondence.

---

## Connection to NOEMA Runtime

CIELingo output feeds into:
1. **HTRI Kuramoto surface** — phase values from tokens perturb oscillator phases
2. **Nonlocal proxy** — unresolved words trigger deferred resolution protocol
3. **Memory orchestrator** — triadic output vectors are stored as memory traces
4. **Orbital bridge** — CIELingo card traces are consumed by the orbital synchronization loop
5. **CQCL engine** — J-functional costs and quantum variables feed flavor mixing and coupling optimization
