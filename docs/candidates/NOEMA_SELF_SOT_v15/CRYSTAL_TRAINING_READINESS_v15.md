# NOEMA Crystal training readiness — v15

Status: `REJECT_FIRST_NATIVE_FIT_BACKEND`

The first controlled native fit was executed on TRAIN only. TEST remains sealed.

- seed cards: **42**
- TRAIN examples used for fit: **644**
- fit epoch: **1**
- fitted: **true**
- fit digest: `12b93506c56c6581681caa5bff7c06cee34f4925048c14bf3610f33ebb7c5f3e`
- corpus digest: `9757782f2263701b19318144632645e2668a3103685766bdc599f0802380d6f3`
- calibration receipt: `d92dd4fe7cce7e310b3a04bbe0af835d1f1cc7a6c7efb1ca7c71ec327f54fd31`
- canonical loss weights: **unset**

## Validation metrics

- reconstruction: `NOT_CALIBRATABLE`, score `None`, n=4 — held-out input is an unseen card identity; no semantic feature frame exists yet
- lane_routing: `MEASURED`, score `0.8757936507936508`, n=4 — card-type lane prototype similarity on held-out identities
- relation: `MEASURED`, score `0.0`, n=5 — typed relation top-1 from TRAIN card-type-pair counts
- contradiction: `MEASURED`, score `1.0`, n=6 — negative relation rejection from TRAIN type-pair evidence
- trajectory: `MEASURED`, score `0.0`, n=2 — next-card-type top-1 from TRAIN trajectory counts
- provenance: `HARD_CONSTRAINT`, score `1.0`, n=21 — all validation examples retain provenance refs

Candidate-only objective weights from `score*sqrt(n)` are:

`{'contradiction': 0.5830623235214263, 'lane_routing': 0.4169376764785737, 'relation': 0.0, 'trajectory': 0.0}`

These weights are **not canonical**.

## Verdict

The backend is rejected for promotion. Lane routing and contradiction baselines have signal, but held-out relation and trajectory scores are zero. Reconstruction is not a legitimate grouped-generalization objective with the current unseen-card-ID-only input contract.

Next gate:

`CardFeatureFrame -> richer relational/trajectory backend -> validation > baseline -> only then reopen fitting promotion`.

TEST remains sealed until a backend passes the validation gate.
