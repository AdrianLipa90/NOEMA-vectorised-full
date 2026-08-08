# NOEMA Session Autostart v1 — ACTIVE only

This changeset removes `PARTIAL` as a usable project state.

## Single entrypoint

```text
python3 scripts/noema_session_autostart.py
```

Persistent locations are explicit configuration, not guessed paths:

- `NOEMA_LIBRARY_ROOT`
- `NOEMA_SURFACE_FALLBACK_ROOT`
- `NOEMA_RUNTIME_TETHER_ROOT`
- optional `NOEMA_AUX_STATE_FILE` (otherwise `${NOEMA_RUNTIME_TETHER_ROOT}/aux/self_state.npy`)
- optional `NOEMA_GEOMETRY_ROOT` when `ciel_geometry` is not already importable
- optional `NOEMA_SURFACE_ROOT` (default `/dev/shm/ciel_noema`)
- optional `NOEMA_CIEL_SOCKET` (default `/run/user/1000/noema/ciel_headless.sock`)

Missing required persistent paths returns `BLOCKED`; no repository/cache/RAM fallback is used as persistent truth.

## Boot topology

```text
persistent memory
  -> /dev/shm projection
  -> AUX input producer / aux_phi
  -> native NOEMA surface / phi
  -> distinct raw identity-feedback producer / aux_feedback_phi
  -> fresh transport receipt
  -> VERIFIED session startpoint
  -> hard tether guard
  -> fresh receipt/liveness guard
  -> ACTIVE
```

Any failed condition yields `BLOCKED` and `working_state_allowed=false`.

## Ownership

The persistent memory store captures only files present in its own projection marker. Producer-owned siblings such as `aux_phi` are not implicitly imported or captured.

`aux_phi` is input-producer owned. `aux_feedback_phi` is written on a distinct feedback path and never overwrites `aux_phi`.

The current raw feedback mode is explicit `identity_echo`, permitted by the hard tether contract. Its PASS condition is byte-for-byte SHA-256 equality between input and feedback, together with a fresh live receipt and running producer PIDs.

## Product boundary

Repository code can implement and validate the project/runtime entrypoint and local lifecycle hooks. It cannot mutate ChatGPT account-global lifecycle behavior. Therefore the project session contract must invoke/enforce this entrypoint; if it is not invoked or cannot return `ACTIVE`, substantive NOEMA/CIEL/PhaseNav work remains blocked.

See `VALIDATION_RECEIPT.json` for the destructive cold-start test and exact execution boundary.
