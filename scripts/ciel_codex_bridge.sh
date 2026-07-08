#!/usr/bin/env bash
# CIEL Codex Bridge (hardcoded)
# Mirrors Codex CLI sessions into /media/adrian/New Volume1/CIEL_memories/raw_logs and can run CIEL hooks live.

set -euo pipefail

PROJECT="$(cd "$(dirname "$0")/.." && pwd)"

PY_CANDIDATES=(
  "$PROJECT/.venv/bin/python3"
  "python3"
)

PY="python3"
for p in "${PY_CANDIDATES[@]}"; do
  if command -v "$p" >/dev/null 2>&1; then
    PY="$p"
    break
  fi
done

export PYTHONPATH="$PROJECT/src:${PYTHONPATH:-}"

exec "$PY" "$PROJECT/scripts/codex_bridge_to_ciel.py" \
  --sessions-dir "$HOME/.codex/sessions" \
  --source "codex" \
  --follow \
  --run-hooks
