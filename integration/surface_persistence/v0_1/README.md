# NOEMA Persistent Surface Sync v0.1

This layer solves the `/dev/shm/ciel_noema` continuity problem without promoting volatile RAM state to Source of Truth.

## Canonical topology

```text
{KANON}/noema/library/surface_store/
    canonical/           persistent Source of Truth
    journal/events.jsonl append-only transaction history
    sync_receipts/       synchronization receipts
    quarantine/          CAS/hash conflicts
    locks/               process lock
    manifest.json        generation + hashes

{KANON}/runtime/surface-fallback/
    derived last-known-good disk mirror

/dev/shm/ciel_noema/
    ephemeral high-speed projection
    .noema_projection.json
```

The existing project contract remains intact: `/dev/shm` is a session surface/startpoint, not automatic SoT.

## Synchronization semantics

- `project`: persistent canonical state -> `/dev/shm`.
- `capture`: validated `/dev/shm` changes -> persistent state only if the projection generation/hash still matches the persistent parent.
- concurrent edits on disk and RAM produce an explicit `CONFLICT`; no last-writer-wins.
- successful capture increments `generation`, fsyncs the persistent write, refreshes the derived fallback and reprojects the new generation.
- `surface-fallback` is a derived last-known-good copy and cannot silently become authoritative.
- `session/startpoint.json` and `session/system_message.txt` remain derived SessionStart products and are not persistent canonical inputs.

## Canonical input set

- `current_memory.json`
- `current_task.json`
- `active_path.json`
- `closed_topics.json`
- `timeline_head.json`
- `provenance.json`
- `receipts/latest.json`
- `aux_phi`

`aux_phi` must be exactly 36 finite little-endian float64 values (288 bytes).

## Host lifecycle

1. Resolve `{library}` and `{surface_fallback}` from canonical `noema_paths.json`.
2. Run `init` once. This creates `{library}/surface_store` on the physical disk.
3. If migrating an existing trusted surface/fallback, use `import-seed` exactly once.
4. Run `project` before the existing `dev_shm_startpoint.py` SessionStart probe.
5. Call `capture` on every meaningful runtime writeback.
6. A watcher/service may invoke `capture` periodically for near-live persistence, but it must preserve the same generation+SHA CAS semantics.

No symlinks are required. The disk and RAM copies are bound by generation and SHA-256 receipts rather than by filesystem aliasing.
