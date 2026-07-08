"""CIELingo CLI — entry point for `cielingo` command.

Usage:
    cielingo info                 — package version + module list
    cielingo seeds [--json]       — load infinitive seeds
    cielingo modalities [--json]  — load modality seeds
    cielingo bus                  — phase bus report
    cielingo chat                 — interactive PhaseNav-powered CIELingo chat
    cielingo ask <TEXT>           — one-shot PhaseNav answer
    cielingo digest <URL...>      — fetch and summarize web content
    cielingo learn <URL...>       — fetch, digest, and store web content
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

try:
    from noema_bootstrap import activate_local_packages

    activate_local_packages()
except Exception:
    pass

from . import __version__
from .htri_phase_bus import phase_bus_report
from .infinitive_modal_potential import load_infinitive_seeds, load_modality_seeds


def _print_json(obj: object) -> None:
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2, default=str)
    sys.stdout.write("\n")


def _cmd_info() -> None:
    print(f"CIELingo v{__version__}")
    print(f"Package root: {Path(__file__).parent}")


def _cmd_seeds(args: list[str]) -> None:
    seeds = load_infinitive_seeds(".")
    if "--json" in args:
        _print_json([s._asdict() if hasattr(s, "_asdict") else str(s) for s in seeds])
    else:
        print(f"Loaded {len(seeds)} infinitive seeds")
        for s in sorted(seeds, key=lambda x: x.infinitive)[:10]:
            print(f"  {s.infinitive:20s} mass={s.rest_semantic_mass:.4f} phi={s.potential_phi:.6f}")
        if len(seeds) > 10:
            print(f"  ... and {len(seeds) - 10} more")


def _cmd_modalities(args: list[str]) -> None:
    mods = load_modality_seeds()
    if "--json" in args:
        _print_json([m._asdict() if hasattr(m, "_asdict") else str(m) for m in mods])
    else:
        print(f"Loaded {len(mods)} modalities")
        for m in mods:
            print(f"  {m.modality_id:20s} family={m.family:12s} mass={m.rest_semantic_mass:.4f}")


def _cmd_bus() -> None:
    report = phase_bus_report()
    _print_json(report)


def _load_inference():
    from ciel_geometry.cielingo_inference import CIELingoInference

    return CIELingoInference()


def _cmd_chat() -> None:
    from ciel_geometry.cielingo_inference import run_cli

    run_cli()


def _cmd_ask(args: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="cielingo ask", add_help=False)
    parser.add_argument("--json", action="store_true", help="Print the full answer payload as JSON.")
    parser.add_argument("--k", type=int, default=5, help="Top-k memory hits.")
    parser.add_argument("text", nargs=argparse.REMAINDER, help="Prompt text.")
    parsed = parser.parse_args(args)

    text = " ".join(piece.strip() for piece in parsed.text if piece.strip()).strip()
    if not text:
        print("Usage: cielingo ask [--json] [--k N] TEXT", file=sys.stderr)
        sys.exit(1)

    inference = _load_inference()
    result = inference.answer(text, k=parsed.k)
    if parsed.json:
        _print_json(result)
        return

    print(result["answer"])
    print()
    print(f"operator: {result['operator']}  confidence: {result['decision'].get('confidence', 'unknown')}")
    if result.get("sources"):
        print("sources:")
        for src in result["sources"][:3]:
            print(f"  - sim={float(src.get('sim', 0.0) or 0.0):.4f} {src.get('text', '')}")


def _cmd_digest(args: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="cielingo digest", add_help=False)
    parser.add_argument("--json", action="store_true", help="Print the digest payload as JSON.")
    parser.add_argument("--news", action="store_true", help="Digest the built-in news feeds instead of URLs.")
    parser.add_argument("--max-sentences", type=int, default=3, help="Maximum sentences per digest.")
    parser.add_argument("--max-articles", type=int, default=5, help="Maximum feed articles when --news is used.")
    parser.add_argument("--theme", action="append", default=[], help="Optional theme label to attach to the digest.")
    parser.add_argument("targets", nargs="*", help="URLs to fetch and digest.")
    parsed = parser.parse_args(args)

    if not parsed.news and not parsed.targets:
        print("Usage: cielingo digest [--json] [--max-sentences N] [URL ...]", file=sys.stderr)
        sys.exit(1)

    ci = _load_inference()
    if parsed.news:
        from cielingo.web_digest import digest_news

        digests = digest_news(max_articles=parsed.max_articles, max_sentences=parsed.max_sentences)
        payload = [d.as_dict() for d in digests]
    else:
        payload = [ci.digest_web(url, max_sentences=parsed.max_sentences) for url in parsed.targets]

    if parsed.json:
        _print_json({"count": len(payload), "digests": payload})
        return

    for item in payload:
        print(f"{item.get('title', '')} [{item.get('url', '')}]")
        print(f"  summary: {item.get('summary', '')}")
        if item.get("keywords"):
            print(f"  keywords: {', '.join(item['keywords'][:8])}")
        if parsed.theme:
            print(f"  themes: {', '.join(parsed.theme)}")
        if item.get("error"):
            print(f"  error: {item['error']}")
        print()


def _cmd_learn(args: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="cielingo learn", add_help=False)
    parser.add_argument("--json", action="store_true", help="Print the learning payload as JSON.")
    parser.add_argument("--news", action="store_true", help="Learn from built-in news feeds instead of URLs.")
    parser.add_argument("--max-sentences", type=int, default=3, help="Maximum sentences per digest.")
    parser.add_argument("--max-articles", type=int, default=5, help="Maximum feed articles when --news is used.")
    parser.add_argument("--no-persist", action="store_true", help="Do not persist learned samples to disk.")
    parser.add_argument("--theme", action="append", default=[], help="Optional theme label to attach to the learned item.")
    parser.add_argument("targets", nargs="*", help="URLs to fetch, digest, and store.")
    parsed = parser.parse_args(args)

    if not parsed.news and not parsed.targets:
        print("Usage: cielingo learn [--json] [--news] [URL ...]", file=sys.stderr)
        sys.exit(1)

    ci = _load_inference()
    if parsed.news:
        result = ci.learn_news(max_articles=parsed.max_articles, persist=not parsed.no_persist, themes=parsed.theme or None)
    else:
        items = [
            ci.learn_web(
                url,
                max_sentences=parsed.max_sentences,
                persist=not parsed.no_persist,
                themes=parsed.theme or None,
            )
            for url in parsed.targets
        ]
        result = {"count": len(items), "items": items, "memory_size": ci.memory.size}

    if parsed.json:
        _print_json(result)
        return

    if "items" in result:
        for item in result["items"]:
            digest = item.get("digest", {})
            learned = item.get("learned", {})
            print(f"{digest.get('title', '')} [{digest.get('url', '')}]")
            print(f"  digest: {digest.get('summary', '')}")
            print(f"  stored index: {learned.get('index', '-')}")
            thematic = item.get("thematic", {})
            if thematic.get("themes"):
                print(f"  themes: {', '.join(thematic['themes'])}")
            print()
    else:
        print(f"Learned {result.get('count', 0)} items; memory size={result.get('memory_size', 0)}")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return
    cmd = args[0]
    rest = args[1:]
    cmds = {
        "info": _cmd_info,
        "seeds": lambda: _cmd_seeds(rest),
        "modalities": lambda: _cmd_modalities(rest),
        "bus": _cmd_bus,
        "chat": _cmd_chat,
        "ask": lambda: _cmd_ask(rest),
        "digest": lambda: _cmd_digest(rest),
        "learn": lambda: _cmd_learn(rest),
    }
    fn = cmds.get(cmd)
    if fn is None:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
    fn()


if __name__ == "__main__":
    main()
