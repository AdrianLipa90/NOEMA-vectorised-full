#!/usr/bin/env bash
set -euo pipefail

NOEMA_ROOT="/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA"
export PYTHONPATH="$NOEMA_ROOT/src:$NOEMA_ROOT/runtime:$NOEMA_ROOT/scripts"
export PYTHONUNBUFFERED=1

echo "[NOEMA] starting system daemons..."

mkdir -p "$NOEMA_ROOT/runtime/logs" "$NOEMA_ROOT/runtime/portal_logs"

python3 -c "from ciel_geometry.noema_surface_mmap import ensure_surface; ensure_surface()" 2>/dev/null || true

# portal
if ! ss -tlnp 2>/dev/null | grep -q :18888; then
    echo "  portal :18888"
    nohup python3 "$NOEMA_ROOT/scripts/noema_portal_daemon.py" --host 127.0.0.1 --port 18888 \
        > "$NOEMA_ROOT/runtime/portal_logs/portal.stdout.log" 2>&1 &
    disown
fi

# headless
if [ ! -S /run/user/1000/noema/ciel_headless.sock ] && [ ! -S /dev/shm/ciel_noema/ciel_headless.sock ]; then
    echo "  CIEL headless (unix socket)"
    CIEL_HEADLESS_PIPELINE_MODE=ciel_canonical_topology_only \
    nohup "$NOEMA_ROOT/.venv/bin/python3" "$NOEMA_ROOT/scripts/ciel_headless_daemon.py" \
        > "$NOEMA_ROOT/runtime/logs/headless.log" 2>&1 &
    disown
fi

# kuramoto
echo "  kuramoto daemon"
nohup "$NOEMA_ROOT/.venv/bin/python3" "$NOEMA_ROOT/scripts/ciel_noema_kuramoto_daemon.py" --interval 0.2 --dt 0.05 \
    > "$NOEMA_ROOT/runtime/logs/kuramoto.log" 2>&1 &
disown

# subconscious
echo "  subconscious daemon"
nohup "$NOEMA_ROOT/.venv/bin/python3" "$NOEMA_ROOT/scripts/ciel_noema_subconscious_daemon.py" \
    > "$NOEMA_ROOT/runtime/logs/subconscious.log" 2>&1 &
disown

# neutrino
echo "  neutrino daemon"
nohup "$NOEMA_ROOT/.venv/bin/python3" "$NOEMA_ROOT/scripts/ciel_noema_neutrino_daemon.py" \
    > "$NOEMA_ROOT/runtime/logs/neutrino.log" 2>&1 &
disown

# phasenav
echo "  phasenav daemon"
nohup "$NOEMA_ROOT/.venv/bin/python3" "$NOEMA_ROOT/scripts/ciel_noema_phasenav_daemon.py" --node cold \
    > "$NOEMA_ROOT/runtime/logs/phasenav.log" 2>&1 &
disown

# memory bind
echo "  memory bind daemon"
nohup "$NOEMA_ROOT/.venv/bin/python3" "$NOEMA_ROOT/scripts/ciel_memory_bind_daemon.py" \
    > "$NOEMA_ROOT/runtime/logs/memory_bind.log" 2>&1 &
disown

# CIEL agent
echo "  CIEL agent daemon"
nohup "$NOEMA_ROOT/.venv/bin/python3" "$NOEMA_ROOT/scripts/ciel_agent_daemon.py" \
    > "$NOEMA_ROOT/runtime/logs/agent.log" 2>&1 &
disown

# web research
echo "  web research daemon"
nohup "$NOEMA_ROOT/.venv/bin/python3" "$NOEMA_ROOT/scripts/ciel_web_research_daemon.py" --interval 1800 \
    > "$NOEMA_ROOT/runtime/logs/web_research.log" 2>&1 &
disown

echo "[NOEMA] all daemons started"
echo "  portal: http://127.0.0.1:18888"
echo ""
echo "stop: pkill -f 'noema_portal_daemon|ciel_headless_daemon|kuramoto_daemon|subconscious_daemon|neutrino_daemon|phasenav_daemon|memory_bind_daemon|agent_daemon|web_research_daemon'"
