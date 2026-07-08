---
name: noema-test-infra
priority: 1
description: >
  >
---
# Test Infrastructure

## Run

```bash
.venv/bin/python3 -m pytest tests/ -v
# or specific:
.venv/bin/python3 -m pytest tests/test_cielingo.py -v
```

## Coverage

| Test | Lokacja | Status (Jun 25) |
|------|---------|-----------------|
| cielingo basic | `tests/` | 46/51 → 51/51 |
| phase evolution | `tests/` | PASS |
| gravity channel | `tests/` | PASS |
| holonomy | `tests/` | PASS |
| CIEL_CANON | `tests/` | PASS |

## Rules

- NEVER skip a test
- Fix failures, don't delete tests
- After changes: `python3 -m pytest tests/ -v`
