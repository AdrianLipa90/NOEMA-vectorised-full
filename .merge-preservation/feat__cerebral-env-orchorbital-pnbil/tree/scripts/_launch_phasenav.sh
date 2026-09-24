#!/bin/bash
cd /home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA
exec setsid python3 -u scripts/ciel_noema_phasenav_daemon.py --interval 5.0 > /dev/shm/ciel_noema/phasenav_daemon.log 2>&1
