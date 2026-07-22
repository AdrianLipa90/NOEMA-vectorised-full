from __future__ import annotations

from .canonical import canonicalize
from .features import extract_features
from .memory import ImmuneMemory
from .phasenav import build_phase_vector, normalised_distance, seed_from_sha256
from .policy import ImmunePolicy
from .schema import ImmuneDecisionRecord
from .structure import structure_summary


def analyse_artifact(path: str):
    artifact, data, b64 = canonicalize(path)
    seed = seed_from_sha256(artifact.sha256)
    features = extract_features(data, b64, seed)
    phase_vector = build_phase_vector(artifact, features)
    return artifact, features, phase_vector


def decide_from_distance(
    distance: float,
    exact: bool,
    empty_memory: bool,
    policy: ImmunePolicy | None = None,
) -> tuple[str, list[str], float]:
    policy = policy or ImmunePolicy()
    if empty_memory:
        return "REVIEW", ["no immune memory profiles are enrolled"], 0.35
    if exact:
        return "ALLOW", ["exact SHA-256 match to enrolled self profile"], 1.0
    if distance <= policy.allow_distance:
        return "ALLOW", ["phase-vector distance is within strict self tolerance"], 0.92
    if distance <= policy.warn_distance:
        return "WARN", ["minor drift from nearest self profile"], 0.76
    if distance <= policy.review_distance:
        return "REVIEW", ["material drift requires human review"], 0.55
    return "QUARANTINE", ["strong non-self anomaly relative to immune memory"], 0.18


def scan(path: str, memory: ImmuneMemory, policy: ImmunePolicy | None = None) -> ImmuneDecisionRecord:
    policy = policy or ImmunePolicy()
    artifact, data, b64 = canonicalize(path)
    seed = seed_from_sha256(artifact.sha256)
    features = extract_features(data, b64, seed)
    phase_vector = build_phase_vector(artifact, features)
    candidate_structure = structure_summary(data, path)

    exact_profile = memory.by_sha256(artifact.sha256)
    exact = exact_profile is not None

    nearest_label = None
    nearest_distance = None
    nearest_profile_digest = None
    nearest_structure_kind = None

    if memory.profiles:
        candidate = phase_vector.vector
        for profile in memory.profiles:
            profile_vector = profile.phase_vector["vector"]
            dist = normalised_distance(candidate, profile_vector)
            if nearest_distance is None or dist < nearest_distance:
                nearest_distance = dist
                nearest_label = profile.label
                nearest_profile_digest = profile.phase_vector.get("digest")
                nearest_structure_kind = profile.artifact.get("structure_kind")

    decision, reasons, score = decide_from_distance(
        nearest_distance if nearest_distance is not None else 1.0,
        exact,
        memory.is_empty(),
        policy,
    )

    # Strong internal instability can never be silently allowed.
    j_bus_total = phase_vector.metric_state.get("j_bus_total", 0.0)
    if decision == "ALLOW" and j_bus_total > policy.high_bus_cost_warn:
        decision = "WARN"
        score = min(score, 0.70)
        reasons.append("internal PhaseNav bus cost is high despite profile similarity")

    # If structure metadata exists on the nearest profile, surface class drift.
    if nearest_structure_kind and nearest_structure_kind != candidate_structure.kind:
        msg = f"artefact kind drift: nearest self is {nearest_structure_kind}, candidate is {candidate_structure.kind}"
        if policy.quarantine_on_kind_mismatch:
            decision = "QUARANTINE"
            score = min(score, 0.20)
            reasons.append(msg)
        elif policy.warn_on_kind_mismatch and decision == "ALLOW":
            decision = "WARN"
            score = min(score, 0.72)
            reasons.append(msg)
        else:
            reasons.append(msg)

    candidate = {
        "artifact": artifact.to_dict(),
        "structure": candidate_structure.to_dict(),
        "features": features.to_dict(),
        "phase_vector": phase_vector.to_dict(),
        "policy": policy.to_dict(),
    }

    return ImmuneDecisionRecord(
        decision=decision,  # type: ignore[arg-type]
        score=score,
        nearest_label=nearest_label,
        nearest_distance=nearest_distance,
        exact_sha256_match=exact,
        reasons=reasons,
        candidate=candidate,
        nearest_profile_digest=nearest_profile_digest,
    )
