#!/usr/bin/env python3
import json, sys
from pathlib import Path
p = Path("/dev/shm/ciel_noema/actuator/result.json")
d = json.loads(p.read_bytes())
print(json.dumps(d, indent=2))
