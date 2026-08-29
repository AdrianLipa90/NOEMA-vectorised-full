# M9 Validation Receipt — Derived Entrypoint Dependency Bundles

## Scope

Validation target: `feat/relational-function-closure` on top of M8/M7.

M9 derives execution dependency bundles from explicit `[project.scripts]` entrypoints and the exact M8 binding graph.

## Implemented

- exact `module:attribute` entrypoint parsing;
- unique target occurrence resolution;
- no first-match selection for ambiguous targets;
- transitive internal dependency closure per entrypoint;
- exact M8 component membership;
- environment-anchor aggregation;
- pinned external requirement extraction from M8 distribution anchors;
- OPEN debt propagation from any reachable occurrence/binding;
- CLI section `CIELPC_ENTRYPOINT_DEPENDENCY_BUNDLES_V1` with `thresholds=[]`;
- no automatic package rewrite or file relocation.

## Regression cases specified

1. exact entrypoint syntax resolves to one qualified target;
2. `[project.scripts]` declarations are loaded deterministically;
3. `main -> helper -> leaf -> numpy.asarray` derives the exact 3-occurrence closure and `numpy==2.0.0`;
4. OPEN relational debt in a reachable child makes the bundle OPEN;
5. missing target stays UNRESOLVED;
6. duplicate exact targets stay AMBIGUOUS, with no first-match choice;
7. invalid target syntax stays INVALID;
8. CLI emits bundle schema, basis, authority, and threshold-free payload.

## Independent isolated-core execution

A separate Python harness exercised the M9 bundle rules outside GitHub Actions.

Observed PASS cases:

- transitive closure from `main` contained exactly `main`, `helper`, and `leaf`;
- the only derived external requirement was `numpy==2.0.0` from the reachable environment anchor;
- no blockers were produced for the fully closed graph;
- OPEN child/binding debt propagated to the entrypoint bundle.

Verdict: **M9 ISOLATED BUNDLE LOGIC = PASS**.

This does not establish a full repository test-suite PASS.

## GitHub Actions evidence

Validated code/documentation head before this receipt: `e2b8a951b9235988fe653370a99d0eda84f68171`.

Workflow:

- workflow: `ci`
- run id: `31473873073`
- run number: `255`
- run conclusion: `failure`
- job: `all-in-one-quality-gate`
- job id: `93723009167`
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

## Known debt

- relative imports are not yet fully package-qualified by the M7 structural scanner;
- recursive SCCs remain OPEN pending cycle identity proof;
- bare/global call bindings remain OPEN without a complete runtime/global binding table;
- exact bundle identity/deduplication is not yet implemented;
- generation of installable manifests from CLOSED bundles remains read-only future work.

These debts can cause false OPEN/UNKNOWN. They are not permitted to create false CLOSED authority.

## Current verdict

- implementation: **IMPLEMENTED CANDIDATE**
- tests: **TEST-SPECIFIED**
- isolated M9 bundle logic: **PASS**
- full repository CI: **UNKNOWN / INFRA_BLOCKED**
- CANON promotion: **NO**
- NOEMA CURRENT update: **NO**
- Actuator: **NO**
- automatic package/dependency rewrite: **NO**
