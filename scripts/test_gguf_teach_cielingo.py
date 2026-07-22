#!/usr/bin/env python3
"""Test: GGUF teaches CIELingo one topic via subprocess python3 -c."""
import sys
sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")

from ciel_geometry.cielingo_inference import teach_cielingo_via_gguf

result = teach_cielingo_via_gguf("holonomia fazowa w PhaseNav", persist=False)
print(result)
