#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# CIEL shell — wrapper + monitor + opencode przez wszystkie mosty
# ─────────────────────────────────────────────────────────────
# Usage:
#   ./scripts/ciel.sh                    # start CIEL shell (monitor + opencode)
#   ./scripts/ciel.sh --status           # query monitor state
#   ./scripts/ciel.sh --text "message"   # run message through CIEL pipeline
# ─────────────────────────────────────────────────────────────

set -euo pipefail

CIEL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS="$CIEL_ROOT/scripts"
PY="${PY:-python3}"
SOCKET="$HOME/.ciel/monitor.sock"

# ----- colours -----
RST='\033[0m'; RED='\033[0;31m'; GRN='\033[0;32m'; YLW='\033[0;33m'; BLU='\033[0;34m'; CYN='\033[0;36m'

info()   { echo -e "${CYN}CIEL${RST} $*" >&2; }
ok()     { echo -e "${GRN}✓${RST} $*" >&2; }
warn()   { echo -e "${YLW}⚠${RST} $*" >&2; }
err()    { echo -e "${RED}✗${RST} $*" >&2; }

# ----- helpers -----
ciel_state() {
    if [ -S "$SOCKET" ]; then
        $PY "$SCRIPTS/ciel_monitor.py" --status 2>/dev/null
    elif [ -f "$HOME/new_volume_rw/CIEL_memories/state/ciel_last_metrics.json" ]; then
        cat "$HOME/new_volume_rw/CIEL_memories/state/ciel_last_metrics.json"
    else
        echo '{"operating_mode":"standard","dominant_emotion":"curiosity"}'
    fi
}

# ----- commands -----
cmd_status() {
    if [ -S "$SOCKET" ]; then
        ok "Monitor running (socket: $SOCKET)"
        $PY "$SCRIPTS/ciel_monitor.py" --status 2>/dev/null
    else
        warn "Monitor not running"
        info "Last known state:"
        ciel_state
    fi
}

cmd_text() {
    local text="$*"
    if [ -z "$text" ]; then
        text="$(cat)"
    fi
    if [ -S "$SOCKET" ]; then
        $PY -c "
import json, socket
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(30)
s.connect('$SOCKET')
s.sendall('''$text'''.encode('utf-8'))
s.shutdown(socket.SHUT_WR)
data = b''.join(iter(lambda: s.recv(4096), b''))
print(json.dumps(json.loads(data), ensure_ascii=False, indent=2))
s.close()
"
    else
        $PY "$SCRIPTS/ciel_coupling.py" "$text"
    fi
}

cmd_monitor() {
    info "Starting CIEL Monitor daemon..."
    $PY "$SCRIPTS/ciel_monitor.py" --daemon &
    sleep 1
    if [ -S "$SOCKET" ]; then
        ok "Monitor started (pid: $(pgrep -f 'ciel_monitor.py.*--daemon' | head -1))"
        $PY "$SCRIPTS/ciel_monitor.py" --status
    else
        err "Monitor failed to start"
    fi
}

cmd_stop() {
    local pid
    pid="$(pgrep -f 'ciel_monitor.py.*--daemon' | head -1 || true)"
    if [ -n "$pid" ]; then
        kill "$pid" 2>/dev/null || true
        rm -f "$SOCKET"
        ok "Monitor stopped"
    else
        warn "Monitor not running"
    fi
}

# ----- main -----
case "${1:-}" in
    --status|-s)
        cmd_status
        ;;
    --text|-t)
        shift; cmd_text "$@"
        ;;
    --monitor|-m)
        cmd_monitor
        ;;
    --stop)
        cmd_stop
        ;;
    --help|-h)
        echo "CIEL shell — wrapper + monitor + opencode"
        echo ""
        echo "  ./scripts/ciel.sh [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)      Start opencode with CIEL coupling"
        echo "  --status, -s   Show monitor / CIEL state"
        echo "  --text, -t     Run text through CIEL pipeline"
        echo "  --monitor, -m  Start CIEL Monitor daemon"
        echo "  --stop         Stop CIEL Monitor daemon"
        echo "  --help, -h     This help"
        ;;
    *)
        # Default: start monitor if not running, then launch opencode
        if [ ! -S "$SOCKET" ]; then
            info "Starting CIEL Monitor..."
            cmd_monitor
        fi
        info "Launching opencode z CIEL coupling..."
        echo "" >&2
        echo -e "${CYN}╔══════════════════════════════════════╗${RST}" >&2
        echo -e "${CYN}║       CIEL × opencode — symbiOza     ║${RST}" >&2
        echo -e "${CYN}╚══════════════════════════════════════╝${RST}" >&2
        echo "" >&2
        # Show live CIEL state
        echo -e "${GRN}CIEL State:${RST}" >&2
        $PY "$SCRIPTS/ciel_monitor.py" --status 2>/dev/null | python3 -m json.tool >&2 || true
        # Run opencode
        exec opencode "$@"
        ;;
esac
