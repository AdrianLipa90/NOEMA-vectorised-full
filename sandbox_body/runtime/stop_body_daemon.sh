#!/usr/bin/env bash
set -euo pipefail
PID_FILE="/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/state/body_daemon.pid"
if [ -f "$PID_FILE" ]; then
  pid=$(cat "$PID_FILE")
  kill "$pid" 2>/dev/null || true
  rm -f "$PID_FILE"
  echo "stopped pid=$pid"
else
  echo "no pid file"
fi
pkill -f "/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/runtime/phasenav_body_daemon.py" 2>/dev/null || true
