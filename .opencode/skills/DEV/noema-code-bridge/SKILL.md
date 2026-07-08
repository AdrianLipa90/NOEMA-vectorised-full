---
name: noema-code-bridge
priority: 1
description: >
  >
---
# noema-code-bridge

## Usage

```bash
.venv/bin/python3 src/noema_learned/code_concept_bridge.py <plik.py>
```

## Pipeline

```
Source code
  ↓ ast.parse + ast.walk
AST node types → operator map (Import→SOURCE_REQUIRED, ClassDef→ASSERTION, etc.)
  ↓ weighted sum of operator_signature() vectors
24D concept vector
  ↓ nearest operator
Primary operator + coherence_R + harmonic_fingerprint
  ↓ seed_to_surface()
Injection into surface phi (strength 0.12-0.15)
```

## AST→Operator map

| AST node | Operator |
|----------|----------|
| `Import`, `ImportFrom` | SOURCE_REQUIRED |
| `ClassDef` | ASSERTION |
| `FunctionDef`, `AsyncFunctionDef` | ACTION_REQUEST |
| `Return` | RETURN |
| `If`, `While` | CONDITION |
| `For`, `Lambda` | COMPOSITION |
| `Try`, `Raise` | RISK |
| `Assign`, `AugAssign` | TRANSFORM |
| `Delete` | NEGATION |
| `Break`, `Continue` | BOUNDARY |
| `With`, `AsyncWith` | CONSENT_REQUIRED |
| `Match` | CONDITION |

## Plik

- `src/noema_learned/code_concept_bridge.py`

## Zależności

Zero poza numpy + stdlib. Żadnego CIELingo core.
