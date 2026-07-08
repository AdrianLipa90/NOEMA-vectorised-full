# 2026-06-26 — Auto-continue + skill factory enrichment

## Auto-Continue Mechanism
- **XTEST key injection**: `libX11.so.6` + `libXtst.so.6` loaded via Python ctypes
- Wysyła real keyboard events via X11 XTEST v2.2
- **Window targeting**: `wmctrl -l` + `wmctrl -ia` → focus opencode terminal (title "OC |")
- **Protocol**: detached script → sleep 120s → find terminal → focus → type "continue\n"
- Stan: [`/tmp/opencode_auto.json`](..//tmp/opencode_auto.json) — count/max/interval/status
- Work queue: [`/tmp/opencode_work_queue.json`](../tmp/opencode_work_queue.json)

## Session state
- 290 skills total (po usunięciu 16 orbital-demo dupes)
- Skill factory: 150 auto-generated z LNS/Orbital/Omega docs + 140 original/enriched
- 00-INDEX rebuilt z kategoriami
- Work queue: 16 tasks, start index 3 (3 done: check_dupes, fix_names, update_index)
- Auto-continue: 100 max cycles, 120s interval (~200 min runtime)

## Key files
- [`scripts/noema_skill_factory.py`](../scripts/noema_skill_factory.py) — batch .md→skill converter
- `/tmp/noema_keyinject.py` — X11 keyboard injection
- `/tmp/noema_auto_continue.py` — scheduler
- `/tmp/NOEMA_AUTO_CONTINUE_PROTOCOL.md` — protocol reference
