from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from .audit import append_audit, verify_audit_chain
from .baseline import build_baseline, compare_to_baseline, enroll_baseline, write_baseline
from .compare import compare_artifacts
from .immune import analyse_artifact, scan
from .manifest import write_manifest
from .memory import ImmuneMemory
from .noema_sot import FileSoTClient, build_vectorised_status, write_json
from .phasenav import vector_with_labels
from .policy import ImmunePolicy, write_default_policy
from .structure import structure_summary


def _load_policy(args: argparse.Namespace) -> ImmunePolicy:
    return ImmunePolicy.load(getattr(args, "policy", None))


def cmd_vector(args: argparse.Namespace) -> int:
    artifact, features, phase_vector = analyse_artifact(args.path)
    data = Path(args.path).read_bytes()
    payload = {
        "artifact": artifact.to_dict(),
        "structure": structure_summary(data, args.path).to_dict(),
        "phase_vector": phase_vector.to_dict(),
        "vector_labeled": vector_with_labels(phase_vector.vector),
        "features_summary": {
            "byte_entropy_norm": features.byte_entropy_norm,
            "base64_entropy_norm": features.base64_entropy_norm,
            "chunk_entropy_mean": features.chunk_entropy_mean,
            "chunk_entropy_std": features.chunk_entropy_std,
            "chunk_entropy_max_delta": features.chunk_entropy_max_delta,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def cmd_enroll(args: argparse.Namespace) -> int:
    artifact, features, phase_vector = analyse_artifact(args.path)
    data = Path(args.path).read_bytes()
    structure = structure_summary(data, args.path)
    memory = ImmuneMemory(args.memory)
    profile = memory.enroll(
        args.label,
        artifact,
        phase_vector,
        features,
        notes=args.notes or "",
        structure_kind=structure.kind,
    )
    print(json.dumps({"enrolled": profile.to_dict(), "structure": structure.to_dict()}, indent=2, sort_keys=True))
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    memory = ImmuneMemory(args.memory)
    record = scan(args.path, memory, policy=_load_policy(args))
    if args.audit:
        append_audit(args.audit, record)
    print(json.dumps(record.to_dict(), indent=2, sort_keys=True))
    return 0 if record.decision in {"ALLOW", "WARN", "REVIEW"} else 2


def _iter_files(root: Path, recursive: bool, max_files: int) -> Iterable[Path]:
    iterator = root.rglob("*") if recursive else root.iterdir()
    count = 0
    for item in iterator:
        if item.is_file():
            count += 1
            if count > max_files:
                break
            yield item


def cmd_scan_dir(args: argparse.Namespace) -> int:
    memory = ImmuneMemory(args.memory)
    policy = _load_policy(args)
    root = Path(args.path)
    results = []
    exit_code = 0
    for item in _iter_files(root, args.recursive, args.max_files):
        record = scan(str(item), memory, policy=policy)
        if args.audit:
            append_audit(args.audit, record)
        if record.decision == "QUARANTINE":
            exit_code = 2
        results.append({"path": str(item), "decision": record.decision, "score": record.score, "reasons": record.reasons})
    print(json.dumps({"schema": "pn-bis-directory-scan-v0.2", "root": str(root), "count": len(results), "results": results}, indent=2, sort_keys=True))
    return exit_code


def cmd_manifest(args: argparse.Namespace) -> int:
    payload = write_manifest(args.path, args.output)
    print(json.dumps({"written": str(args.output), "artifact_sha256": payload["artifact"]["sha256"], "vector_digest": payload["phase_vector"]["digest"]}, indent=2, sort_keys=True))
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    print(json.dumps(compare_artifacts(args.left, args.right), indent=2, sort_keys=True))
    return 0


def cmd_policy_init(args: argparse.Namespace) -> int:
    write_default_policy(args.output)
    print(json.dumps({"written": str(args.output)}, indent=2, sort_keys=True))
    return 0


def cmd_verify_audit(args: argparse.Namespace) -> int:
    result = verify_audit_chain(args.path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 2


def _parse_excludes(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def cmd_baseline(args: argparse.Namespace) -> int:
    snapshot = build_baseline(args.path, recursive=args.recursive, max_files=args.max_files, excludes=_parse_excludes(args.exclude))
    write_baseline(snapshot, args.output)
    print(json.dumps({"written": str(args.output), "entries": len(snapshot.entries), "tree_digest": snapshot.tree_digest}, indent=2, sort_keys=True))
    return 0


def cmd_baseline_diff(args: argparse.Namespace) -> int:
    payload = compare_to_baseline(
        args.baseline,
        args.path,
        policy=_load_policy(args),
        recursive=args.recursive,
        max_files=args.max_files,
        excludes=_parse_excludes(args.exclude),
    )
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["overall"] == "PASS" else (2 if payload["overall"] == "FAIL" else 1)


def cmd_baseline_enroll(args: argparse.Namespace) -> int:
    from .baseline import load_baseline

    snapshot = load_baseline(args.baseline)
    payload = enroll_baseline(snapshot, args.memory, label_prefix=args.label_prefix)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0

def _sot_client(args: argparse.Namespace) -> FileSoTClient:
    return FileSoTClient(args.sot)


def cmd_sot_init(args: argparse.Namespace) -> int:
    payload = _sot_client(args).init()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def cmd_sot_pull(args: argparse.Namespace) -> int:
    client = _sot_client(args)
    client.init()
    current = client.pull_current()
    payload = {
        "schema": "NOEMA_PULL_CURRENT_RESULT_V0_1",
        "sot": str(client.root),
        "current_state_loaded": current.current_loaded,
        "current_state_id": current.state_id,
        "payload": current.payload,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if current.current_loaded else 1


def cmd_sot_status(args: argparse.Namespace) -> int:
    client = _sot_client(args)
    client.init()
    status = build_vectorised_status(
        args.repo,
        sot=client,
        baseline_path=args.baseline,
        memory_path=args.memory,
        tests=args.tests,
        release_gate=args.release_gate,
        excludes=_parse_excludes(args.exclude),
        max_files=args.max_files,
    )
    if args.output:
        write_json(status.payload, args.output)
    print(json.dumps(status.payload, indent=2, sort_keys=True))
    return 0


def cmd_sot_stage_update(args: argparse.Namespace) -> int:
    client = _sot_client(args)
    client.init()
    status = build_vectorised_status(
        args.repo,
        sot=client,
        baseline_path=args.baseline,
        memory_path=args.memory,
        tests=args.tests,
        release_gate=args.release_gate,
        excludes=_parse_excludes(args.exclude),
        max_files=args.max_files,
    )
    candidate = client.stage_update(
        status,
        message=args.message or "",
        promote_current_requested=args.request_current_promotion,
    )
    if args.output:
        write_json(candidate, args.output)
    print(json.dumps({"candidate_id": candidate["candidate_id"], "written": str(client.staged / f'{candidate["candidate_id"]}.json'), "status_digest": status.digest}, indent=2, sort_keys=True))
    return 0


def cmd_sot_accept(args: argparse.Namespace) -> int:
    client = _sot_client(args)
    receipt = client.accept_candidate(args.candidate_id, promote_current=args.promote_current, accepted_by=args.accepted_by)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


def cmd_sot_verify(args: argparse.Namespace) -> int:
    result = _sot_client(args).verify_receipt(args.candidate_id)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pn-bil",
        description="PhaseNav Binary Immune Surface: defensive static vectorisation and immune scoring.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_vector = sub.add_parser("vector", help="Inspect a 24D PhaseNav-compatible vector for an artefact.")
    p_vector.add_argument("path")
    p_vector.set_defaults(func=cmd_vector)

    p_enroll = sub.add_parser("enroll", help="Enroll a known-good artefact into immune memory.")
    p_enroll.add_argument("path")
    p_enroll.add_argument("--label", required=True)
    p_enroll.add_argument("--memory", required=True)
    p_enroll.add_argument("--notes", default="")
    p_enroll.set_defaults(func=cmd_enroll)

    p_scan = sub.add_parser("scan", help="Scan an artefact against immune memory.")
    p_scan.add_argument("path")
    p_scan.add_argument("--memory", required=True)
    p_scan.add_argument("--policy")
    p_scan.add_argument("--audit")
    p_scan.set_defaults(func=cmd_scan)

    p_scan_dir = sub.add_parser("scan-dir", help="Scan a directory of artefacts without executing them.")
    p_scan_dir.add_argument("path")
    p_scan_dir.add_argument("--memory", required=True)
    p_scan_dir.add_argument("--policy")
    p_scan_dir.add_argument("--audit")
    p_scan_dir.add_argument("--recursive", action="store_true")
    p_scan_dir.add_argument("--max-files", type=int, default=256)
    p_scan_dir.set_defaults(func=cmd_scan_dir)

    p_manifest = sub.add_parser("manifest", help="Write a deterministic artefact manifest.")
    p_manifest.add_argument("path")
    p_manifest.add_argument("--output", required=True)
    p_manifest.set_defaults(func=cmd_manifest)

    p_compare = sub.add_parser("compare", help="Compare two artefacts on the PhaseNav immune surface.")
    p_compare.add_argument("left")
    p_compare.add_argument("right")
    p_compare.set_defaults(func=cmd_compare)

    p_policy = sub.add_parser("policy-init", help="Write a default policy JSON file.")
    p_policy.add_argument("--output", required=True)
    p_policy.set_defaults(func=cmd_policy_init)

    p_audit = sub.add_parser("verify-audit", help="Verify append-only audit hash chain integrity.")
    p_audit.add_argument("path")
    p_audit.set_defaults(func=cmd_verify_audit)

    p_baseline = sub.add_parser("baseline", help="Create a deterministic known-good directory baseline.")
    p_baseline.add_argument("path")
    p_baseline.add_argument("--output", required=True)
    p_baseline.add_argument("--recursive", action="store_true", default=True)
    p_baseline.add_argument("--max-files", type=int, default=10000)
    p_baseline.add_argument("--exclude", help="Comma-separated glob patterns to exclude, relative to baseline root.")
    p_baseline.set_defaults(func=cmd_baseline)

    p_diff = sub.add_parser("baseline-diff", help="Compare a directory to a saved known-good baseline.")
    p_diff.add_argument("path")
    p_diff.add_argument("--baseline", required=True)
    p_diff.add_argument("--policy")
    p_diff.add_argument("--output")
    p_diff.add_argument("--recursive", action="store_true", default=True)
    p_diff.add_argument("--max-files", type=int, default=10000)
    p_diff.add_argument("--exclude", help="Comma-separated glob patterns to exclude, relative to scan root.")
    p_diff.set_defaults(func=cmd_baseline_diff)

    p_benroll = sub.add_parser("baseline-enroll", help="Enroll all entries in a baseline as immune self profiles.")
    p_benroll.add_argument("--baseline", required=True)
    p_benroll.add_argument("--memory", required=True)
    p_benroll.add_argument("--label-prefix", default="baseline")
    p_benroll.set_defaults(func=cmd_baseline_enroll)

    p_sot_init = sub.add_parser("sot-init", help="Initialise a local append-only NOEMA SoT simulator.")
    p_sot_init.add_argument("--sot", required=True, help="Directory for local file SoT state.")
    p_sot_init.set_defaults(func=cmd_sot_init)

    p_sot_pull = sub.add_parser("sot-pull", help="Pull CURRENT/latest-state from local file SoT.")
    p_sot_pull.add_argument("--sot", required=True)
    p_sot_pull.set_defaults(func=cmd_sot_pull)

    p_sot_status = sub.add_parser("sot-status", help="Build a vectorised NOEMA status snapshot for this repo/state.")
    p_sot_status.add_argument("--sot", required=True)
    p_sot_status.add_argument("--repo", default=".")
    p_sot_status.add_argument("--baseline")
    p_sot_status.add_argument("--memory")
    p_sot_status.add_argument("--tests", default="unknown", choices=["pass", "fail", "unknown"])
    p_sot_status.add_argument("--release-gate", choices=["PASS", "REVIEW", "FAIL", "UNKNOWN"])
    p_sot_status.add_argument("--exclude", help="Comma-separated glob patterns to exclude from status baseline.")
    p_sot_status.add_argument("--max-files", type=int, default=10000)
    p_sot_status.add_argument("--output")
    p_sot_status.set_defaults(func=cmd_sot_status)

    p_sot_stage = sub.add_parser("sot-stage-update", help="Stage an append-only vectorised status update candidate.")
    p_sot_stage.add_argument("--sot", required=True)
    p_sot_stage.add_argument("--repo", default=".")
    p_sot_stage.add_argument("--baseline")
    p_sot_stage.add_argument("--memory")
    p_sot_stage.add_argument("--tests", default="unknown", choices=["pass", "fail", "unknown"])
    p_sot_stage.add_argument("--release-gate", choices=["PASS", "REVIEW", "FAIL", "UNKNOWN"])
    p_sot_stage.add_argument("--exclude", help="Comma-separated glob patterns to exclude from status baseline.")
    p_sot_stage.add_argument("--max-files", type=int, default=10000)
    p_sot_stage.add_argument("--message", default="")
    p_sot_stage.add_argument("--request-current-promotion", action="store_true")
    p_sot_stage.add_argument("--output")
    p_sot_stage.set_defaults(func=cmd_sot_stage_update)

    p_sot_accept = sub.add_parser("sot-accept", help="Local simulator only: accept a staged candidate into snaps, optionally updating CURRENT.")
    p_sot_accept.add_argument("--sot", required=True)
    p_sot_accept.add_argument("--candidate-id", required=True)
    p_sot_accept.add_argument("--promote-current", action="store_true")
    p_sot_accept.add_argument("--accepted-by", default="local-operator")
    p_sot_accept.set_defaults(func=cmd_sot_accept)

    p_sot_verify = sub.add_parser("sot-verify", help="Verify a local file SoT receipt for a staged candidate.")
    p_sot_verify.add_argument("--sot", required=True)
    p_sot_verify.add_argument("--candidate-id", required=True)
    p_sot_verify.set_defaults(func=cmd_sot_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # CLI boundary; library functions remain typed.
        print(f"pn-bil error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
