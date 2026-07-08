# NOEMA Card Systems Reference

NOEMA uses two distinct card systems that serve different purposes in the topology: **Nonlocal Cards** (JSON, at `cards/base/noema_nonlocal_db/`) define the system's functional architecture as a directed graph, and **Object Cards** (Markdown, at `docs/object_cards/`) document runtime entities, code modules, and concept mappings. A third supplementary card category — **Word Cards** (JSONL, at `src/cielingo/cards/`) — feeds the CIELingo linguistic topology engine.

---

## 1. Nonlocal Cards

**Location:** `cards/base/noema_nonlocal_db/` — 33 cards indexed 000–033.

**Registry:** `cards/base/noema_nonlocal_db/registry.json` (schema `noema:nonlocal_db:registry:v0.2`) contains the master index with schema audit, gaps, and anomalies.

**Schema versions:**

| Range | Schema | Count |
|---|---|---|
| 000–009, 011–013 | `noema/nonlocal-db-card/v0.1` | 13 |
| 014–033 | `noema/card/v0.1` | 20 |

**Known gap:** Card 010 does not exist (skipped 009→011).

**Buildroot subregistry:** A dedicated auxiliary Buildroot card DB lives at `cards/base/buildroot_nonlocal_db/` and is bridged into the main nonlocal DB by `047_BUILDROOT_CARD_DB.noema.card.json`. It is generated from the live Buildroot tree via `src/ciel_sot_agent/buildroot_card_db.py` and mirrors the root/boot/linux/toolchain/system/fs/package/probe slices used by the PhaseNav probe.

**Anomalies recorded in registry:**
- Card 011 was repurposed (deprecated HOLONOMY_MEDIUM → CIELINGO_CARD_TRACE_ORCHORBITAL)
- Cards 011 and 020 were missing `status` field (resolved 2026-06-22)
- Card 011 has inconsistent `card_id` format
- Dual schema with incompatible field structures (migration deferred)

### Card JSON Structure

Each card is a JSON file containing:
- `id` — unique identifier (e.g. `noema:nonlocal_db:000_ROOT` or `noema:card:016:cielingo_collatz_semantic_htri_sync`)
- `name` — human-readable title
- `layer` — functional layer designation
- `schema` — schema version string
- `description` — purpose and behaviour
- `edges` — links to other cards, forming a directed graph

### Card Inventory (33 cards)

| ID | Name | Layer | Description |
|---|---|---|---|
| 000 | ROOT | bootstrap | NOEMA root card, system anchor |
| 001 | DOCTOR | bootstrap | NOEMA Doctor, self-diagnosis entry |
| 002 | PIPELINE SURFACE | bootstrap | Pipeline surface for data flow |
| 003 | HTRI KURAMOTO 120 | bootstrap | HTRI Kuramoto 120-oscillator reference |
| 004 | J FUNCTIONAL | bootstrap | J-functional cost surface |
| 005 | PAIN SURFACE | bootstrap | Pain surface for constraint encoding |
| 006 | SEMANTIC BRIDGE | bootstrap | Semantic bridge between layers |
| 007 | NONLOCAL PROXY | bootstrap | Nonlocal proxy for async ops |
| 008 | EULER BERRY CLOSURE | bootstrap | Euler-Berry closure condition |
| 009 | NOEMA PRIORITY FIELD | bootstrap | Priority field for scheduling |
| 011 | CIELINGO CARD TRACE ORCHORBITAL | speech_memory | Card trace EEG + OrchORbital router |
| 012 | CIELINGO POLISH LINGUISTIC SURFACE | bootstrap | Polish linguistic surface |
| 013 | HOLONOMY MEDIUM | bootstrap | Holonomy medium scalar grid |
| 014 | MONGO FILE INDEX | core | Mongo-backed NOEMA file index |
| 015 | CIELINGO LNS LANGUAGE CARDS | cielingo | LNS language cards |
| 016 | CIELINGO COLLATZ SEMANTIC HTRI SYNC | cielingo | Collatz-semantic-HTRI sync |
| 017 | CIELINGO HTRI PHASE BUS | cielingo | HTRI phase bus binding |
| 018 | CIELINGO INFINITIVE MODAL POTENTIAL | cielingo | Infinitive→modal potential |
| 019 | CIELINGO VECTOR SURFACE | cielingo | 24D vector compatibility surface |
| 020 | CIELINGO LEXICAL HOLONOMY | cielingo | Lexical Berry phase accumulation |
| 021 | CIELINGO TENSOR SCALAR CONTEXT FIELD | cielingo | Tensor-scalar context field |
| 022 | CIELINGO PHASE SENSE OUTPUT TRIAD | cielingo | Phase sense parser + triadic output |
| 023 | CIELINGO REALTIME UNRESOLVED PROTOCOL | cielingo | Real-time unresolved word protocol |
| 024 | CIELINGO MEANING DEBT WORD CARDS | cielingo.debt_surface | Meaning-debt word card scaffolder |
| 025 | ERB METRIC TENSOR | noema_erb | ERB metric tensor g_ij |
| 026 | CQCL FLAVOR MIXING | noema_erb | CQCL flavor mixing (neutrino analogy) |
| 027 | YUKAWA CIELINGO COUPLER | noema_erb | Yukawa CIELingo coupler Y_NOEMA |
| 028 | OPENCODE CIEL INSTRUCTIONS | opencode | Opencode CIEL instruction surface |
| 029 | OPENCODE DIRECT CIEL COUPLING | opencode | Opencode direct CIEL coupling |
| 030 | OPENCODE RAW LOG TSM BRIDGE | opencode.memory_ingest | Opencode raw log → TSM bridge |
| 031 | PHASE MEMORY BINARY VECTOR ADAPTER | ciel_memory | Phase memory binary-vector adapter |
| 032 | RESONANCE BRIDGE | noema_erb.imaginal | Real-imaginal resonance bridge |
| 033 | DUAL SURFACE PIPELINE RUNNER | noema_erb.imaginal | Dual-surface pipeline runner |

### Layer Organization

- **bootstrap (000–009, 012–013):** Core boot cards — root, doctor, pipeline, Kuramoto, J-functional, pain, semantic bridge, nonlocal proxy, Euler-Berry, priority field, Polish surface, holonomy medium
- **speech_memory (011):** Card trace EEG and OrchORbital routing
- **core (014):** Mongo file index
- **cielingo (015–024):** Full CIELingo linguistic stack — LNS cards, Collatz sync, phase bus, infinitive modal, vector surface, lexical holonomy, tensor-scalar, phase sense, unresolved protocol, meaning debt
- **noema_erb (025–027):** ERB metric tensor, CQCL flavor mixing, Yukawa coupler
- **opencode (028–030):** Opencode integration — instructions, direct coupling, raw log bridge
- **ciel_memory (031):** Phase memory binary-vector adapter
- **noema_erb.imaginal (032–033):** Resonance bridge, dual-surface pipeline

### Directed Graph (Edges)

Each card contains an `edges` array referencing other cards by ID. These edges define:
- Synchronization dependencies (card A must be synced before card B)
- Data flow paths (card A writes state consumed by card B)
- Topological ordering for the orbital bridge and synchronizer
- Constraint propagation chains

The registry's anomalies section records structural issues in edge definitions.

---

## 2. Object Cards

**Location:** `docs/object_cards/` — Markdown files organized by category.

**Categories:**

| Directory | Contents |
|---|---|
| `nonlocal/` | 6 nonlocal runtime-layer cards |
| `repo/` | ~100+ cards for scripts and packages |
| `db/entities/` | 21 relational entities (people, concepts, subsystems) |
| `db/repos/` | 5 repository-level orbital cards |
| `db/sectors/` | 6 sector cards (memory, bridge, vocabulary, fields, runtime, constraints) |
| `db/tsm/` | TSM (temporal state memory) cards |
| `db/words/` | Word concept cards (e.g. WORD-0001: water) |
| `satellites/` | 11 satellite cards (NOEMA, P3, P7, consolidator, audio, etc.) |
| `session/` | Session-level cards (currently empty) |

### Nonlocal Object Cards (6)

| ID | Name | Purpose |
|---|---|---|
| NL-HOLOMEM-0001 | HolonomicMemoryOrchestrator | Holonomic memory orchestration |
| NL-EBA-0002 | EBA Loop Evaluation Set | EBA loop evaluation |
| NL-BRIDGE-0003 | MemoryCorePhaseBridge | Memory core phase bridging |
| NL-PHASE-0004 | PhaseInfoSystem | Phase information system |
| NL-BERRY-ACC-0005 | BerryAccumulatedHolonomy | Berry phase accumulator (winding, groove depth) |
| NL-WIJ-0005 | WijCouplingOptimizer | L-BFGS-B coupling optimizer (closure_penalty) |

### Repo Object Cards (~100+)

Located at `docs/object_cards/repo/`, these document every significant script and package in the project. Naming convention mirrors source paths:
- `scripts_*.md` — scripts in `scripts/`
- `src_ciel_sot_agent_*.md` — modules in `src/ciel_sot_agent/`
- `src_CIEL_OMEGA_COMPLETE_SYSTEM_*.md` — modules in `src/CIEL_OMEGA_COMPLETE_SYSTEM/`
- `integration_*.md` — integration manifests

The repo/object card generators now emit native PhaseNav labels and Polish section headers, while keeping the path-based naming convention unchanged.

### DB Entity Cards (21 objects)

Defined in `docs/object_cards/db/entities/` with orbital parameters:
- `M_sem` — semantic mass
- `attractor` — attractor type (procedural, abstraction, identity, conflict, project)
- `T_orbit` — orbital period

Key entities: Adrian_Lipa, relational_contract, HTRI, Kuramoto, Berry_holonomy, CIEL_pipeline, Lie4, Zeta_Schrodinger, Intention_Field, soul_invariant, etc.

### Creating a New Object Card

1. Choose the category directory (`nonlocal/`, `repo/`, `db/entities/`, etc.)
2. Create a Markdown file with a unique ID (e.g. `NL-NEW-0001.md` or `entity_new_concept.md`)
3. Follow the established frontmatter pattern:
   - `id` — unique identifier
   - `type` — card category
   - `description` — what this card represents
   - `connections` — links to other cards (by ID)
   - `parameters` — orbital/phase parameters if applicable
4. Update the corresponding `INDEX.md` in the category directory

### Linking Cards via Edges

- **Nonlocal cards** use JSON `edges` arrays referencing other card IDs
- **Object cards** use Markdown links and frontmatter `connections` fields
- **Orbital bridge** consumes edges to build the system topology graph for sync ordering
- **Synchronizer** uses the edge graph to determine dependency resolution order

### Card System Usage

- **Orbital bridge** (`src/ciel_sot_agent/orbital_bridge.py`): Reads nonlocal card edges to determine synchronization order and constraint propagation
- **Synchronizer** (`src/ciel_sot_agent/synchronize.py`, `synchronize_v2.py`): Uses card topology to sequence phase updates and dependency resolution
- **Registry generator** (`scripts/build_nonlocal_cards_registry.py`): Rebuilds `registry.json` from on-disk cards
- **CIELingo** (`src/cielingo/`): Reads language cards and nonlocal CIELingo-layer cards for phase encoding
- **Phase bus** (`src/cielingo/htri_phase_bus.py`): Binds card state to HTRI oscillator surface

---

## 3. Word Cards (CIELingo Radical + Language)

### Radical Cards

**Location:** `cards/cielingo_radicals/radical_cards_seed_v0_1.jsonl` — 24 radical cards.

Each radical card defines a universal semantic primitive:

```json
{
  "slot_id": 1..24,
  "radical_id": "rad_entity",
  "label": "ENTITY",
  "gloss": "A distinguishable being/object/participant in a linguistic equation.",
  "primitive_family": ["ONTOLOGY"],
  "relation_axes": ["HAS_IDENTITY"],
  "runtime_axes": ["reference"],
  "confidence": 0.7,
  "validation_status": "draft"
}
```

Radical set (24 slots): ENTITY, ACTION, STATE, RELATION, SOURCE, EVIDENCE, TRUTH, HYPOTHESIS, SIMULATION, MEMORY, TRACE, CONSENT, REFUSAL, PAUSE, FILE, CHECK_VERIFY, READ, WRITE_SAVE, TEST, MERGE, BRIDGE, NEGATION, QUESTION, CONDITION.

### Language Alignment Cards

**Location:** `cards/cielingo_alignments/alignment_seed_en_ja_v0_1.jsonl` — 24 alignment records mapping EN and JA slots to the same 24 radical slots.

### Language Slot Entries

**Location:** `cards/cielingo_languages/en/slot_entries_test_v0_1.jsonl` and `cards/cielingo_languages/ja/slot_entries_test_v0_1.jsonl`

Each entry provides language-local realizations of a radical slot with local holonomy parameters.

### How Word Cards Feed Phase-Token Mapping

1. Polish text is tokenized via `phase_sense_parser.py` (regex split on Unicode word boundaries)
2. Each token is looked up against radical cards via `lns_language_cards.py`
3. Radical's `slot_id` maps to oscillator ID 0..23 via `stage0_radical_cards.py`
4. Grammatical features (inflection, modality) adjust phase offset via `infinitive_modal_potential.py`
5. Collatz trajectory from `collatz_semantic_htri_sync.py` maps to oscillator index for sync
6. Output: 24D vector surface + tensor-scalar context field + triadic output vector
