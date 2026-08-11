# M8 Validation Receipt — Relational Function Identity Closure

## Scope

Validation target: `feat/relational-function-closure` against `master` after M7 merge `3562a33f905ec17971946eeec4bda4fe725103eb`.

## Implemented

- structural identity explicitly separated from relational identity;
- concrete callable occurrence keys;
- exact internal binding resolution without first-match selection;
- versioned imported environment anchors;
- bare global/builtin names fail closed without a global binding table;
- occurrence call graph;
- exact SCC derivation and condensation DAG;
- acyclic relational hash closure;
- recursive SCCs remain OPEN debt;
- NOEMA structural/relational bridges;
- existing function-identity CLI extended with a threshold-free relational-closure section.

## Regression cases specified

1. structurally identical callers of different module-local helpers must **not** become aliases;
2. true copies with relationally identical helpers must become CLOSED aliases;
3. bare `len()` remains OPEN until global-shadowing absence can be derived;
4. explicit stdlib import may close through runtime identity;
5. pinned external distribution may close through distribution identity;
6. unversioned external distribution remains OPEN;
7. dynamic/local callable parameter remains OPEN;
8. recursive SCC remains OPEN with cycle debt;
9. same qualified symbol with different CLOSED relational identity is CONFLICT;
10. NOEMA structural bridge cannot claim relational closure;
11. CLOSED relational aliases share NOEMA relational identity without fabricated PNV36;
12. OPEN relational identities remain occurrence-specific;
13. CLI payload exposes exact bindings, components, condensation edges, and `thresholds=[]`.

## Independent isolated-core execution

A separate Python harness mirroring the committed M8 closure algorithm was executed outside GitHub Actions. It exercised the relational core without depending on the repository workflow infrastructure.

Observed PASS cases:

- false structural alias with different helper bindings -> relational invariants differ;
- true copy with identical helper closure -> relational ALIAS;
- bare unqualified `len` -> OPEN;
- explicit dotted stdlib binding -> CLOSED;
- version-pinned external distribution binding -> CLOSED;
- self-recursive internal component -> OPEN and recursive SCC detected.

Verdict: **M8 ISOLATED CORE LOGIC = PASS**.

This does **not** establish a full repository test-suite PASS and is not a substitute for repository-wide execution.

## GitHub Actions evidence

PR #21 head at first validation: `4a110fe895ee8d0dd70640eb5d48e5eb9c050d3e`.

Workflow:

- workflow: `ci`
- run id: `31472737661`
- run number: `249`
- run conclusion: `failure`
- job: `all-in-one-quality-gate`
- job id: `93719454035`
- job conclusion: `failure`
- job `logs_url`: `null`
- job embedded `steps`: `null`
- direct step lookup: `[]`
- direct job-log download: GitHub API `404 BlobNotFound`

No executable setup, compile, pytest, lint, build, or assertion step result is observable. Therefore the workflow conclusion cannot be attributed to the code.

Classification:

- repository workflow execution: **INFRA_BLOCKED / NO STEP EVIDENCE**
- repository code PASS: **NOT ESTABLISHED**
- repository code FAIL: **NOT ESTABLISHED**

## Current verdict

- implementation: **IMPLEMENTED CANDIDATE**
- tests: **TEST-SPECIFIED**
- isolated M8 core logic: **PASS**
- full repository CI: **UNKNOWN / INFRA_BLOCKED**
- CANON promotion: **NO**
- NOEMA CURRENT update: **NO**
- Actuator: **NO**
- automatic module/package rewrite: **NO**

A workflow status without executable step evidence must not be interpreted as a code PASS or code FAIL.
