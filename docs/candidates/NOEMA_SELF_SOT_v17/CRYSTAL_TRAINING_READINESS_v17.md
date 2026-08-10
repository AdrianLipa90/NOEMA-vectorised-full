# NOEMA Crystal Training Readiness v17

Status: `PASS_VALIDATION_IMPROVEMENT_V2_CANDIDATE`

This changeset introduces a deterministic stdlib-only feature-delta backend v2.

## Evidence

- fit scope: TRAIN only
- validation relation top-1: **0.4** (v15 baseline: 0.0)
- validation trajectory top-1: **0.5** (v15 baseline: 0.0)
- TEST: **sealed / not evaluated**
- relation features: `RELATIONAL_SEMANTIC` SparseLexical64 delta
- trajectory features: `STRUCTURAL` lane-affinity delta only
- reconstruction: unchanged / not calibrated
- candidate pool for trajectory validation: explicitly **transductive within the held-out validation group**

## Boundary

`PASS_VALIDATION_IMPROVEMENT_V2_CANDIDATE` is not a SoT promotion and is not final generalization evidence.
The validation set was used to select/accept this candidate backend. TEST remains reserved for the next gate.
No canonical loss weights are promoted here.

## Next gate

Freeze v17 backend and hyperparameters, execute the single reserved TEST evaluation once, compare against frozen baselines, and promote only if the predeclared test gate passes.
