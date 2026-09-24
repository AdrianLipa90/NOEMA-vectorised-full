#!/usr/bin/env python3
"""HTRI Benchmark — explicit baseline versus verified HTRI thread metric.

Metodologia:
  Runda A: POST /api/chat/message with caller-supplied baseline threads
  Runda B: POST /api/chat/message with verified HTRI optimal threads

Mierzy: czas odpowiedzi (ms), długość odpowiedzi (chars), chars/ms.
Wynik: tabela A vs B z avg ± std.

Wymagania: serwis ciel-gui aktywny (port 2435), model załadowany.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import statistics
import sys
import time
from pathlib import Path

# Dodaj src do path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import urllib.request

from ciel_sot_agent.htri_scheduler import get_state_status as get_htri_state

GUI_URL    = "http://127.0.0.1:2435"
N_ROUNDS   = 5
PROMPTS    = [
    "kim jesteś?",
    "co to jest Kuramoto?",
    "opisz rezonans Schumanna",
    "co to jest soul invariant?",
    "wyjaśnij synchronizację fazową",
]


def _post(url: str, data: dict) -> tuple[dict, float]:
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return result, elapsed_ms


def _reset():
    try:
        _post(f"{GUI_URL}/api/chat/reset", {})
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/htri_bench.py:54 quiet except scope=_reset reason=pass")
        raise
        pass


def run_round(label: str, n_threads_override: int | None = None) -> list[dict]:
    results = []
    for i, prompt in enumerate(PROMPTS[:N_ROUNDS]):
        _reset()
        payload = {"message": prompt}
        if n_threads_override:
            payload["n_threads_override"] = n_threads_override
        try:
            resp, ms = _post(f"{GUI_URL}/api/chat/message", payload)
            reply_len = len(resp.get("reply", ""))
            htri_n = resp.get("htri_n_threads", "?")
            results.append({
                "prompt": prompt[:30],
                "ms": ms,
                "chars": reply_len,
                "chars_per_ms": reply_len / ms if ms > 0 else 0,
                "htri_n": htri_n,
            })
            print(f"  [{label}] #{i+1} {ms:6.0f}ms  {reply_len}ch  htri_n={htri_n}")
        except Exception as e:
            print(f"  [{label}] #{i+1} ERROR: {e}")
            results.append({"ms": 0, "chars": 0, "chars_per_ms": 0, "error": str(e)})
        time.sleep(0.5)
    return results


def stats(results: list[dict]) -> dict:
    ms_list = [r["ms"] for r in results if r.get("ms", 0) > 0]
    cpm_list = [r["chars_per_ms"] for r in results if r.get("chars_per_ms", 0) > 0]
    return {
        "ms_avg": statistics.mean(ms_list) if ms_list else 0,
        "ms_std": statistics.stdev(ms_list) if len(ms_list) > 1 else 0,
        "cpm_avg": statistics.mean(cpm_list) if cpm_list else 0,
        "cpm_std": statistics.stdev(cpm_list) if len(cpm_list) > 1 else 0,
        "n": len(ms_list),
    }


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("thread count must be positive")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline-threads",
        type=_positive_int,
        required=True,
        help="explicit comparison thread count",
    )
    args = parser.parse_args()
    print("=" * 60)
    print("  HTRI BENCHMARK — inference timing A vs B")
    print("=" * 60)

    htri_state = get_htri_state()
    htri_n = htri_state.get("n_threads_optimal")
    htri_r = htri_state.get("coherence")
    if (
        isinstance(htri_n, bool)
        or not isinstance(htri_n, int)
        or htri_n < 1
        or isinstance(htri_r, bool)
        or not isinstance(htri_r, (int, float))
    ):
        print(
            json.dumps(
                {
                    "status": "unavailable",
                    "reason": "verified_htri_benchmark_metrics_unavailable",
                    "htri_status": htri_state.get("status"),
                    "publication": htri_state.get("publication"),
                    "coherence": None,
                    "optimal_thread_count": None,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 2

    print(
        f"\n  verified HTRI coherence r={float(htri_r):.4f} "
        f"→ n_threads_optimal={htri_n}"
    )
    baseline_n = args.baseline_threads

    # Sprawdź czy serwis działa
    try:
        with urllib.request.urlopen(f"{GUI_URL}/api/chat/models", timeout=5) as r:
            models = json.loads(r.read())
        current = models.get("current", "?")
        print(f"  Model: {Path(current).name if current else '?'}")
    except Exception as e:
        print(f"\nERROR: serwis niedostępny na {GUI_URL}: {e}")
        return 1

    print(f"\n  Runda A (baseline n_threads={baseline_n}):")
    results_a = run_round("A", baseline_n)

    print(f"\n  Runda B (HTRI n_threads={htri_n}):")
    results_b = run_round("B", htri_n)

    sa = stats(results_a)
    sb = stats(results_b)

    print("\n" + "=" * 60)
    print(f"  {'Metryka':<22} {'Runda A (baseline)':>18} {'Runda B (HTRI)':>16}")
    print("  " + "-" * 56)
    print(f"  {'n_threads':<22} {baseline_n:>18} {htri_n:>16}")
    print(f"  {'czas avg (ms)':<22} {sa['ms_avg']:>16.0f}ms {sb['ms_avg']:>14.0f}ms")
    print(f"  {'czas std (ms)':<22} {sa['ms_std']:>16.0f}ms {sb['ms_std']:>14.0f}ms")
    print(f"  {'chars/ms avg':<22} {sa['cpm_avg']:>16.3f}   {sb['cpm_avg']:>14.3f}")
    print(f"  {'chars/ms std':<22} {sa['cpm_std']:>16.3f}   {sb['cpm_std']:>14.3f}")

    if sa["ms_avg"] > 0 and sb["ms_avg"] > 0:
        speedup = (sa["ms_avg"] - sb["ms_avg"]) / sa["ms_avg"] * 100
        jitter_change = (sb["ms_std"] - sa["ms_std"]) / max(sa["ms_std"], 1) * 100
        print()
        print(f"  Δ czas:    {speedup:+.1f}%  (+ = B szybsze)")
        print(f"  Δ jitter:  {jitter_change:+.1f}%  (- = B stabilniejsze)")

    print("=" * 60)

    # Zapisz wyniki
    out = Path(__file__).parent.parent / "integration" / "reports" / "htri_bench_result.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "baseline_n": baseline_n, "htri_n": htri_n, "htri_coherence": htri_r,
        "round_a": sa, "round_b": sb,
    }, indent=2))
    print(f"\n  Wyniki zapisane: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
