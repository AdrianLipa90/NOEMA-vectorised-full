import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import urllib.request
from pathlib import Path
from typing import Any

AGENT_URL = "http://localhost:18520/v1/chat/completions"

# CIEL ORBITAL BINDING — hardcoded check przy imporcie
_CIEL_BINDING_PATH = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
_CIEL_BINDING_OK = _CIEL_BINDING_PATH.exists() and _CIEL_BINDING_PATH.read_text().strip() == "ACTIVE"
if not _CIEL_BINDING_OK:
    import warnings
    warnings.warn("CIEL ORBITAL BINDING — agent_client loaded but binding not ACTIVE")


def analyze(text: str, timeout: int = 5) -> dict[str, Any]:
    payload = json.dumps({
        "messages": [
            {"role": "user", "content": f"File fragment input.txt:\n{text}"}
        ]
    }).encode()
    req = urllib.request.Request(AGENT_URL, data=payload,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        body = json.loads(resp.read())
        content = body["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/cielingo_core/bridge/agent_client.py:30 quiet except scope=analyze reason=return {\"error\": str(e), \"themes\": [], \"affect\": \"calm\", \"anchor_terms\": [], \"essence\": text[:150], \"hunch\": \"\"}")
        return {"error": str(e), "themes": [], "affect": "calm",
                "anchor_terms": [], "essence": text[:150], "hunch": ""}


def health() -> bool:
    try:
        resp = urllib.request.urlopen("http://localhost:18520/health", timeout=2)
        return resp.status == 200
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/cielingo_core/bridge/agent_client.py:39 quiet except scope=health reason=return False")
        return False
