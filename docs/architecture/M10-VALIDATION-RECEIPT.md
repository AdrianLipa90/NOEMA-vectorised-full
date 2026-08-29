# M10 Validation Receipt — Module-Context Dependency Derivation

## Scope

Validation target: `feat/relational-function-closure` on top of M8/M9.

M10 adds exact Python module/package context to dependency derivation while preserving the original M7 structural observation.

## Implemented

- package/module context derivation from source paths, including `src/` layout and `__init__.py` package modules;
- exact `ImportFrom.level` relative-import resolution;
- per-function dependency rewrite maps;
- preservation of both observed and resolved dependency symbols;
- inheritance of relative-import aliases into nested function closures;
- class namespace not treated as a lexical parent of methods;
- full-AST import-root collection, including imports inside functions;
- exact stdlib/local/external root partitioning;
- explicit unresolved-relative-import debt;
- M8 exact-prefix rewrite integration before binding resolution;
- CLI surface `CIELPC_MODULE_CONTEXT_DEPENDENCIES_V1` with `thresholds=[]`.

## Regression cases specified

1. `from .helper import helper` in `pkg.main` resolves `helper.helper -> pkg.helper.helper`;
2. M8 then resolves that target as the exact internal function occurrence;
3. nested functions inherit an enclosing function's relative-import alias;
4. imports inside functions enter the dependency manifest;
5. unresolvable relative imports produce explicit debt;
6. absolute imports create no relative rewrite;
7. CLI preserves `observed_dependency_symbol` and resolved `dependency_symbol` separately;
8. a relative-import entrypoint bundle closes over the actual package helper rather than a guessed/false external name.

## Independent isolated-core execution

A separate Python harness exercised the new M10 rules outside GitHub Actions.

Observed PASS cases:

- `.helper` resolved from package `pkg`;
- `..helper` resolved from package `pkg.sub`;
- `from . import helper as h` preserved the local alias and resolved the package target;
- longest exact-prefix rewrite selected the most specific observed symbol;
- import discovery traversed into a function-local `import numpy` statement.

Verdict: **M10 ISOLATED MODULE-CONTEXT LOGIC = PASS**.

This does not establish a full repository test-suite PASS.

## GitHub Actions evidence

Validated code/documentation head before this receipt: `42042f621b9a2062d6227728540f4d5a377b9d4d`.

Workflow:

- workflow: `ci`
- run id: `31475145534`
- run number: `265`
- run conclusion: `failure`
- job: `all-in-one-quality-gate`
- job id: `93727013287`
- job conclusion: `failure`
- job `logs_url`: `null`
- job embedded `steps`: `null`
- direct step lookup: `[]`
- direct job-log download: GitHub API `404 BlobNotFound`

No executable setup, compile, pytest, lint, build, or assertion step result is observable.

Classification:

- repository workflow execution: **INFRA_BLOCKED / NO STEP EVIDENCE**
- repository code PASS: **NOT ESTABLISHED**
- repository code FAIL: **NOT ESTABLISHED**

## Epistemic boundary

M10 proves source/module-context relations. It does not prove that a live mutable Python global namespace remains unchanged after import.

Therefore:

`CLOSED_STATIC_SOURCE_RELATION != VERIFIED_LIVE_RUNTIME_BINDING`.

Live binding claims require a separate runtime namespace snapshot/probe and receipt.

## Current verdict

- implementation: **IMPLEMENTED CANDIDATE**
- tests: **TEST-SPECIFIED**
- isolated M10 module-context logic: **PASS**
- full repository CI: **UNKNOWN / INFRA_BLOCKED**
- CANON promotion: **NO**
- NOEMA CURRENT update: **NO**
- Actuator: **NO**
- automatic source/package rewrite: **NO**
