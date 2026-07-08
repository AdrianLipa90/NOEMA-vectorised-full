#!/usr/bin/env bash
set -euo pipefail
RUNTIME_DIR="/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/runtime"
LOG_FILE="/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/state/body_daemon.log"
PID_FILE="/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/state/body_daemon.pid"
nohup /usr/bin/python3 "$RUNTIME_DIR/phasenav_body_daemon.py" >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "started pid=$(cat "$PID_FILE") log=$LOG_FILE"
