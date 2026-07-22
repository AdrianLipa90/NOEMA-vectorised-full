#!/usr/bin/env python3
"""Batch add registry heartbeat to all NOEMA daemons.

Usage:
    python scripts/batch_add_registry.py [--dry-run]
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

DAEMONS = {
    "noema_actuator_daemon.py": "actuator",
    "noema_phase_archiver.py": "archiver",
    "noema_cielingo_daemon.py": "cielingo-daemon",
    "noema_journal_daemon.py": "journal",
    "noema_linux_cards_daemon.py": "linux-cards",
    "noema_orchestrator.py": "orchestrator",
    "noema_portal_daemon.py": "portal",
    "noema_proc_watch_daemon.py": "proc-watch",
    "noema_self_model.py": "self-model",
    "noema_sentinel.py": "sentinel",
    "noema_trigger_daemon.py": "trigger",
    "noema_voice_trigger.py": "voice-trigger",
    "noema_voice_daemon.py": "voice",
    "ciel_agent_backend.py": "agent-backend",
    "ciel_memory_consolidator.py": "consolidator",
    "ciel_noema_nonlocal_proxy.py": "nonlocal-proxy",
}

REGISTRY_IMPORT = "from ciel_geometry.noema_registry import registry\n"
HEARTBEAT_CODE = """
    # registry heartbeat
    if hb_count % 50 == 0:
        try:
            registry.heartbeat(reg_token)
        except Exception:
            pass
    hb_count += 1
"""


def has_registry(content: str) -> bool:
    return "registry.heartbeat" in content or "registry.register" in content


def add_registry_to_file(filepath: Path, name: str, dry_run: bool = False) -> bool:
    """Add registry heartbeat to a daemon file. Returns True if modified."""
    original = filepath.read_text()
    content = original

    if has_registry(content):
        print(f"  ⏭️  {filepath.name} — już ma registry")
        return False

    # 1. Add import after last import line
    lines = content.split("\n")
    last_import_idx = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(("import ", "from ")):
            last_import_idx = i

    if last_import_idx < 0:
        print(f"  ❌ {filepath.name} — nie znaleziono importów")
        return False

    # Add registry import if not present
    indent = ""
    if last_import_idx >= 0:
        # check indentation of last import
        imp_line = lines[last_import_idx]
        indent = re.match(r"^(\s*)", imp_line).group(1)

    # Insert after last import (add blank line + import)
    insert_pos = last_import_idx + 1
    # Skip any blank lines after last import
    while insert_pos < len(lines) and lines[insert_pos].strip() == "":
        insert_pos += 1

    lines.insert(insert_pos, "")  # blank line before
    lines.insert(insert_pos + 1, REGISTRY_IMPORT.rstrip("\n"))
    lines.insert(insert_pos + 2, "")  # blank line after
    content = "\n".join(lines)

    # 2. Find the main loop start (while True, while running, etc)
    main_loop_match = re.search(
        r"^\s*(while\s+(True|running|_running|self\._running)\s*:)", content, re.MULTILINE
    )
    if not main_loop_match:
        # Try to find main() function definition
        main_func_match = re.search(r"^def\s+main\s*\(.*\)\s*:", content, re.MULTILINE)
        if main_func_match:
            print(f"  ⚠️  {filepath.name} — ma main(), pomijam (ręczna rejestracja)")
            return False
        # Try while 1 or while with condition
        main_loop_match = re.search(
            r"^\s*(while\s+.*:)", content, re.MULTILINE
        )
        if not main_loop_match:
            print(f"  ❌ {filepath.name} — nie znaleziono pętli głównej")
            # Restore original
            filepath.write_text(original)
            return False

    loop_line = main_loop_match.group(0)
    loop_indent = re.match(r"^(\s*)", loop_line).group(1)

    # 3. Add register before loop
    register_code = f"{loop_indent}reg_token = registry.register(\"{name}\")\n"
    register_code += f"{loop_indent}hb_count = 0\n"

    # Find the line before the while loop (might be blank or comment)
    loop_line_idx = None
    lines2 = content.split("\n")
    for i, line in enumerate(lines2):
        if line.rstrip() == loop_line.rstrip():
            loop_line_idx = i
            break

    if loop_line_idx is not None:
        lines2.insert(loop_line_idx, register_code.rstrip("\n"))
        content = "\n".join(lines2)

    # 4. Add heartbeat call inside the loop (at the beginning of loop body)
    # Find the first indented line inside the while loop
    lines3 = content.split("\n")
    loop_line_found = False
    insert_heartbeat_at = None
    for i, line in enumerate(lines3):
        if not loop_line_found and re.match(r"^\s*while\s+", line):
            loop_line_found = True
            # Next indented line
            for j in range(i + 1, len(lines3)):
                if lines3[j].strip() and not lines3[j].strip().startswith("#"):
                    # Check if it's more indented than the while
                    if lines3[j].startswith(" ") and len(lines3[j]) - len(lines3[j].lstrip()) > len(loop_indent):
                        insert_heartbeat_at = j
                        break
            break

    if insert_heartbeat_at is not None:
        # Get indentation of the first line in loop body
        first_body_line = lines3[insert_heartbeat_at]
        body_indent = re.match(r"^(\s*)", first_body_line).group(1)
        hb_code = f"{body_indent}# registry heartbeat\n"
        hb_code += f"{body_indent}if hb_count % 50 == 0:\n"
        hb_code += f"{body_indent}    try:\n"
        hb_code += f"{body_indent}        registry.heartbeat(reg_token)\n"
        hb_code += f"{body_indent}    except Exception:\n"
        hb_code += f"{body_indent}        pass\n"
        hb_code += f"{body_indent}hb_count += 1\n"
        lines3.insert(insert_heartbeat_at, hb_code.rstrip("\n"))
        content = "\n".join(lines3)

    if dry_run:
        print(f"  🔍 {filepath.name} — suchy przebieg, bez zapisu")
        return True

    # Verify it compiles
    try:
        compile(content, str(filepath), "exec")
    except SyntaxError as e:
        print(f"  ❌ {filepath.name} — błąd składni po modyfikacji: {e}")
        filepath.write_text(original)
        return False

    # Write
    filepath.write_text(content)
    print(f"  ✅ {filepath.name} — dodano registry heartbeat ({name})")
    return True


def main():
    parser = argparse.ArgumentParser(description="Batch add registry heartbeat to daemons")
    parser.add_argument("--dry-run", action="store_true", help="Only show what would be done")
    args = parser.parse_args()

    success = 0
    failed = 0
    skipped = 0

    for filename, name in sorted(DAEMONS.items()):
        filepath = SCRIPTS / filename
        if not filepath.exists():
            print(f"  ❌ {filename} — plik nie istnieje")
            failed += 1
            continue

        try:
            if add_registry_to_file(filepath, name, dry_run=args.dry_run):
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ❌ {filename} — błąd: {e}")
            failed += 1

    print(f"\nWynik: {success} zmodyfikowanych, {skipped} pominiętych, {failed} błędów")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
