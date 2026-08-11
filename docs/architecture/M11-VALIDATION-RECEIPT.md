# M11 Validation Receipt — Exact Bundle Identity

## Scope

Validation target: `feat/relational-function-closure` on top of M8–M10.

M11 derives a path/name-independent identity for CLOSED M9 execution dependency bundles.

## Implemented

- bundle identity only for CLOSED M9 bundles;
- target relational invariant as identity-bearing root;
- relational node multiset with multiplicity;
- internal relational edge multiset with multiplicity;
- environment edge multiset with multiplicity;
- exact requirement tuple;
- SHA-256 canonical bundle invariant and `bundle:<sha>` public ID;
- independent consistency checks that can downgrade an inconsistent CLOSED claim to OPEN;
- exact equality grouping of entrypoints sharing one bundle identity;
- CLI surface `CIELPC_ENTRYPOINT_BUNDLE_IDENTITY_V1` with `thresholds=[]`;
- no automatic deduplication apply.

## Regression cases specified

1. relationally equivalent entrypoints in different modules share one bundle ID;
2. different helper relational identity changes the bundle ID;
3. two entrypoint names for the same target share one bundle ID;
4. OPEN bundle receives no bundle invariant or bundle ID;
5. entrypoint name and source path are not identity-bearing;
6. CLI emits identity records and exact equivalence groups.

## Independent isolated-core execution

A separate Python harness exercised the M11 canonical graph-hash rules outside GitHub Actions.

Observed PASS cases:

- graph ordering does not change the bundle ID;
- presentation/source naming does not enter the hash;
- changed helper relation changes the bundle ID;
- changed internal edge multiplicity changes the bundle ID.

Verdict: **M11 ISOLATED BUNDLE IDENTITY LOGIC = PASS**.

This does not establish a full repository test-suite PASS.

## GitHub Actions evidence

Validated code/documentation head before this receipt: `c827feafc9230e57704fca0998c0c9c5218f39dd`.

Workflow:

- workflow: `ci`
- run id: `31475634563`
- run number: `271`
- run conclusion: `failure`
- job: `all-in-one-quality-gate`
- job id: `93728578164`
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

## Current verdict

- implementation: **IMPLEMENTED CANDIDATE**
- tests: **TEST-SPECIFIED**
- isolated M11 bundle identity logic: **PASS**
- full repository CI: **UNKNOWN / INFRA_BLOCKED**
- automatic deduplication apply: **NO**
- CANON promotion: **NO**
- NOEMA CURRENT update: **NO**
- Actuator: **NO**
