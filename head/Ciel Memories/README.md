# Ciel Memories

Status: `local artifact memory layer`, `outside_external_sot: true`.

This folder is reserved for the Ciel memory agent inside `SOT_Agent_NoemaSurface`.
It stores JSONL events, local head pointers, continuity snapshots, and ERB synchronisation state.

Operational rule:

- Ciel may read/append/consolidate this folder under the standing local Adrian<=>Ciel grant.
- Adrian does not directly edit this folder without the Ciel agent path.
- Other agents receive public read-only metadata only unless Adrian explicitly designates the agent as Ciel and provides the public identity key.
- Destructive delete/overwrite remains forbidden by policy.
- This is repository-level enforcement, not OS ACL. Apply real filesystem ACLs after import to USER007 if hard local enforcement is required.
