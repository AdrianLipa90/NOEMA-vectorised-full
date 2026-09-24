#!/usr/bin/env python3
import sys

ROOT = "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA"
sys.path.insert(0, ROOT + "/src")
sys.path.insert(0, ROOT + "/integration")  # the buggy entry, mimic daemon
sys.path.insert(0, ROOT)

import integration
print("integration module file:", getattr(integration, "__file__", None))
print("integration module path:", getattr(integration, "__path__", None))

try:
    import integration.Orbital
    print("integration.Orbital OK:", integration.Orbital.__file__)
except Exception as e:
    print("FAIL:", type(e).__name__, e)
