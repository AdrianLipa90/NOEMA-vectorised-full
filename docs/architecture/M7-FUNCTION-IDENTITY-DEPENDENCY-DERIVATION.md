# M7 — Dependency Derivation Direction

The original task was to build dependency packages. M7 reverses the usual
workflow: code is scanned first and dependency declarations become claims to
validate against observed relations.

```text
functions
  -> explicit calls/imports
  -> local/external relation split
  -> dependency graph
  -> transitive closure
  -> distribution resolver
  -> generated dependency package
```

The current slice derives import roots only. It deliberately does not guess
Python distribution names when import names differ from package names.

Next implementation should add a resolver with explicit provenance from one or
more of:

- `importlib.metadata.packages_distributions()` on the validated runtime,
- lock files,
- installed wheel metadata,
- declared project metadata used only as a candidate mapping.

If multiple distributions can provide one import, the result remains
ambiguous/UNKNOWN until resolved. No first-match policy is allowed.
