# M7 — Dependency Derivation Direction

The original task was to build dependency packages. M7 reverses the usual
workflow: code is scanned first and dependency declarations become claims to
validate against observed relations.

```text
functions
  -> explicit calls/imports
  -> local/external relation split
  -> dependency graph
  -> distribution resolver
  -> generated dependency package
```

## Implemented resolver

`dependency_resolver.py` maps observed external import roots through explicit
Python package metadata (`importlib.metadata.packages_distributions()`). The
resolver has only three outcomes:

```text
0 distribution candidates -> UNRESOLVED
1 distribution candidate  -> RESOLVED
>1 candidates              -> AMBIGUOUS
```

There is no first-match policy. Candidate ordering never grants authority.

When exactly one distribution is resolved, the runtime metadata is queried for
an installed version. If present, the generated requirement is pinned as
`distribution==version`; if version metadata is unavailable, only the unique
distribution name can be emitted.

The derived package contains requirements only for `RESOLVED` imports. Every
`AMBIGUOUS` or `UNRESOLVED` import is listed in `blocked_imports` instead of
being guessed.

## Provenance layers

Current resolver evidence comes from the validated Python runtime metadata.
Additional resolvers may later add independent evidence from:

- lock files,
- installed wheel metadata,
- declared project metadata used only as a candidate/consistency claim.

If evidence sources disagree, the dependency must become conflict/debt rather
than silently selecting one source.

## Remaining derivation

```text
FunctionIdentity
  -> local call graph
  -> transitive identity closure
  -> distribution evidence merge
  -> declared-vs-derived dependency audit
  -> generated dependency package
  -> module boundary proposals
  -> MegaSorter sectorization
```
