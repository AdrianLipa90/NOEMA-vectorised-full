# M12 Validation Receipt — Content-Addressed Bundle Manifests

## Scope

Validation target: `feat/relational-function-closure` on top of M8–M11.

M12 derives exactly one read-only manifest per unique M11 bundle identity group.

## Implemented

- one manifest per unique exact M11 bundle group;
- entrypoint names retained as provenance but excluded from manifest identity;
- exact sorted/deduplicated pinned requirements;
- deterministic requirements text;
- SHA-256 of requirements payload;
- declared `requires-python` included as an identity-bearing runtime contract;
- canonical manifest invariant under schema `CIELPC_DERIVED_BUNDLE_MANIFEST_V1`;
- public content address `manifest:<sha256>`;
- CLI surface `bundle_manifests` with `thresholds=[]`;
- explicit authority `DERIVED_READ_ONLY_NO_INSTALL_AUTHORITY`;
- no install/apply path.

## Regression cases specified

1. one M11 equivalence group derives exactly one manifest;
2. entrypoint rename does not change manifest identity;
3. changing `requires-python` changes manifest identity;
4. requirements rendering is deterministic and deduplicated;
5. requirements payload SHA-256 is explicit;
6. empty requirements render to empty bytes with the standard SHA-256 of the empty payload;
7. `requires-python` is loaded exactly from `pyproject.toml`;
8. CLI manifest record points to the exact M11 bundle ID and remains read-only;
9. relative-import package closure can derive a bundle identity and then a manifest without source-path identity leakage.

## Independent isolated-core execution

A separate Python harness exercised the committed M12 manifest rules outside GitHub Actions.

Observed PASS cases:

- renaming an entrypoint while holding bundle identity, requirements, and `requires-python` constant left the manifest ID unchanged;
- changing `requires-python` changed the manifest ID;
- changing the bundle ID changed the manifest ID;
- requirements were canonically sorted and deduplicated;
- requirements SHA-256 matched the rendered bytes;
- an empty requirements payload hashed to `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Verdict: **M12 ISOLATED MANIFEST LOGIC = PASS**.

This does not establish a full repository test-suite PASS.

## GitHub Actions evidence

Validated M12 code/documentation head before this receipt: `912b868f4123930aab5249bf4d81a73191d341d5`.

Workflow:

- workflow: `ci`
- run id: `31476129944`
- run number: `277`
- run conclusion: `failure`
- job: `all-in-one-quality-gate`
- job id: `93730152537`
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

## Boundary to actuation

M12 closes the current derivation chain:

`source -> structural function -> static relational function -> module context -> entrypoint closure -> bundle identity -> content-addressed manifest`.

The next step is an actuation-policy problem rather than another dependency-classification problem. Materialization or installation must require a separate Gate/Doctor/Return authorization path.

## Current verdict

- implementation: **IMPLEMENTED CANDIDATE**
- tests: **TEST-SPECIFIED**
- isolated M12 manifest logic: **PASS**
- full repository CI: **UNKNOWN / INFRA_BLOCKED**
- manifest installation: **NO**
- automatic dependency rewrite: **NO**
- CANON promotion: **NO**
- NOEMA CURRENT update: **NO**
- Actuator: **NO**
