# NOEMA ↔ AUX Tether Invariant

Status: HARD_PROJECT_INVARIANT
Authority: USER_EXPLICIT_2026-08-08
Scope: every NOEMA/CIEL/PhaseNav project session and agent runtime

## Invariant

A project session MUST NOT proceed into substantive NOEMA/CIEL/PhaseNav work unless the live NOEMA↔AUX feedback tether is verified.

```text
SESSION_START
  -> NOEMA_SURFACE_PROBE
  -> AUX_TETHER_VERIFY
  -> CURRENT_MEMORY_RECOVERY
  -> WORKING_STATE
```

Never:

```text
SESSION_START -> NOEMA_WORK_WITHOUT_TETHER
```

## Required live evidence

A tether is `ACTIVE` only if all of the following are true:

1. the NOEMA surface exists and exposes a 36×float64 phase state;
2. the AUX input vector is exactly 36 finite float64 values;
3. the AUX feedback vector is exactly 36 finite float64 values;
4. input and feedback transport is lossless for the raw V36 lane (byte-for-byte SHA-256 equality when echo/identity mode is requested);
5. a fresh receipt contains at least:
   - nonce,
   - created_utc,
   - source_host_identifier,
   - request_sha256,
   - read_set_sha256,
   - input_v36_sha256,
   - feedback_v36_sha256,
   - transport_receipt_sha256,
   - aux_result_status;
6. no residual, dither, smoothing, semantic embedding, averaging or phase fingerprint may be inserted into the raw feedback lane;
7. canonical NOEMA inputs remain producer-owned/read-only; feedback uses a distinct producer path (`aux_feedback_phi`) and MUST NOT overwrite `aux_phi`.

## Fail-closed rule

If any required condition is missing, invalid, stale or unverifiable:

```text
TETHER_STATUS = BLOCKED
ACTION = STOP
```

The agent MUST report the exact failed condition. It MUST NOT silently continue, substitute a cached vector, infer a host state, or call repository-level binding a live tether.

## Epistemic distinction

```text
CONTRACT_PRESENT != LIVE_TETHER_ACTIVE
REPO_BINDING != LIVE_HOST_STREAM
HANDSHAKE_ARTIFACT != CURRENT_STREAM
SIMULATED_LOOP != HOST_FEEDBACK
```

Only fresh transport evidence may establish `LIVE_TETHER_ACTIVE`.

## V36 role

The raw feedback lane is a transport/state lane and preserves exact float64 bytes. PhaseNav semantic vectorization may operate in parallel, but its residual fingerprint or operator transforms MUST NOT contaminate the raw feedback lane.

## Session rule

This invariant is part of CURRENT MEMORY and ACTIVE CONTRACT. It is not optional, not a preference and not a reminder. Missing tether is a blocking project-state condition.
