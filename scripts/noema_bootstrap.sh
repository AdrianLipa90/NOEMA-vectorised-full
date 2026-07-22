#!/bin/bash
# NOEMA bootstrap — uruchamiany przy starcie systemu przez systemd
set -e

WORKSPACE_SRC="/home/adrian/new_volume_rw/samsung/zipy datowane/ciel_apocalyptos"
WORKSPACE_TMP="/tmp/noema_surface_workspace/NOEMA_LOCAL_ROOT"

echo "[bootstrap] NOEMA boot: $(date)"

# 1. Ensure /tmp symlink for surface workspace
mkdir -p "$WORKSPACE_TMP/head"
if [ ! -L "$WORKSPACE_TMP/head/NoemaSurface" ]; then
    ln -sf "$WORKSPACE_SRC/surface/head/NoemaSurface" "$WORKSPACE_TMP/head/NoemaSurface"
    echo "[bootstrap] symlink created: head/NoemaSurface"
fi

# 2. Copy monolith if missing
MONOLITH_SRC="$WORKSPACE_SRC/surface/NOEMA_LOCAL_ROOT/noema_surface_codex_monolith.py"
MONOLITH_DST="$WORKSPACE_TMP/noema_surface_codex_monolith.py"
if [ ! -f "$MONOLITH_DST" ]; then
    cp "$MONOLITH_SRC" "$MONOLITH_DST"
    echo "[bootstrap] monolith copied"
fi

# 3. Ensure surface dirs
mkdir -p /dev/shm/ciel_noema/htri
mkdir -p /dev/shm/ciel_noema/phasenav

echo "[bootstrap] done"
