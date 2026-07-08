from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.prompt_inject import (  # noqa: E402
    PROMPT_INJECT_TIMEOUT_SECONDS,
    build_prompt_inject_context,
    render_noema_metrics_block,
)


def test_prompt_inject_timeout_is_120_seconds() -> None:
    assert PROMPT_INJECT_TIMEOUT_SECONDS == 120


def test_prompt_inject_renders_metrics_and_prompt() -> None:
    metrics_summary = {
        "total": 2,
        "ok": 1,
        "warning": 0,
        "critical": 1,
        "unknown": 0,
        "metrics": {
            "noema_tick": {
                "value": 7,
                "status": "ok",
                "unit": "count",
                "description": "tick",
                "source": "surface",
            },
            "daemons_alive": {
                "value": 23,
                "status": "ok",
                "unit": "count",
                "description": "alive",
                "source": "daemon",
            },
        },
    }

    metrics_block = render_noema_metrics_block(metrics_summary)
    assert "=== NOEMA_METRICS_BEGIN ===" in metrics_block
    assert "summary=total=2 ok=1 warning=0 critical=1 unknown=0" in metrics_block
    assert "[system]" in metrics_block
    assert "[daemon]" in metrics_block
    assert "noema_tick" in metrics_block
    assert "daemons_alive" in metrics_block

    context = build_prompt_inject_context(
        message="Pierw start prompt",
        cielingo_block="=== CIELINGO_MESSAGE ===\nhello\n=== CIELINGO_MESSAGE_END ===",
        metrics_summary=metrics_summary,
    )
    assert "Pierw start prompt" in context
    assert "CIELINGO_MESSAGE" in context
    assert "NOEMA_METRICS_BEGIN" in context
