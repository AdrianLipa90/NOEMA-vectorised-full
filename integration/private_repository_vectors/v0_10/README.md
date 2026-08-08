# NOEMA Private Repository Tree/Blob Vectorization v0.10

This append-only layer records the next deterministic descent after the complete v0.9 private repository-head snapshot.

PhaseNav canonical scanner parent:

`5a4a06eec8611dc8f890516ea457926d069e6612`

Hard canon `1.5.0`, package `0.8.0`, scanner `0.10.0`.

## What is complete

The private repository-head layer is complete for the frozen snapshot: 40 private repositories inventoried, 39 real heads vectorized, one archived empty repository left without an invented vector.

The scanner that descends a frozen checkout into commit/tree/blob objects is implemented and focused-validated. It discovers objects through Git itself, not through a hand-picked path list.

## What is not complete

The full 39-checkout tree/blob execution is currently `NOT_RUN`. Current connector access does not expose the private repositories as local Git object databases and does not provide recursive private tree listing. This missing execution is not replaced by filename heuristics.

## Canonical rules

- commit/tree/blob identity comes from the native Git object digest;
- paths are occurrence/localizer metadata only;
- duplicate blobs share one vector;
- pure rename preserves the blob vector;
- content change forces a new blob digest/vector;
- only native `commit -> root tree` and `tree -> child` edges are emitted at this layer;
- edge geometry is calculated from endpoint vectors;
- relation labels do not get pseudo-object vectors;
- moving-head drift fails closed;
- a partial scan cannot claim complete private snapshot status.

NOEMA stores these states as provenance. It does not promote semantic, mathematical or physical claims.