#!/bin/bash
# Start NOEMA site preview server
cd "$(dirname "$0")"
echo "✦ NOEMA Site — http://localhost:18888"
python3 -m http.server 18888
