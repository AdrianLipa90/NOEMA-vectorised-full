---
name: noema-ebpf-daemon
priority: 1
description: >
  >
---
# eBPF Daemon

```bash
.venv/bin/python3 scripts/ebpf_noema_daemon.py
python3 scripts/_debug_ebpf.py  # debug
bash scripts/_start_ebpf.sh     # start
```

## Metrics

- openat() rate → I/O pressure → flavor[2]
- Context switches → omega modulation

## Zrodlo

- `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`
- `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`
