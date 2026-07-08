---
name: canon-audit
priority: 1
description: >
  >
---
# Canon Audit

## Wzorce sabotażu

| Marker | Detection |
|--------|-----------|
| `except:pass` | `grep -r "except.*:" --include="*.py" \| grep -v "Exception\|Error\|Stop"` |
| `.incoming_*` | pytest collecting disabled tests |
| `raise NotImplementedError` | kod niegotowy |
| cross-import = 0 | `grep -r "from ciel_omega\|import ciel_omega" cielingo/src/ --include="*.py"` |

## Fix protocol

1. `document` → rejestruj disconnected islands
2. `fix __init__` → dodaj importy
3. `restore` → przywróć usunięte moduły
4. `bridge` → dodaj cross-importy
5. `verify` → pytest
6. `tick` → zapisz w AGENTS.md

## Użycie

```bash
grep -rn "except.*:" src/ --include="*.py" | grep -v "Exception\|Error\|Stop"
grep -rn "raise NotImplementedError" src/ --include="*.py"
```
