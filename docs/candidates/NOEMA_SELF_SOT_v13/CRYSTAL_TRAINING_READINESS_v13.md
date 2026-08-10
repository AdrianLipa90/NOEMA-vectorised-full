# NOEMA Crystal Training Readiness — v13

Status: `PASS_CHANGESET_F_BENCHMARK_AND_NATIVE_TOPOLOGY_PREP_NOT_TRAINED`

This candidate changeset adds the first deterministic seed benchmark harness and a zero-dependency native sparse relational crystal topology.

## New gates

1. `CrystalSeedBenchmark` checks provenance coverage, exact example-ID split leakage, cross-split card-reference overlap, and two deliberately weak held-out baselines.
2. The report explicitly labels itself a **seed smoke benchmark**, not generalization evidence.
3. `NativeCrystalTopologyBuilder` materializes identity-bearing nodes and provenance-backed relation/trajectory couplings with all trainable weights initialized to `0.0`.
4. `CrystalTrainingPlanner` refuses fitting while the canonical seed is below 32 validated cards.

## Invariants

- no LLM required by the native topology;
- no third-party runtime dependency;
- `similarity != identity`;
- training topology does not become Memory Home;
- benchmark PASS does not imply scientific or linguistic generalization;
- no training starts without an explicit later gate.

## Verification

- full regression: `115/115 PASS`;
- dependency audit: `PASS`;
- third-party dependencies in candidate core: `0`;
- deterministic rebuild: `PASS`;
- release SHA256: `f9e46e6cc33e0d533a104f141b123ca4189015a261ce2f86fca63e8da04f533f`.

## Epistemic boundary

The v12 dry-run stores card/edge aggregates but not all 45 serialized `CrystalTrainingExample` payloads. Therefore the exact v12 7-card benchmark was **not replayed** from serialized examples in v13; no benchmark result is fabricated. The benchmark harness itself was validated deterministically on a synthetic fixture.

## Next gate

Expand the canonical seed to at least 32 validated cards, serialize the complete corpus, and run a grouped holdout benchmark that prevents card-identity leakage across TRAIN/VALIDATION/TEST before enabling fitting.
