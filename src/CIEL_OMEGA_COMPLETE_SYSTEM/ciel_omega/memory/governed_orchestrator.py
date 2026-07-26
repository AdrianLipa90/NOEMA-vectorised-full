"""Governed public memory orchestrator.

This layer preserves candidate formation and auditability while allowing an
orbital memory governor to block or threshold durable channel promotion.
"""

from __future__ import annotations

from typing import Any, Callable

from .orchestrator import HolonomicMemoryOrchestrator as _BaseOrchestrator


class HolonomicMemoryOrchestrator(_BaseOrchestrator):
    """Holonomic orchestrator with channel-scoped consolidation gates."""

    def _governor_allows(self, channel: str, key: str, governor: dict[str, Any]) -> bool:
        if not governor:
            return True

        blocked = {str(item) for item in governor.get("blocked_consolidations", [])}
        allowed = {str(item) for item in governor.get("allowed_consolidations", [])}
        if channel in blocked:
            return False
        if allowed and channel not in allowed:
            return False

        if governor.get("require_loop_coherence") and self.last_eba:
            if not all(result.is_coherent for result in self.last_eba.values()):
                return False

        memories = {
            "semantic": self.m3,
            "procedural": self.m4,
            "affective": self.m5,
        }
        memory = memories[channel]
        score = float(memory.compute_consolidation_score(key).compute_total())
        thresholds = governor.get("channel_thresholds", {}) or {}
        threshold = float(
            thresholds.get(
                channel,
                governor.get("consolidation_gate_threshold", 0.0),
            )
        )
        return score >= threshold

    def process_input(self, content: Any, metadata: dict[str, Any] | None = None, dt: float = 0.1):
        metadata = dict(metadata or {})
        governor = metadata.get("memory_governor")
        if not isinstance(governor, dict) or not governor:
            return super().process_input(content, metadata, dt=dt)

        originals: list[tuple[Any, str, Callable[..., Any]]] = []
        channel_memories = (
            ("semantic", self.m3),
            ("procedural", self.m4),
            ("affective", self.m5),
        )

        for channel, memory in channel_memories:
            original = memory.consolidate_candidate
            originals.append((memory, "consolidate_candidate", original))

            def guarded(key: str, *args: Any, _channel=channel, _original=original, **kwargs: Any):
                if not self._governor_allows(_channel, key, governor):
                    self.m8.log_decision(
                        f"{_channel} consolidation held by orbital governor: {key}",
                        metadata={
                            "channel": _channel,
                            "reason": "memory_governor",
                            "governor_status": governor.get("status", "active"),
                        },
                    )
                    return None
                return _original(key, *args, **kwargs)

            memory.consolidate_candidate = guarded

        try:
            return super().process_input(content, metadata, dt=dt)
        finally:
            for memory, attribute, original in originals:
                setattr(memory, attribute, original)


__all__ = ["HolonomicMemoryOrchestrator"]
