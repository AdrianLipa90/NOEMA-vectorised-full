# M7 — Function Identity Kernel

Status: **IMPLEMENTED CANDIDATE / VALIDATION PENDING**

## Purpose

CIELPC must not treat a function name, file path, module placement, or manually
assigned role as the identity of a function. Those are representations.

M7 introduces a conservative derived identity:

```text
Python source
  -> lexical scope
  -> alpha-normalized callable AST
  -> signature shape
  -> explicit call/import relations
  -> canonical JSON payload
  -> SHA-256 invariant
```

No similarity threshold, learned weight, hand-written semantic category, or
folder name participates in the identity proof.

## Identity relation

For function observations `f` and `g`:

```text
same qualified symbol + same invariant  -> SAME_IDENTITY
different symbol + same invariant       -> ALIAS
same qualified symbol + different hash  -> CONFLICT
otherwise                               -> UNKNOWN
```

`UNKNOWN` is a required state. General program equivalence is not claimed by a
static scanner.

## What is identity-bearing

The normalized callable AST preserves operations, constants, control flow,
default values, decorators, annotations, imports and external call structure.
Local parameter and local-variable spelling is canonicalized. Function name,
module name and source path are excluded from the invariant itself.

Import aliases are canonicalized to imported targets (`np.asarray` becomes
`numpy.asarray`). Scope is local: an import alias in one function cannot leak
into another function's identity.

Conservative rule: if a Python construct cannot yet be safely normalized, M7
prefers a false UNKNOWN over a false ALIAS.

## NOEMA bridge

A derived identity becomes a `RelationalState` with:

```text
identity        = function:<invariant_sha256>
kind            = function_identity
relations       = depends_on:<observed-call>
provenance      = source:<source-path>
authority       = DERIVED_STATIC_NO_AUTHORITY
phase36         = None
phase_space     = UNKNOWN
phase_projection= UNKNOWN_UNTIL_DERIVED
```

M7 deliberately does **not** hash a function into a fake 36D PhaseNav vector.
Until a justified projection exists, PhaseNav must see missing coordinates and
HOLD any operation that requires them.

## Dependency derivation

The repository scanner gathers observed Python import roots and partitions them
using runtime facts:

```text
observed imports
  -> Python stdlib names
  -> repository-local roots
  -> external import roots
```

This reverses the usual dependency workflow. A declared package list is no
longer the primary source of truth; it becomes a claim to compare against the
dependencies derived from code.

Distribution-name resolution (for cases such as import `yaml` -> distribution
`PyYAML`) is intentionally not guessed in M7. It requires an explicit resolver
from package metadata/lock data and remains the next layer.

## Non-goals

M7 does not prove mathematical equivalence of arbitrary programs. It does not
infer runtime side effects that are invisible to syntax, execute scanned code,
assign mutation authority, promote CANON, or create PhaseNav coordinates.

## Next derivation

```text
FunctionIdentity
  -> dependency graph
  -> transitive identity closure
  -> import-name/distribution resolver
  -> derived dependency package
  -> module boundary proposals
  -> MegaSorter sectorization
```

The key invariant is:

> Representation may change while function identity is preserved only when the
> derived invariant is preserved.
