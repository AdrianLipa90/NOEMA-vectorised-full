#!/usr/bin/env python3
"""Timing probe: mierzy czas każdego kroku w pipeline process_text().
Uruchamia się jako standalone (nie przez socket) żeby zobaczyć gdzie jest bottleneck."""
import sys, time, threading
sys.path.insert(0, "/home/adrian/noema/scripts")
sys.path.insert(0, "/home/adrian/noema/src")
sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")

TEXT = "test"

def ts(label, t0):
    print(f"  [{time.time()-t0:.2f}s] {label}", flush=True)

t_total = time.time()

print("=== STEP 1: _build_lingo_frame ===", flush=True)
t0 = time.time()
from ciel_headless_daemon import _build_lingo_frame, _get_learning_engine, _read_surface_state, _inject_phi_to_surface, _frame_to_phi
frame = _build_lingo_frame(TEXT)
ts("build_lingo_frame done", t0)

print("=== STEP 2: _frame_to_phi ===", flush=True)
t0 = time.time()
phi = _frame_to_phi(frame)
ts("frame_to_phi done", t0)

print("=== STEP 3: inject ===", flush=True)
t0 = time.time()
injection = _inject_phi_to_surface(phi, strength=0.3)
ts("inject done", t0)

print("=== STEP 4: read_surface_state ===", flush=True)
t0 = time.time()
surface_state = _read_surface_state()
ts("read_surface_state done", t0)

print("=== STEP 4a: learning engine + encoder_weighted ===", flush=True)
t0 = time.time()
eng = _get_learning_engine()
ts("_get_learning_engine done", t0)
if eng is not None:
    t0 = time.time()
    q_phi, q_weights = eng._encoder_weighted(TEXT)
    ts("_encoder_weighted done", t0)
    t0 = time.time()
    q_results = eng.memory.query(q_phi, k=3, min_sim=0.15, weights=q_weights,
                                  exclude_sources={"raw_logs"})
    ts(f"memory.query done ({len(q_results)} wynikow)", t0)
else:
    print("  [WARNING] learning engine is None", flush=True)

print("=== STEP 5: parallel tasks (12s budget) ===", flush=True)
t0 = time.time()
_kr_box: list = []
_ciel_box: list = []

def _bg_knowledge():
    try:
        from ciel_geometry.cielingo_headless import generate_headless_response
        _kr_box.append(generate_headless_response(TEXT, ciel_state=surface_state))
        print(f"  [bg_knowledge done in {time.time()-t0:.2f}s]", flush=True)
    except Exception as e:
        print(f"  [bg_knowledge ERROR: {e}]", flush=True)

def _bg_cielingo():
    try:
        _eng = eng or _get_learning_engine()
        if _eng:
            _ciel_box.append(_eng.answer(TEXT, k=15))
            print(f"  [bg_cielingo done in {time.time()-t0:.2f}s]", flush=True)
    except Exception as e:
        print(f"  [bg_cielingo ERROR: {e}]", flush=True)

t_kr = threading.Thread(target=_bg_knowledge, daemon=True)
t_ciel = threading.Thread(target=_bg_cielingo, daemon=True)
t_kr.start()
t_ciel.start()

deadline = t0 + 12.0
t_kr.join(timeout=max(0.0, deadline - time.time()))
t_ciel.join(timeout=max(0.0, deadline - time.time()))
ts("parallel phase done (12s budget)", t0)

print("=== STEP 6: realize_native_reply ===", flush=True)
t0 = time.time()
from ciel_sot_agent.conversation_bridge import realize_native_reply
episodic = realize_native_reply(TEXT, ciel_state=surface_state, language="pl")
ts("realize_native_reply done", t0)

print("=== STEP 7: CerebralLanguageModel.process ===", flush=True)
t0 = time.time()
from ciel_headless_daemon import _get_cerebral_model
cm = _get_cerebral_model()
cr = cm.process(TEXT)
ts(f"cerebral.process done, reply[:60]={str(cr.get('reply',''))[:60]}", t0)

print(f"\n=== TOTAL: {time.time()-t_total:.2f}s ===", flush=True)
