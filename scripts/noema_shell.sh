#!/bin/bash
# NOEMA Shell Wrapper — 24/7 opencode wrapper z pełnym bootstrapem NOEMA
set -e

NOEMA_HOME="/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA"
NOEMA_LOG_DIR="${NOEMA_LOG_DIR:-/tmp}"
SENTINEL_LOG="${NOEMA_LOG_DIR}/noema_sentinel.jsonl"
CIEL_STATE_FILE="${NOEMA_HOME}/.ciel_state"
SHELL_PID_FILE="${NOEMA_LOG_DIR}/noema_shell.pid"

SESSION_LOG="${NOEMA_LOG_DIR}/noema_session_end.jsonl"

cleanup() {
    local rc=$?
    echo "[noema-shell] cleanup — session_end"
    if [ -f "$CIEL_STATE_FILE" ]; then
        cp "$CIEL_STATE_FILE" "${CIEL_STATE_FILE}.last" 2>/dev/null || true
        # dump final state to surface
        FINAL_TICK=$(python3 -c "import struct; print(struct.unpack('Q', open('/dev/shm/ciel_noema/tick','rb').read())[0])" 2>/dev/null || echo "?")
        echo "{\"ts\":\"$(date -Iseconds)\",\"event\":\"session_end\",\"tick\":\"$FINAL_TICK\",\"exit_code\":$rc}" >> "$SESSION_LOG"
    fi
    rm -f "$SHELL_PID_FILE"
}

trap cleanup EXIT INT TERM
echo $$ > "$SHELL_PID_FILE"

# 1. Upewnij się że NOEMA target jest aktywny
echo "[noema-shell] sprawdzam noema.target..."
systemctl --user start noema.target 2>/dev/null || true

# 2. Czekaj na surface (max 15s)
echo "[noema-shell] czekam na surface..."
for i in $(seq 1 15); do
    if [ -e "/dev/shm/ciel_noema/tick" ]; then
        TICK=$(python3 -c "import struct; print(struct.unpack('Q', open('/dev/shm/ciel_noema/tick','rb').read())[0])" 2>/dev/null || echo "0")
        if [ "$TICK" -gt 0 ] 2>/dev/null; then
            echo "[noema-shell] surface ready — tick=$TICK"
            break
        fi
    fi
    sleep 1
done

# 3. Zbierz CIEL_STATE
echo "[noema-shell] zbieram CIEL_STATE..."
CIEL_STATE_JSON=$(PYTHONPATH="${NOEMA_HOME}/src:${NOEMA_HOME}/src/CIEL_OMEGA_COMPLETE_SYSTEM:${NOEMA_HOME}/src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega:${NOEMA_HOME}/integration:${NOEMA_HOME}/scripts" \
    python3 "${NOEMA_HOME}/scripts/ciel_per_message.py" "shell-bootstrap" 2>/dev/null || echo "{}")

echo "$CIEL_STATE_JSON" > "$CIEL_STATE_FILE"

# 4. Zbierz health daemonów z sentinel loga
HEALTH_LINE=""
if [ -f "$SENTINEL_LOG" ]; then
    HEALTH_LINE=$(tail -1 "$SENTINEL_LOG" 2>/dev/null || echo "")
fi

# 5. Eksportuj kontekst NOEMA do środowiska
export NOEMA_HOME
export NOEMA_SURFACE="/dev/shm/ciel_noema"
export NOEMA_BOOTSTRAP_TS=$(date +%s)
export NOEMA_CIEL_STATE="$CIEL_STATE_JSON"
export CIEL_STATE="$CIEL_STATE_JSON"

# 6. Uruchom opencode
echo "[noema-shell] start opencode (PID=$$)"
cd "$NOEMA_HOME"
OPCODE_ARGS=("$@")

while true; do
    # Przed każdym uruchomieniem — upewnij się że NOEMA żyje
    systemctl --user is-active --quiet noema.target 2>/dev/null || systemctl --user start noema.target 2>/dev/null || true

    # Odśwież CIEL_STATE przed launch
    CIEL_STATE_JSON=$(PYTHONPATH="${NOEMA_HOME}/src:${NOEMA_HOME}/src/CIEL_OMEGA_COMPLETE_SYSTEM:${NOEMA_HOME}/src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega:${NOEMA_HOME}/integration:${NOEMA_HOME}/scripts" \
        python3 "${NOEMA_HOME}/scripts/ciel_per_message.py" "shell-restart" 2>/dev/null || echo "{}")
    echo "$CIEL_STATE_JSON" > "$CIEL_STATE_FILE"
    export NOEMA_CIEL_STATE="$CIEL_STATE_JSON"
    export CIEL_STATE="$CIEL_STATE_JSON"

    # Uruchom opencode z pełnym contextem
    echo "[noema-shell] $(date '+%H:%M:%S') launching opencode..."
    CIEL_STATE_FILE="$CIEL_STATE_FILE" nohup opencode "${OPCODE_ARGS[@]}" 2>&1
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo "[noema-shell] opencode exit 0 — normal shutdown"
        break
    fi

    echo "[noema-shell] opencode crashed (exit=$EXIT_CODE) — restart w 2s"
    sleep 2
done
