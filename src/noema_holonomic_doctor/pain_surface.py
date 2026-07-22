"""NOEMA pain surface models for diagnostic reports."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class PainPoint:
    code: str
    severity: str
    where: str
    symptom: str
    class_: str = "unknown"
    suggested_action: str = "manual_review"
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["class"] = data.pop("class_")
        return data


def classify_test_result(path: str, returncode: int, elapsed_s: float, timeout_s: float, stdout: str = "", stderr: str = "") -> PainPoint | None:
    if returncode == 0 and elapsed_s <= timeout_s * 0.75:
        return None
    if returncode == 124 or elapsed_s >= timeout_s:
        return PainPoint(
            code="test_timeout",
            severity="high",
            where=path,
            symptom=f"test exceeded timeout budget ({timeout_s:.1f}s)",
            class_="TIMEOUT",
            suggested_action="vectorize_or_split_heavy_fixture",
            evidence={"elapsed_s": elapsed_s, "timeout_s": timeout_s},
        )
    if returncode != 0:
        return PainPoint(
            code="test_failure",
            severity="high",
            where=path,
            symptom="pytest returned non-zero status",
            class_="FAIL",
            suggested_action="inspect_failure_trace_and_patch",
            evidence={"returncode": returncode, "stdout_tail": stdout[-2000:], "stderr_tail": stderr[-2000:]},
        )
    if elapsed_s > timeout_s * 0.75:
        return PainPoint(
            code="slow_test",
            severity="medium",
            where=path,
            symptom="test is close to timeout budget",
            class_="SLOW",
            suggested_action="profile_and_vectorize",
            evidence={"elapsed_s": elapsed_s, "timeout_s": timeout_s},
        )
    return None


__all__ = ["PainPoint", "classify_test_result"]
