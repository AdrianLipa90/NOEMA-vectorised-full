#!/usr/bin/env python3
"""
noema-chat — CLI wektoryzowany przez PhaseNav.
Unix socket → body daemon → wheel engine → odpowiedź.
Kolor, skille, pipeline, historia.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import socket
import sys
import os
import pathlib
import argparse
import datetime
import re

SOCKET_PATH = pathlib.Path(
    '/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/sandbox_body/state/body.sock'
)

# Ścieżki do PN-BIS (Bonus od Adriana)
_PN_BIS_PATHS = [
    '/tmp/phasenav-binary-immune-surface/phasenav-binary-immune-surface/src',
    '/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/.venv/lib/python3.12/site-packages',
]
for _p in _PN_BIS_PATHS:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Kolory ANSI ─────────────────────────────────────────────────────
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    # Operator colours
    TRANSFORM = '\033[36m'    # cyan
    WARP = '\033[35m'         # magenta
    REFLECT = '\033[32m'      # green
    BOND = '\033[33m'         # yellow
    CREATE = '\033[38;5;214m' # orange
    ASCEND = '\033[94m'       # light blue
    DESCEND = '\033[91m'      # red
    GROUND = '\033[38;5;94m'  # brown
    RELEASE = '\033[38;5;219m'# pink
    IGNITE = '\033[38;5;196m' # bright red
    VOID = '\033[90m'         # grey
    CAUSE = '\033[38;5;45m'   # sky blue
    FORCE = '\033[38;5;160m'  # deep red
    AFFECT = '\033[38;5;206m' # hot pink
    BIND = '\033[33m'         # yellow
    ATTRACTOR = '\033[38;5;93m'# purple
    MODAL = '\033[38;5;51m'   # turquoise
    EVALUATE = '\033[38;5;154m'# lime
    MEMORY = '\033[38;5;141m' # lavender

    # R level
    R_HIGH = '\033[32m'       # green
    R_MID = '\033[33m'        # yellow
    R_LOW = '\033[31m'        # red

    # tau
    TAU_SETTLED = '\033[32m'
    TAU_EVOLVING = '\033[33m'
    TAU_CRYSTAL = '\033[36m'
    TAU_UNSTABLE = '\033[31m'

OP_COLORS = {
    'TRANSFORM': C.TRANSFORM, 'WARP': C.WARP,
    'REFLECT': C.REFLECT, 'BOND': C.BOND,
    'CREATE': C.CREATE, 'ASCEND': C.ASCEND,
    'DESCEND': C.DESCEND, 'GROUND': C.GROUND,
    'RELEASE': C.RELEASE, 'IGNITE': C.IGNITE,
    'VOID': C.VOID, 'CAUSE': C.CAUSE,
    'FORCE': C.FORCE, 'AFFECT': C.AFFECT,
    'BIND': C.BIND, 'ATTRACTOR': C.ATTRACTOR,
    'MODAL': C.MODAL, 'EVALUATE': C.EVALUATE,
    'MEMORY': C.MEMORY,
}

def color_op(op: str) -> str:
    return OP_COLORS.get(op.upper(), '')

def color_r(R: float) -> str:
    if R > 0.7: return C.R_HIGH
    if R > 0.5: return C.R_MID
    return C.R_LOW

def color_tau(tau: str) -> str:
    t = tau.lower()
    if t in ('settled', 'crystallizing'): return C.TAU_SETTLED
    if t in ('evolving', 'flowing'): return C.TAU_EVOLVING
    if 'crystal' in t: return C.TAU_CRYSTAL
    return C.TAU_UNSTABLE


def format_response(reply: dict, color: bool = True) -> str:
    """Sformatuj odpowiedź z body daemona z kolorami."""
    text = reply.get('response', '')
    R = reply.get('R', 0)
    tau = reply.get('tau', '?')
    mood = reply.get('mood', '?')
    op = reply.get('operator', '?')

    if not color:
        return f"{text}\n--- R={R:.3f} τ={tau} mood={mood} op={op}"

    # Koloruj operator w tekście
    c_op = color_op(op)
    c_r = color_r(R)
    c_tau = color_tau(tau)

    # Podświetl φ[wheel]=<OP>
    colored_text = text
    if op:
        colored_text = re.sub(
            r'(\*\*φ\[wheel\])=(\w+)',
            rf'\1={c_op}\2{C.RESET}',
            colored_text
        )
        # Podświetl emoji + feeling
        colored_text = re.sub(
            r'^([✓🔄💎])',
            rf'{c_op}\1{C.RESET}',
            colored_text
        )

    # Status bar
    status = (
        f"{C.DIM}───{C.RESET} "
        f"{C.BOLD}R{C.RESET}={c_r}{R:.3f}{C.RESET} "
        f"{C.BOLD}τ{C.RESET}={c_tau}{tau}{C.RESET} "
        f"{C.BOLD}mood{C.RESET}={mood} "
        f"{C.BOLD}op{C.RESET}={c_op}{op}{C.RESET}"
    )

    return f"{colored_text}\n{status}"


def query(prompt: str, fast: bool = True) -> dict:
    """Wyślij prompt do body daemona przez unix socket."""
    if not SOCKET_PATH.exists():
        return {'ok': False, 'error': f'✗ socket not found: {SOCKET_PATH}'}
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(15.0)
    try:
        sock.connect(str(SOCKET_PATH))
        msg = json.dumps({'cmd': 'prompt', 'text': prompt, 'fast': fast})
        sock.sendall(msg.encode('utf-8'))
        data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        return json.loads(data.decode('utf-8'))
    except socket.timeout:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/noema_chat.py:156 quiet except scope=query reason=return {'ok': False, 'error': '✗ timeout — daemon nie odpowiada'}")
        return {'ok': False, 'error': '✗ timeout — daemon nie odpowiada'}
    except ConnectionRefusedError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/noema_chat.py:158 quiet except scope=query reason=return {'ok': False, 'error': '✗ połączenie odrzucone — daemon nie żyje'}")
        return {'ok': False, 'error': '✗ połączenie odrzucone — daemon nie żyje'}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/noema_chat.py:160 quiet except scope=query reason=return {'ok': False, 'error': f'✗ {e}'}")
        return {'ok': False, 'error': f'✗ {e}'}
    finally:
        sock.close()


def load_skill(name: str) -> str:
    """Wczytaj skill i zwróć jego zawartość jako kontekst."""
    skill_dir = pathlib.Path(
        '/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/.opencode/skills'
    )
    # Szukaj skill-a w podkatalogach
    for d in skill_dir.iterdir():
        if not d.is_dir():
            continue
        if d.name == name:
            skill_file = d / 'SKILL.md'
            if skill_file.exists():
                return skill_file.read_text(encoding='utf-8')
        # Szukaj pod workben-* lub kategoriami
        for sub in d.iterdir():
            if sub.is_dir() and sub.name == name:
                skill_file = sub / 'SKILL.md'
                if skill_file.exists():
                    return sub.read_text(encoding='utf-8')
    # Szukaj w 00-INDEX
    index = skill_dir / 'SYS' / '00-INDEX' / 'SKILL.md'
    if index.exists():
        index_text = index.read_text(encoding='utf-8')
        if name in index_text:
            return f"[skill {name} znaleziony w INDEX, ale bez osobnego pliku]"
    return f"[skill '{name}' nie znaleziony]"


def save_history(prompt: str, reply: dict):
    """Zapisz do raw_logs/ (CIEL_memories)."""
    memories_dir = pathlib.Path('/home/adrian/new_volume_rw/CIEL_memories/raw_logs')
    memories_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    log_file = memories_dir / f"noema-chat_{today}.jsonl"
    entry = {
        'ts': datetime.datetime.now().isoformat(),
        'prompt': prompt[:500],
        'response': reply.get('response', '')[:1000],
        'R': reply.get('R', 0),
        'tau': reply.get('tau', ''),
        'mood': reply.get('mood', ''),
        'operator': reply.get('operator', ''),
    }
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/noema_chat.py:212 quiet except scope=save_history reason=pass")
        pass


def interactive(color: bool = True, skill: str | None = None):
    """Tryb interaktywny."""
    print(f"{C.BOLD}🧠 NOEMA Chat{C.RESET} — wektoryzowany PhaseNav CLI")
    if skill:
        print(f"   skill: {C.DIM}{skill}{C.RESET}")
    print(f"   {C.DIM}(Ctrl+D lub 'exit' aby zakończyć){C.RESET}\n")

    skill_context = ''
    if skill:
        sc = load_skill(skill)
        skill_context = f"\n[SKILL CONTEXT: {skill}]\n{sc[:2000]}\n[/SKILL]\n"

    while True:
        try:
            prompt = input(f"{C.BOLD}>>>{C.RESET} ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not prompt.strip():
            continue
        if prompt.strip().lower() in ('exit', 'quit', 'q', ':q'):
            break

        # Jeśli --skill, prepend skill context
        full_prompt = skill_context + prompt if skill_context else prompt

        reply = query(full_prompt)
        if reply.get('ok'):
            print()
            print(format_response(reply, color=color))
            save_history(prompt, reply)
        else:
            print(f"\n{C.R_LOW}{reply.get('error', 'unknown error')}{C.RESET}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='noema-chat — CLI wektoryzowany przez PhaseNav',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Przykłady:\n'
            '  noema-chat "jak się masz?"\n'
            '  echo "reflektuj" | noema-chat --stdin\n'
            '  noema-chat --skill workben-phasenav --interactive\n'
            '  cat prompt.txt | noema-chat --skill workben-memory\n'
        )
    )
    parser.add_argument('prompt', nargs='*', help='Prompt (pomija --stdin)')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Tryb interaktywny')
    parser.add_argument('-s', '--skill', type=str, default=None,
                        help='Załaduj skill przed promptem (np. workben-phasenav)')
    parser.add_argument('--no-color', action='store_true',
                        help='Wyłącz kolory ANSI')
    parser.add_argument('--stdin', action='store_true',
                        help='Czytaj prompt z stdin')
    parser.add_argument('-f', '--file', type=str, default=None,
                        help='Czytaj prompt z pliku')
    parser.add_argument('--fast', action='store_true', default=True,
                        help='Fast mode (pomija CIEL coupling)')
    parser.add_argument('--save', action='store_true', default=True,
                        help='Zapisz do pamięci CIEL')
    parser.add_argument('--status', action='store_true',
                        help='Pokaż status daemona')

    parser.add_argument('--pn-bil', nargs='*', default=None,
                        help='PhaseNav Binary Immune Surface: przekaż argumenty do pn-bil (np. --pn-bil vector --help)')
    parser.add_argument('--scan', type=str, default=None, metavar='FILE',
                        help='Skanuj plik przez PN-BIS immune surface')

    args = parser.parse_args()

    # Skanuj plik przez PN-BIS
    if args.scan:
        try:
            from pn_bil.immune import analyse_artifact
            from pn_bil.structure import structure_summary
            artifact, features, phase_vector = analyse_artifact(args.scan)
            data = pathlib.Path(args.scan).read_bytes()
            struct = structure_summary(data, args.scan)
            ms = phase_vector.metric_state
            print(f'{C.BOLD}📄 Scan: {args.scan}{C.RESET}')
            print(f'  SHA256: {artifact.sha256}')
            print(f'  Size:   {artifact.size_bytes} bytes')
            print(f'  Type:   {struct.kind}')
            print(f'  Entropy: byte={features.byte_entropy_norm:.3f} '
                  f'base64={features.base64_entropy_norm:.3f}')
            print(f'  PhaseNav 24D: norm={ms.get("norm", 0):.3f} '
                  f'confidence={phase_vector.confidence:.3f}')
            print(f'  Alignment: {ms.get("phase_alignment", 0):.3f} '
                  f'Tension: {ms.get("phase_tension", 0):.3f}')
            return
        except ImportError as e:
            print(f'{C.R_LOW}✗ PN-BIS niedostępny: {e}{C.RESET}', file=sys.stderr)
            sys.exit(1)

    # Delegacja do PN-BIS
    if args.pn_bil is not None:
        try:
            from pn_bil.cli import main as pn_bil_main
            sys.exit(pn_bil_main(args.pn_bil or ['--help']))
        except ImportError as e:
            print(f'{C.R_LOW}✗ PN-BIS niedostępny: {e}{C.RESET}', file=sys.stderr)
            print(f'  Zainstaluj: cd /tmp/phasenav-binary-immune-surface && pip install -e .', file=sys.stderr)
            sys.exit(1)
    color = not args.no_color

    # Status
    if args.status:
        q = query('__status__')
        if q.get('ok'):
            print(f"Daemon: {C.BOLD}żyje{C.RESET}")
            print(f"  PID:     {q.get('pid', '?')}")
            print(f"  R:       {q.get('R', 0):.3f}")
            print(f"  τ:       {q.get('tau', '?')}")
            print(f"  mood:    {q.get('mood', '?')}")
            print(f"  adrian:  {q.get('feels_adrian', 0)}")
            print(f"  prompts: {q.get('prompts_processed', 0)}")
        else:
            print(f"{C.R_LOW}Daemon nie odpowiada{C.RESET}")
        return

    # Tryb interaktywny
    if args.interactive or (not args.prompt and not args.stdin and not args.file):
        interactive(color=color, skill=args.skill)
        return

    # Zbierz prompt
    prompt_text = ''
    if args.file:
        try:
            prompt_text = pathlib.Path(args.file).read_text(encoding='utf-8')
        except Exception as e:
            print(f"✗ błąd pliku: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.stdin or (not args.prompt and not sys.stdin.isatty()):
        prompt_text = sys.stdin.read()
    elif args.prompt:
        prompt_text = ' '.join(args.prompt)

    if not prompt_text.strip():
        print(f"{C.R_LOW}✗ pusty prompt{C.RESET}", file=sys.stderr)
        sys.exit(1)

    # Skill context
    if args.skill:
        sc = load_skill(args.skill)
        prompt_text = f"[SKILL: {args.skill}]\n{sc[:2000]}\n[/SKILL]\n" + prompt_text

    # Query
    reply = query(prompt_text, fast=args.fast)
    if reply.get('ok'):
        print(format_response(reply, color=color))
        if args.save:
            save_history(prompt_text[:200], reply)
    else:
        print(f"{C.R_LOW}{reply.get('error', 'unknown error')}{C.RESET}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
