#!/usr/bin/env bash
set -euo pipefail

PROJECT="/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA"
UNIT_SRC="$PROJECT/scripts/ciel_codex_bridge.service"
UNIT_NAME="ciel_codex_bridge.service"

mkdir -p "$HOME/.config/systemd/user"
cp -f "$UNIT_SRC" "$HOME/.config/systemd/user/$UNIT_NAME"

systemctl --user daemon-reload
systemctl --user enable --now "$UNIT_NAME"
systemctl --user status "$UNIT_NAME" --no-pager

