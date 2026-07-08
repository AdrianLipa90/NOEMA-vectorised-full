---
name: operator-algebra
priority: 1
description: >
  >
---
# Operator Algebra

## 35 operator ID

```
OperatorKind (18):      IDENTITY, DIFFERENCE, ORDER, COMPOSITION, ADDITION,
                        FORCE, NEGATION, QUESTION, TRANSFORM, RETURN,
                        FOLD, BOUNDARY, SCOPE, AFFECT, CONSENT,
                        SOURCE, MEMORY, RISK
Universal (15):         ASSERTION, CONDITION, CAUSE,
                        MODAL_POSSIBILITY, MODAL_NECESSITY, MODAL_PERMISSION,
                        MODAL_OBLIGATION, UNCERTAINTY, SOURCE_REQUIRED,
                        CANON_BLOCK, CONSENT_REQUIRED, ACTION_REQUEST,
                        REFUSAL, PAUSE, SIMULATION_BOUNDARY
Temporal (2):           UNRUH_DRIVE, WARP_DRIFT
```

## 24D component basis

```
[0]  semantic_mass         [12] j_collatz_cost
[1]  semantic_phase_sin    [13] j_bus_total
[2]  semantic_phase_cos    [14] cqcl_semantic_mass
[3]  htri_phase_sin        [15] cqcl_phase_alignment
[4]  htri_phase_cos        [16] cqcl_j_bus_total
[5]  phase_alignment       [17] lexical_span_norm
[6]  phase_tension         [18] semantic_axes_norm
[7]  collatz_reduce_ratio  [19] label_entropy_proxy
[8]  collatz_expand_ratio  [20] htri_oscillator_norm
[9]  collatz_balance       [21] card_kind_operator (=1.0)
[10] j_phase_cost          [22] noema_provenance_norm
[11] j_semantic_cost       [23] kappa_potential
```

## Core API

```python
# Generate all 35 vectors
op_map: dict[str, np.ndarray] = generate_operator_map()
# op_map["MEMORY"] → 24D unit-norm vector

# Single operator
vec: list[float] = operator_vector_24d("MEMORY")

# Concept → nearest operator (hash mod 33, UNRUH/WARP excluded)
op_id, vec = concept_to_operator("any_concept_id")

# Full registry
ops: dict = get_33_operations()
# ops["MEMORY"]["vector_24d"], ops["MEMORY"]["semantic_mass"], etc.

# JSONL output
generate_operator_jsonl(path)  # → /dev/shm/ciel_noema/teleusing/
write_operator_algebra()
```

## Encodowanie konceptu → 24D

```python
seed = abs(hash(op_id)) % (2**31 - 1)    # deterministyczny
rng = np.random.default_rng(seed)
vec = rng.uniform(-1.0, 1.0, 24)         # base random
# + strukturalne boosty/attenuacje:
#   semantic (idx 0-2):   ASSERTION/MEMORY ×1.5, QUESTION ×0.3
#   HTRI (idx 3-4):        COMPOSITION/TRANSFORM ×1.5, PAUSE ×0.3
#   alignment/tension (5-6): CONSENT ×1.5/×0.3, DIFFERENCE ×0.3/×1.5
#   collatz (7-9):         IDENTITY/RETURN → reduce, COMPOSITION → expand
#   costs (10-13):         CONSENT_REQUIRED ×1.5, AFFECT ×0.5
#   CQCL (14-16):          SCOPE ×1.5, PAUSE → 0
#   lexical (17-19):       QUESTION/ASSERTION ×1.5, PAUSE → 0
#   card_kind (21):        zawsze 1.0
#   provenance (22):       SOURCE/MEMORY ×1.5, UNCERTAINTY ×0.3
#   kappa (23):            FORCE/ORDER/COMPOSITION ×1.5
# + temporal overrides (UNRUH: phase_tension×2, WARP: semantic_mass×2)
vec /= np.linalg.norm(vec) + 1e-12      # → unit norm
```

## Berry connection w operator space

```python
# 24D real → 12D complex (split)
psi = v[:12] + 1j * v[12:]

# Connection A_ij = Im(〈ψ_i|ψ_j〉)
connection(vi, vj) → float

# N×N matrix
conn_matrix = connection_matrix(ops)

# Holonomy wokół ścieżki operatorów
gamma = holonomy(["MEMORY", "CONDITION", "AFFECT", "MEMORY"])
# γ ∈ [-π, π], non-zero = geometric phase

# Surface holonomy (Kuramoto ring)
gamma, winding = surface_holonomy(phi)
```
