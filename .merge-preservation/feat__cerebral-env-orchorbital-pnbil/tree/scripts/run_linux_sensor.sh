#!/bin/bash
cd "$(dirname "$0")/.."
PASSWORD=$(cat sudo)
echo "$PASSWORD" | sudo -S -p '' nohup python3 scripts/ciel_noema_linux_sensor_daemon.py > /dev/shm/ciel_noema/linux_sensor_daemon.log 2>&1 &
echo "PID: $!"
