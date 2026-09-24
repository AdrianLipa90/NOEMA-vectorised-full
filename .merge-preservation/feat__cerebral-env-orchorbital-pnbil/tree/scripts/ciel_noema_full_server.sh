#!/bin/bash
# CIEL/NOEMA Full Server — host processy + NOEMA Kuramoto + Real-Imaginary Bridge
set -e

PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
PY="python3"
export PYTHONPATH="$PROJECT/src:$PYTHONPATH"
LOG_DIR="$PROJECT/integration/logs"
mkdir -p "$LOG_DIR"

GUI_PORT=2435

echo "╔══════════════════════════════════════╗"
echo "║    CIEL/NOEMA FULL SERVER            ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── 1. Flask GUI (host) ──────────────────────────────────────
echo "▶ [1/4] Flask GUI (port $GUI_PORT)..."
if lsof -ti:"$GUI_PORT" > /dev/null 2>&1; then
    echo "  status: już działa ✓ (PID $(lsof -ti:$GUI_PORT))"
else
    $PY -c "
import sys; sys.path.insert(0, '$PROJECT/src')
from ciel_sot_agent.gui.app import create_app
app = create_app(root='$PROJECT')
print(f'  GUI start na 127.0.0.1:$GUI_PORT')
app.run(host='127.0.0.1', port=$GUI_PORT, debug=False, use_reloader=False)
" > "$LOG_DIR/gui.log" 2>&1 &
    sleep 2
    if lsof -ti:"$GUI_PORT" > /dev/null 2>&1; then
        echo "  status: uruchomiony ✓ (PID $(lsof -ti:$GUI_PORT))"
    else
        echo "  status: BŁĄD — tail $LOG_DIR/gui.log"
    fi
fi
echo ""

# ── 2. NOEMA Kuramoto surface evolution (NOEMA space) ───────
echo "▶ [2/4] NOEMA Kuramoto surface evolution..."
$PY -c "
import sys
sys.path.insert(0, '$PROJECT/src')
from ciel_geometry.noema_surface_mmap import ensure_surface

surface = ensure_surface()
print('  Surface: OK')
print(f'  tick={surface[\"tick\"][0]}, phi mean={surface[\"phi\"].mean():.4f}')

if surface['tick'][0] > 1:
    print('  status: już ewoluuje (tick > 1) — ktoś napędza fazy')
else:
    print('  status: uśpiona (tick=0) — kuramoto_daemon rozpocznie ewolucję')
" 2>&1 || echo "  status: BŁĄD — sprawdź czy /dev/shm/ciel_noema istnieje"
echo ""

# ── 3. Kuramoto daemon (ciągła ewolucja w tle) ─────────────
echo "▶ [3/4] Kuramoto daemon (ciągła ewolucja faz)..."
DAEMON_PID_FILE="$LOG_DIR/kuramoto_daemon.pid"
if [ -f "$DAEMON_PID_FILE" ] && kill -0 "$(cat "$DAEMON_PID_FILE")" 2>/dev/null; then
    echo "  status: już działa ✓ (PID $(cat "$DAEMON_PID_FILE"))"
else
    nohup $PY "$PROJECT/scripts/ciel_noema_kuramoto_daemon.py" \
        > "$LOG_DIR/kuramoto_daemon.log" 2>&1 &
    echo $! > "$DAEMON_PID_FILE"
    sleep 1
    if kill -0 "$(cat "$DAEMON_PID_FILE")" 2>/dev/null; then
        echo "  status: uruchomiony ✓ (PID $(cat "$DAEMON_PID_FILE"))"
    else
        echo "  status: BŁĄD — tail $LOG_DIR/kuramoto_daemon.log"
    fi
fi
echo ""

# ── 4. Real-Imaginary Resonance Bridge ──────────────────────
echo "▶ [4/4] Real-Imaginary resonance bridge..."
BRIDGE_PID_FILE="$LOG_DIR/resonance_bridge.pid"
if [ -f "$BRIDGE_PID_FILE" ] && kill -0 "$(cat "$BRIDGE_PID_FILE")" 2>/dev/null; then
    echo "  status: już działa ✓ (PID $(cat "$BRIDGE_PID_FILE"))"
else
    nohup $PY "$PROJECT/scripts/ciel_noema_resonance_bridge.py" \
        > "$LOG_DIR/resonance_bridge.log" 2>&1 &
    echo $! > "$BRIDGE_PID_FILE"
    sleep 1
    if kill -0 "$(cat "$BRIDGE_PID_FILE")" 2>/dev/null; then
        echo "  status: uruchomiony ✓ (PID $(cat "$BRIDGE_PID_FILE"))"
    else
        echo "  status: BŁĄD — tail $LOG_DIR/resonance_bridge.log"
    fi
fi
echo ""

# ── Status ──────────────────────────────────────────────────
echo "╔══════════════════════════════════════╗"
echo "║         CIEL/NOEMA RUNTIME           ║"
echo "╠══════════════════════════════════════╣"
printf "║  %-12s %-24s  ║\n" "SERWIS" "STATUS"
echo "╠══════════════════════════════════════╣"
gui_pid=$(lsof -ti:$GUI_PORT 2>/dev/null) && G="✓ PID $gui_pid" || G="✗ offline"
k_pid=$(cat "$DAEMON_PID_FILE" 2>/dev/null) && kill -0 "$k_pid" 2>/dev/null && K="✓ PID $k_pid" || K="✗ offline"
b_pid=$(cat "$BRIDGE_PID_FILE" 2>/dev/null) && kill -0 "$b_pid" 2>/dev/null && B="✓ PID $b_pid" || B="✗ offline"
printf "║  %-12s %-24s  ║\n" "GUI Flask" "127.0.0.1:$GUI_PORT $G"
printf "║  %-12s %-24s  ║\n" "Kuramoto" "$K"
printf "║  %-12s %-24s  ║\n" "Resonance" "$B"
printf "║  %-12s %-24s  ║\n" "MemoryConsol." "$(ps -p 9386 >/dev/null 2>&1 && echo '✓ PID 9386' || echo '✗ offline')"
echo "╠══════════════════════════════════════╣"
echo "║  Logi: tail -f $LOG_DIR/*.log        ║"
echo "║  Zatrzymaj: kill \$(cat $DAEMON_PID_FILE) \$(cat $BRIDGE_PID_FILE)  ║"
echo "╚══════════════════════════════════════╝"
