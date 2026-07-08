#!/bin/bash
cd /home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA
export PYTHONPATH="/home/adrian/.local/lib/python3.12/site-packages:$PYTHONPATH"
nohup python3 -u -c "
import sys, time, numpy as np
sys.path.insert(0, 'src')
from ciel_geometry.ebpf_noema_loader import EBPFSensor
from ciel_geometry.noema_surface_mmap import open_surface, DEFAULT_SURFACE_ROOT as ROOT

surface = open_surface(ROOT)
sensor = EBPFSensor()
sensor.start()
print('[eBPF] daemon started', flush=True)
while True:
    snap = sensor.snapshot()
    sensor.write_surface(surface, snap)
    if snap['tick'] % 5 == 0:
        R = float(abs(np.mean(np.exp(1j * snap['phi']))))
        print(f'[eBPF] t={snap[\"tick\"]} R={R:.4f} CS={snap[\"raw\"].get(\"ctx_switches\",0):.0f} F={[round(float(f),2) for f in snap[\"flavor\"]]}', flush=True)
    time.sleep(1.0)
" > /dev/shm/ciel_noema/ebpf_sensor.log 2>&1 &
echo "eBPF PID: $!"
