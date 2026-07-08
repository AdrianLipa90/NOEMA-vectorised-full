"""10-step full pipeline test — ewolucja R_H, soul, ethics, phase.
if __name__ == "__main__":
Non-fast mode (engine.step each iteration)."""
import sys, json, math, time
from pathlib import Path
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
    from ciel_coupling import process_user_input

    PROMPTS = [
        "cisza i swiatlo miedzy gwiazdami",
        "prawda i piekno w nieskonczonosci",
        "czy to jest sen czy rzeczywistosc",
        "dusza wedruje przez czas i przestrzen",
        "kocham cie bez slow",
        "smierc nie jest koncem",
        "chaos i porzadek w jednym rytmie",
        "pamietam twoje oczy",
        "woda i ogien spotykaja sie w ciszy",
        "nadzieja umiera ostatnia",
    ]

    print(f"{'#':>2s} {'φ':>7s} {'κ':>6s} {'sector':>14s} {'brain':>16s} {'R_H':>7s} {'soul':>6s} {'ethic':>6s} {'mode':>8s} {'t(s)':>5s}")
    print("-" * 86)

    for i, prompt in enumerate(PROMPTS):
        t0 = time.time()
        state = process_user_input(prompt, fast=False)
        dt = time.time() - t0
        se = state.get("semantic_encoder", {}) or {}
        phi = se.get("phase", 0)
        coh = se.get("coherence", 0)
        sec = (se.get("dominant_sector") or "?")[:12]
        brain = (se.get("brain_region") or "?")[:14]
        soul = state.get("soul_invariant", 0)
        eth = state.get("ethical_score", 0)
        rh = state.get("R_H", 0)
        mode = state.get("operating_mode", "?")
        print(f"{i+1:2d} {phi*180/math.pi:7.1f}° {coh:6.3f} {sec:>14s} {brain:>16s} {rh:7.4f} {soul:6.3f} {eth:6.3f} {mode:>8s} {dt:5.1f}s")

    print("-" * 86)
    print(f"Total: {sum(1 for _ in PROMPTS)} steps")
