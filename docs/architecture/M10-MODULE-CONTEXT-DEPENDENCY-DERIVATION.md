# M10 — Module-Context Dependency Derivation

## Status

IMPLEMENTED CANDIDATE. Read-only refinement of M8/M9. No source rewrite, package rewrite, CANON promotion, CURRENT update, or Actuator action.

## Why M10 exists

M7 intentionally derives a callable structural fingerprint without requiring full module/runtime context. That means relative-import syntax can be structurally observed without knowing its package-qualified destination.

For example:

```python
# pkg/main.py
from .helper import helper

def main():
    return helper()
```

The structural layer may observe the call relation as `helper.helper`. The package context derives the exact source-level target `pkg.helper.helper`.

M10 supplies that missing context to M8 without rewriting the M7 observation.

## Invariant

```text
observation != contextual resolution
```

A binding stores both:

```text
observed_dependency_symbol
resolved dependency_symbol
```

so contextual normalization never erases provenance.

## Exact relative-import derivation

Python defines relative imports from:

- the `ImportFrom.level` value;
- the source module's package;
- the imported module/name.

M10 uses those exact syntax facts. No search ranking or similarity matching is involved.

Examples:

```text
pkg.main + from .helper import helper
  -> pkg.helper.helper

pkg.sub.main + from ..helper import helper
  -> pkg.helper.helper

pkg.main + from . import helper as h + h.helper()
  -> pkg.helper.helper
```

## Lexical scope

M10 derives relative-import rewrite maps per qualified function.

- module-level relative imports are inherited by functions;
- function-local relative imports override module-level names in that function scope;
- nested functions inherit enclosing function relative-import aliases;
- class namespace imports are not treated as lexical parents of methods;
- an outer function binding can still be inherited through a nested class by a method closure.

Both M7's normalized representation and the local alias spelling are retained when needed so nested closures can resolve the same imported object.

## Full-AST dependency manifest

The M7 dependency manifest is preserved as legacy structural evidence. M10 derives the dependency manifest used by the M8/M9 CLI from **all import statements in the AST**, including imports inside functions.

This prevents a runtime-only import from disappearing merely because it is not module-level.

Observed import roots are partitioned exactly into:

- stdlib roots from `sys.stdlib_module_names`;
- local roots proven by Python modules present under the scanned root;
- remaining roots as external candidates.

Relative imports are package-qualified before their root is classified.

## Unresolved relative imports

If source context cannot legally resolve a relative import, M10 records explicit debt in:

`unresolved_relative_imports`.

No guessed absolute module name is generated.

## M8 integration

`derive_function_topology` accepts a per-function `dependency_rewrites` map.

The binder applies only exact prefix rewrites, longest exact prefix first. It then performs the ordinary M8 exact internal/environment/ambiguous/unresolved resolution.

A rewrite may therefore change:

```text
helper.helper -> pkg.helper.helper
```

but it cannot choose a merely similar symbol.

## Static closure versus live runtime

M10 derives static Python source/module relations. It does not prove that a mutable module global keeps the same live value forever.

Therefore:

```text
M10 exact source binding != live runtime namespace proof
```

The M8/M9 authority remains read-only and non-CANON. A later runtime namespace probe may validate live bindings separately.

## CLI

The report adds:

```text
module_context_dependencies.schema = CIELPC_MODULE_CONTEXT_DEPENDENCIES_V1
module_context_dependencies.thresholds = []
```

and includes:

- non-empty function dependency rewrites;
- unresolved relative-import debt;
- read-only authority marker.

M8 binding records additionally expose `observed_dependency_symbol` beside the resolved dependency symbol.

## Next derivation

M10 removes a syntactic source of false OPEN results. The next non-arbitrary compression step is an exact identity for CLOSED M9 execution bundles so identical dependency closures can be deduplicated by equality rather than by package naming or similarity.
