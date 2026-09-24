#!/usr/bin/env bash
set -euo pipefail

echo "[NOEMA] stopping all daemons..."
pkill -f 'noema_portal_daemon' 2>/dev/null || true
pkill -f 'ciel_headless_daemon' 2>/dev/null || true
pkill -f 'kuramoto_daemon' 2>/dev/null || true
pkill -f 'subconscious_daemon' 2>/dev/null || true
pkill -f 'neutrino_daemon' 2>/dev/null || true
pkill -f 'phasenav_daemon' 2>/dev/null || true
pkill -f 'memory_bind_daemon' 2>/dev/null || true
pkill -f 'agent_daemon' 2>/dev/null || true
pkill -f 'web_research_daemon' 2>/dev/null || true
echo "[NOEMA] done"
