# NOEMA Persistent Surface Sync v0.2.0

Canonical topology:

- `{KANON}/noema/library/surface_store/canonical` — persistent Source of Truth.
- `{KANON}/runtime/surface-fallback` — derived last-known-good disk mirror.
- `/dev/shm/ciel_noema` — volatile high-speed projection.

The volatile surface is never authoritative.

## Transaction model

`project` copies the current persistent generation to `/dev/shm` and writes a generation/SHA projection marker.

`capture` accepts changed canonical inputs from `/dev/shm` only when their projected parent still matches the persistent parent. Concurrent modification of the same file is quarantined and fails closed. Direct mutation of canonical disk files outside a manifest transaction is also quarantined and fails closed.

`sync-once` chooses one operation:

- RAM changed -> `CAPTURE`;
- persistent generation changed and RAM did not -> `PROJECT`;
- both unchanged -> `NOOP`.

`watch --interval 0.25` repeats the same guarded operation. There is no last-writer-wins mode.

## Synced canonical inputs

`current_memory.json`, `current_task.json`, `active_path.json`, `closed_topics.json`, `timeline_head.json`, `provenance.json`, `receipts/latest.json`, and `aux_phi`.

`aux_phi` is validated as exactly 36 finite little-endian float64 values.

Derived SessionStart files under `session/` are intentionally not persisted.

## Host deployment

Resolve the persistent library and fallback paths from the canonical `noema_paths.json`. The code creates `surface_store/` under that physical library on first `init`.

The repository changeset validates the transaction engine in isolation. Actual installation of the user service and a live `/dev/shm` probe on the user host remain `NOT_RUN` until executed on that host.
