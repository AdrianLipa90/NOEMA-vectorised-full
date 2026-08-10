# M6 Validation Receipt — Canonical NOEMA

Branch: `arch/pnv-gate-fabric-consolidation`

PR: `#19`

Validated head observed: `1b517edbbf922e58b590e4120136036b04bdba46`

Status: **INFRA_BLOCKED / CODE_VERDICT_UNKNOWN**

## Cross-repo fixture identity

Shared fixture:

`contracts/fixtures/noema_megasorter_roundtrip_v1.json`

Git blob SHA on canonical NOEMA feature branch:

`2428fb1701eb048d665a08056539e956832322d1`

Git blob SHA observed on MegaSorter feature branch:

`2428fb1701eb048d665a08056539e956832322d1`

The golden round-trip fixture is therefore byte-identical across both feature branches.

Transport descriptor SHA-256:

`b490f9ec27879db1fd7ab83473a670a8e49190ca8bf6bc8d1595da2195654f7b`

Expected proposal batch SHA-256 embedded in the fixture:

`e74866ad8acc4b4457cef1821e224c446d73bef61c6415c792bf5c0373aef37b`

These identities establish contract/fixture consistency only. They do not establish execution PASS, evidence truth or mutation authority.

## GitHub Actions observation

```text
run_id      = 31369090960
workflow    = ci
status      = completed
conclusion  = failure
```

Initial job:

```text
all-in-one-quality-gate  job_id=93393821863  conclusion=failure  logs_url=null  steps=null
```

Direct step lookup returned:

```text
[]
```

Direct job-log download for `93393821863` returned `404 BlobNotFound`; no log blob exists for the job.

## Controlled rerun

A single controlled rerun of `all-in-one-quality-gate` was requested through the GitHub Actions API and accepted (`success=true`). The same workflow run then produced a fresh job identity:

```text
all-in-one-quality-gate  job_id=93395203609  conclusion=failure  logs_url=null  steps=null
```

The controlled rerun reproduced the same failure mode before any executable workflow-step record became available.

This is strong evidence that the observed Actions failure occurs before repository code tests/build steps are recorded. It does not establish the exact account/infrastructure cause.

No checkout, setup, test, build or runtime step result is exposed in either attempt.

Classification:

```text
M6 code                 = IMPLEMENTED
M6 tests                = TEST-SPECIFIED
golden fixture identity = VERIFIED BY GIT BLOB SHA
workflow execution      = INFRA_BLOCKED / NO STEP EVIDENCE
controlled rerun        = SAME PRE-STEP FAILURE REPRODUCED
code PASS               = NOT ESTABLISHED
code FAIL               = NOT ESTABLISHED
runtime validation      = UNKNOWN
```

## Promotion decision

Keep PR #19 draft.

No live Actuator side effect, no SoT promotion and no merge to `master` are justified by this run.
