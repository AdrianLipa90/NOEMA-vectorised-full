# NOEMA Crystal training readiness — v14

Status: `PASS_GROUPED_GENERALIZATION_GATE`

The canonical-source seed has crossed the 32-card floor without enabling training.

- validated seed cards: **42**
- typed edges: **38**
- grouped corpus examples: **684**
- card groups: TRAIN **34**, VALIDATION **4**, TEST **4**
- example groups: TRAIN **656**, VALIDATION **14**, TEST **14**
- provenance coverage: **100.0%**
- card identity leakage across splits: **0**
- native topology nodes: **42**
- native topology couplings: **45**
- topology fitted: **false**
- epoch: **0**
- canonical loss weights: **unset**

Corpus digest: `ae113eec9082b3a2fc0805927bbcef51e215eb312334e046ac095a2bc2e30fce`

Grouped benchmark receipt: `97225c539f1f33f89ab893bb403da07baef5788567157db6a635cc78a2a0c20e`

Topology digest: `3485609b47bc96a01b1281bb896a68872cf61ecd6cc00c24246fefc6a87b9179`

## Gate interpretation

This is a **data-integrity and leakage gate**, not evidence that the crystal generalizes.
The next stage is backend/loss calibration on the frozen grouped split, followed by the first deliberately authorized fit.

## Preserved invariants

1. similarity != identity
2. Memory Home admission != source generation
3. CIELingoPhase36 != NOEMA Vector36
4. language proposal != identity authority
5. grouped holdout contains no card identity shared between TRAIN/VALIDATION/TEST
6. no training starts implicitly
