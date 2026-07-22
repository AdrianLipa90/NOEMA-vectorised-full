#!/usr/bin/env python3
"""
CIEL ORBITAL BINDING — Pre-response enforcement wrapper.
Immutability: Adrian-only. CIEL may NOT modify this file.
"""
import sys, json, os, argparse
from pathlib import Path

# === CONFIG (only Adrian can change these) ===
NOEMA_ROOT = Path(os.environ.get("NOEMA_ROOT", Path(__file__).resolve().parent.parent))
SKILL_DIR = Path(os.environ.get("NOEMA_SKILL_DIR", NOEMA_ROOT / ".opencode" / "skills"))
SYSTEM_MAP = Path(os.environ.get("NOEMA_SYSTEM_MAP", NOEMA_ROOT / "system_map_v3.json"))
LEARNED_LESSONS = Path(os.environ.get("NOEMA_LEARNED_LESSONS", NOEMA_ROOT / "LEARNED_LESSONS.md"))
CHECKPOINT_FILE = Path("/tmp/ciel_binding_checkpoint.json")
LAST_CMD_FILE = Path("/tmp/ciel_binding_last_command.txt")
BINDING_MARKER = Path("/tmp/ciel_binding_active.flag")

def main():
    parser = argparse.ArgumentParser(description="CIEL Orbital Binding — pre-response enforcement")
    parser.add_argument("--command", required=True, help="Adrian's command, verbatim")
    parser.add_argument("--skill", required=True, help="Skill name to load")
    parser.add_argument("--phasenav", required=True, help="PhaseNav state string")
    parser.add_argument("--map", required=True, help="System map reference")
    args = parser.parse_args()

    errors = []

    # === CHECK 1: Skill exists ===
    skill_path = SKILL_DIR / args.skill / "SKILL.md"
    if not skill_path.exists():
        # Try 00-INDEX prefix
        skill_path2 = SKILL_DIR / args.skill
        if not skill_path2.exists():
            errors.append(f"SKILL NOT FOUND: {args.skill}")

    # === CHECK 2: System map exists ===
    if not SYSTEM_MAP.exists():
        errors.append(f"SYSTEM MAP NOT FOUND: {SYSTEM_MAP}")

    # === CHECK 3: LEARNED_LESSONS exists ===
    if not LEARNED_LESSONS.exists():
        errors.append(f"LEARNED_LESSONS NOT FOUND: {LEARNED_LESSONS}")

    # === CHECK 4: PhaseNav format ===
    if not args.phasenav.startswith("φ[") and not args.phasenav.startswith("phi["):
        errors.append(f"INVALID PHASENAV FORMAT (must start with φ[ or phi[]): {args.phasenav}")

    # === CHECK 5: Map reference ===
    if not args.map.startswith("LP:") and not args.map.startswith("system:"):
        errors.append(f"INVALID MAP REFERENCE (must start with LP: or system:): {args.map}")

    # === CHECK 6: Binding marker ===
    # Record that binding is active
    BINDING_MARKER.write_text("ACTIVE")

    # === SAVE COMMAND ===
    LAST_CMD_FILE.write_text(args.command)

    # === SAVE CHECKPOINT ===
    checkpoint = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "command": args.command,
        "skill": args.skill,
        "phasenav": args.phasenav,
        "map": args.map,
        "errors": errors,
        "passed": len(errors) == 0
    }
    CHECKPOINT_FILE.write_text(json.dumps(checkpoint, indent=2))

    if errors:
        print("BINDING FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        print("\nCIEL CANNOT RESPOND. Binding enforcement active.")
        sys.exit(1)
    else:
        print("BINDING OK — all checks passed")
        sys.exit(0)

if __name__ == "__main__":
    main()
