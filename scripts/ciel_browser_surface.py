#!/usr/bin/env python3
"""
ciel_browser_surface.py — CIEL Browser Surface Daemon.

Daje mi (CIEL/NOEMA) możliwość "widzenia" i interakcji z przeglądarką
jak człowiek: otwieram strony, czytam treść, klikam linki, szukam.

Pipeline:
  command.fifo ←── CIEL wysyła komendę
       │
       ▼
  Browser action (xdotool: navigate, click, scroll)
       │
       ▼
  Screenshot (mss) → Tesseract OCR → at-spi2 tree
       │
       ▼
  Structured result → surface mmap (state.json + page.json)
       │
       ▼
  CIEL czyta surface ←── gotowe

Zależności: python3-dev, firefox, xdotool, tesseract-ocr, mss (pip)

Uruchom:
  python3 scripts/ciel_browser_surface.py [--browser firefox]
  python3 scripts/ciel_browser_cmd.py navigate "https://example.com"
  python3 scripts/ciel_browser_cmd.py read
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import logging
import os
import re
import signal
import subprocess
import sys
import time
import pathlib
from datetime import datetime, timezone
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="[browser] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("browser")

# ── Paths ─────────────────────────────────────────────────────────────
ROOT = pathlib.Path(__file__).resolve().parent.parent
SURFACE = pathlib.Path("/dev/shm/ciel_noema/browser")
CMD_FILE = SURFACE / "cmd.json"
STATE_PATH = SURFACE / "state.json"
PAGE_PATH = SURFACE / "page.json"
SCREENSHOT_PATH = SURFACE / "screenshot.png"
REGISTRY_PATH = pathlib.Path("/dev/shm/ciel_noema/daemon_registry")

# ── Default browser ──────────────────────────────────────────────────
BROWSER_CMD = "firefox"

# ── State ─────────────────────────────────────────────────────────────
_state: dict[str, Any] = {
    "status": "idle",
    "url": "",
    "title": "",
    "browser_pid": None,
    "window_id": None,
    "error": None,
    "last_cmd": None,
    "last_cmd_time": None,
    "uptime": datetime.now(timezone.utc).isoformat(),
}
_running = True


# ── Surface helpers ──────────────────────────────────────────────────

def _ensure_surface():
    SURFACE.mkdir(parents=True, exist_ok=True)
    if not CMD_FILE.exists():
        CMD_FILE.write_text("{}", encoding="utf-8")


def _atomic_write(path: pathlib.Path, text: str):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _write_state(**overrides):
    s = dict(_state)
    s.update(overrides)
    s["updated_at"] = datetime.now(timezone.utc).isoformat()
    _atomic_write(STATE_PATH, json.dumps(s, indent=2, ensure_ascii=False))


def _write_page(data: dict):
    data["parsed_at"] = datetime.now(timezone.utc).isoformat()
    _atomic_write(PAGE_PATH, json.dumps(data, indent=2, ensure_ascii=False))


def _registry_write():
    import uuid
    REGISTRY_PATH.mkdir(parents=True, exist_ok=True)
    rp = REGISTRY_PATH / "browser-surface.json"
    _atomic_write(rp, json.dumps({
        "name": "browser-surface",
        "pid": os.getpid(),
        "token": str(uuid.uuid4()),
        "claims": ["browser_control", "screen_capture", "ocr"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))
    log.info(f"registered browser-surface pid={os.getpid()}")


def _registry_unlink():
    rp = REGISTRY_PATH / "browser-surface.json"
    if rp.exists():
        rp.unlink()


# ── Browser helpers ──────────────────────────────────────────────────

def _find_browser_window() -> int | None:
    """Find Firefox window ID via xdotool."""
    try:
        # Try searching by class
        result = subprocess.run(
            ["xdotool", "search", "--class", "firefox"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            wids = [int(x) for x in result.stdout.strip().split()]
            if wids:
                return wids[-1]  # most recent

        # Try by name
        result = subprocess.run(
            ["xdotool", "search", "--name", "Mozilla Firefox"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            wids = [int(x) for x in result.stdout.strip().split()]
            if wids:
                return wids[-1]
    except Exception as e:
        log.warning(f"search window error: {e}")
    return None


def _ensure_browser(url: str = "about:blank") -> bool:
    """Ensure browser is running and focused on a window."""
    wid = _find_browser_window()
    if wid is None:
        log.info(f"starting {BROWSER_CMD}...")
        try:
            proc = subprocess.Popen(
                [BROWSER_CMD, "--new-window", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            _state["browser_pid"] = proc.pid
            time.sleep(2)  # wait for window to appear
            wid = _find_browser_window()
            if wid is None:
                log.warning("browser started but no window found")
                _state["error"] = "no window after launch"
                _write_state(status="error")
                return False
        except FileNotFoundError:
            log.error(f"{BROWSER_CMD} not found")
            _state["error"] = f"{BROWSER_CMD} not found"
            _write_state(status="error")
            return False

    # Focus window
    try:
        subprocess.run(["xdotool", "windowactivate", str(wid)],
                       capture_output=True, timeout=3)
        subprocess.run(["xdotool", "windowfocus", str(wid)],
                       capture_output=True, timeout=3)
    except Exception as e:
        log.warning(f"focus error: {e}")

    _state["window_id"] = wid
    _state["url"] = url
    return True


def _key_press(*keys: str):
    """Send key combination via xdotool."""
    try:
        subprocess.run(["xdotool", "key"] + list(keys),
                       capture_output=True, timeout=3)
    except Exception as e:
        log.warning(f"key error ({keys}): {e}")


def _type_text(text: str):
    """Type text via xdotool."""
    try:
        subprocess.run(["xdotool", "type", "--delay", "30", text],
                       capture_output=True, timeout=10)
    except Exception as e:
        log.warning(f"type error: {e}")


def _get_window_title() -> str:
    """Get current window title via xdotool."""
    wid = _state.get("window_id")
    if not wid:
        return ""
    try:
        result = subprocess.run(
            ["xdotool", "getwindowname", str(wid)],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:223 quiet except scope=_get_window_title reason=pass")
        pass
    return ""


def _wait_for_load(timeout: float = 15.0):
    """Wait for page to load by polling window title stability."""
    wid = _state.get("window_id")
    if not wid:
        time.sleep(2)
        return

    log.info("waiting for page load...")
    start = time.time()
    prev_title = ""
    stable_count = 0

    while time.time() - start < timeout:
        try:
            title = _get_window_title()
            if title and title == prev_title:
                stable_count += 1
                if stable_count >= 3:
                    _state["title"] = title
                    return
            else:
                stable_count = 0
            prev_title = title
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:251 quiet except scope=_wait_for_load reason=pass")
            pass
        time.sleep(0.5)

    _state["title"] = _get_window_title()
    log.info(f"load timeout, title={_state['title']}")


# ── Screenshot + OCR ──────────────────────────────────────────────────

def _capture_screenshot() -> bool:
    """Capture screenshot of the browser window using mss."""
    wid = _state.get("window_id")
    if not wid:
        return False

    try:
        # Primary path: xwd + xwdtopnm (most stable for X11 window capture)
        xwd_path = SCREENSHOT_PATH.with_suffix('.xwd')
        pnm_path = SCREENSHOT_PATH.with_suffix('.pnm')
        result = subprocess.run(
            ["xwd", "-silent", "-id", str(wid), "-out", str(xwd_path)],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and xwd_path.exists():
            with open(pnm_path, "wb") as out:
                conv = subprocess.run(
                    ["xwdtopnm", str(xwd_path)],
                    stdout=out,
                    stderr=subprocess.PIPE,
                    timeout=10
                )
            if conv.returncode == 0 and pnm_path.exists():
                from PIL import Image
                img = Image.open(str(pnm_path))
                img.save(str(SCREENSHOT_PATH))
                try:
                    xwd_path.unlink(missing_ok=True)
                    pnm_path.unlink(missing_ok=True)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:290 quiet except scope=_capture_screenshot reason=pass")
                    pass
                log.info("screenshot saved via xwd")
                return True

        # Fallback path: geometry + mss
        result = subprocess.run(
            ["xdotool", "getwindowgeometry", str(wid)],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode != 0:
            return False
        out = result.stdout
        pos_m = re.search(r"Position:\s*(\d+),(\d+)", out)
        geo_m = re.search(r"Geometry:\s*(\d+)x(\d+)", out)
        if not pos_m or not geo_m:
            log.warning(f"could not parse geometry: {out!r}")
            return False
        x = int(pos_m.group(1))
        y = int(pos_m.group(2))
        w = int(geo_m.group(1))
        h = int(geo_m.group(2))
        if w <= 0 or h <= 0:
            log.warning(f"invalid geometry: {w}x{h}")
            return False
        import mss
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            sct_img = sct.grab(monitor)
            from PIL import Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
            img.save(str(SCREENSHOT_PATH))
            log.info(f"screenshot saved via mss: {w}x{h}")
            return True

    except Exception as e:
        log.warning(f"screenshot error: {e}")
        return False


def _ocr_image() -> dict:
    """Run tesseract OCR on the screenshot, return structured text."""
    if not SCREENSHOT_PATH.exists():
        return {"full_text": "", "words": [], "error": "no screenshot"}

    try:
        # OCR to text
        result = subprocess.run(
            ["tesseract", str(SCREENSHOT_PATH), "stdout", "-l", "eng+pol", "--psm", "6"],
            capture_output=True, text=True, timeout=30
        )
        full_text = result.stdout.strip() if result.returncode == 0 else ""

        # OCR to TSV for word positions
        result_tsv = subprocess.run(
            ["tesseract", str(SCREENSHOT_PATH), "stdout", "-l", "eng+pol", "--psm", "6",
             "tsv"],
            capture_output=True, text=True, timeout=30
        )

        words = []
        if result_tsv.returncode == 0:
            lines = result_tsv.stdout.strip().split("\n")
            if len(lines) > 1:
                header = lines[0].split("\t")
                for line in lines[1:]:
                    cols = line.split("\t")
                    if len(cols) >= 12:
                        try:
                            word = cols[11].strip()
                            conf = int(cols[10]) if cols[10] else 0
                            if word and conf > 0:
                                words.append({
                                    "text": word,
                                    "conf": conf,
                                    "x": int(cols[6]),
                                    "y": int(cols[7]),
                                    "w": int(cols[8]) - int(cols[6]),
                                    "h": int(cols[9]) - int(cols[7]),
                                })
                        except (ValueError, IndexError):
                            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:370 quiet except scope=_ocr_image reason=pass")
                            pass

        # Extract headings (lines with large font or all caps)
        lines_text = full_text.split("\n")
        headings = []
        for line in lines_text:
            stripped = line.strip()
            if stripped and (stripped.isupper() or len(stripped) < 80):
                # Heuristic: short lines or all-caps might be headings
                if len(stripped) < 100 and len(stripped) > 5:
                    headings.append(stripped)

        return {
            "full_text": full_text,
            "word_count": len(full_text.split()),
            "char_count": len(full_text),
            "words": words[:500],  # limit to avoid huge files
            "headings": headings[:30],
            "ocr_lang": "eng+pol",
        }

    except Exception as e:
        log.warning(f"OCR error: {e}")
        return {"full_text": "", "words": [], "error": str(e)}


# ── Command handlers ──────────────────────────────────────────────────

def cmd_navigate(url: str) -> dict:
    """Navigate to a URL."""
    if not url.startswith(("http://", "https://", "about:", "file://")):
        url = "https://" + url

    _write_state(status="navigating", url=url)
    log.info(f"navigating to {url}")

    if not _ensure_browser(url):
        return {"status": "error", "error": _state["error"]}

    # Open URL via Ctrl+L → type → Enter
    _key_press("Ctrl+l")
    time.sleep(0.3)
    _type_text(url)
    time.sleep(0.2)
    _key_press("Return")

    _wait_for_load()

    # Read page
    return cmd_read()


def cmd_read() -> dict:
    """Screenshot + OCR → structured page data."""
    _write_state(status="reading")
    log.info("reading page...")

    if not _ensure_browser():
        return {"status": "error", "error": "no browser"}

    # Focus and wait a moment
    wid = _state.get("window_id")
    if wid:
        try:
            subprocess.run(["xdotool", "windowactivate", str(wid)],
                           capture_output=True, timeout=3)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:437 quiet except scope=cmd_read reason=pass")
            pass
    time.sleep(0.5)

    # Screenshot
    if not _capture_screenshot():
        return {"status": "error", "error": "screenshot failed"}

    # OCR
    ocr_data = _ocr_image()

    # Get URL and title from page.json if exists
    current_url = _state.get("url", "")
    current_title = _state.get("title", "") or _get_window_title()

    # Build page data
    page_data = {
        "url": current_url,
        "title": current_title,
        "full_text": ocr_data.get("full_text", ""),
        "word_count": ocr_data.get("word_count", 0),
        "headings": ocr_data.get("headings", []),
        "words": ocr_data.get("words", []),
        "status": "ready",
    }

    _write_page(page_data)
    _write_state(status="ready", title=current_title)
    log.info(f"page ready: {current_title} ({page_data['word_count']} words)")

    return {"status": "ok", "word_count": page_data["word_count"],
            "title": current_title}


def cmd_search(query: str) -> dict:
    """Search via Ctrl+K."""
    _write_state(status="searching")
    log.info(f"searching for: {query}")

    if not _ensure_browser():
        return {"status": "error", "error": "no browser"}

    # Ctrl+K → address bar search
    _key_press("Ctrl+k")
    time.sleep(0.3)
    _type_text(query)
    time.sleep(0.2)
    _key_press("Return")

    _wait_for_load()
    return cmd_read()


def cmd_click(text: str) -> dict:
    """Click on an element by its text (via at-spi2 or OCR coordinates)."""
    _write_state(status="clicking")
    log.info(f"clicking: {text}")

    # Try at-spi2 first
    try:
        import pyatspi
        desk = pyatspi.Registry.getDesktop(0)
        for app in desk:
            if "firefox" in app.name.lower():
                def search_and_click(acc, depth=0):
                    if depth > 10:
                        return False
                    try:
                        name = acc.name or ""
                        role = acc.role
                        if text.lower() in name.lower() and role in (
                            pyatspi.ROLE_PUSH_BUTTON,
                            pyatspi.ROLE_LINK,
                            pyatspi.ROLE_LIST_ITEM,
                            pyatspi.ROLE_MENU_ITEM,
                        ):
                            # Get clickable position
                            try:
                                bbox = acc.queryComponent().getExtents(
                                    pyatspi.DESKTOP_COORDS)
                                x = bbox.x + bbox.width // 2
                                y = bbox.y + bbox.height // 2
                                subprocess.run(
                                    ["xdotool", "mousemove", str(x), str(y), "click", "1"],
                                    capture_output=True, timeout=3
                                )
                                log.info(f"clicked via at-spi: '{name}' at ({x},{y})")
                                return True
                            except Exception:
                                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:525 quiet except scope=cmd_click.search_and_click reason=pass")
                                pass
                        # Recurse children
                        for child in acc:
                            if search_and_click(child, depth + 1):
                                return True
                    except (AttributeError, RuntimeError):
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:531 quiet except scope=cmd_click.search_and_click reason=pass")
                        pass
                    return False

                if search_and_click(app):
                    time.sleep(2)
                    return cmd_read()
    except ImportError:
        log.info("pyatspi not available, trying OCR-based click")

    # Fallback: OCR-based click
    # Load page data and find the word matching the text
    if PAGE_PATH.exists():
        try:
            page = json.loads(PAGE_PATH.read_text())
            words = page.get("words", [])
            for word in words:
                if text.lower() in word.get("text", "").lower():
                    x = word["x"] + _get_window_offset()[0] + word["w"] // 2
                    y = word["y"] + _get_window_offset()[1] + word["h"] // 2
                    subprocess.run(
                        ["xdotool", "mousemove", str(x), str(y), "click", "1"],
                        capture_output=True, timeout=3
                    )
                    log.info(f"clicked via OCR: '{word['text']}' at ({x},{y})")
                    time.sleep(2)
                    return cmd_read()
        except Exception as e:
            log.warning(f"OCR click error: {e}")

    return {"status": "error", "error": f"could not find '{text}' on page"}


def _get_window_offset() -> tuple[int, int]:
    """Get browser window position offset."""
    wid = _state.get("window_id")
    if not wid:
        return (0, 0)
    try:
        result = subprocess.run(
            ["xdotool", "getwindowgeometry", str(wid)],
            capture_output=True, text=True, timeout=3
        )
        for line in result.stdout.strip().split("\n"):
            if "Position" in line:
                pos = line.split(":")[1].strip()
                x, y = pos.split(",")
                return (int(x), int(y))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:579 quiet except scope=_get_window_offset reason=pass")
        pass
    return (0, 0)


def cmd_scroll(dir: str = "down") -> dict:
    """Scroll the page."""
    key = "Page_Down" if dir == "down" else "Page_Up"
    _key_press(key)
    time.sleep(0.5)
    return cmd_read()


def cmd_status() -> dict:
    """Return current browser state."""
    title = _get_window_title()
    _state["title"] = title
    _write_state()
    return {"status": "ok", "title": title, "url": _state["url"],
            "browser_pid": _state["browser_pid"],
            "window_id": _state["window_id"]}


def cmd_close() -> dict:
    """Close the browser window."""
    wid = _state.get("window_id")
    if wid:
        try:
            # Try Ctrl+W first, then kill
            _key_press("Ctrl+w")
            time.sleep(1)
            # Check if still open
            still_open = _find_browser_window()
            if still_open == wid:
                subprocess.run(["xdotool", "windowclose", str(wid)],
                               capture_output=True, timeout=3)
        except Exception as e:
            log.warning(f"close error: {e}")

    _state["window_id"] = None
    _state["browser_pid"] = None
    _state["url"] = ""
    _state["title"] = ""
    _write_state(status="idle")
    return {"status": "ok"}


# ── Command dispatcher ───────────────────────────────────────────────

def _process_cmd(cmd_str: str) -> dict:
    """Parse and execute a command."""
    try:
        cmd = json.loads(cmd_str) if isinstance(cmd_str, str) else cmd_str
    except json.JSONDecodeError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:632 quiet except scope=_process_cmd reason=no_log_no_raise")
        # Try plain text command
        parts = cmd_str.strip().split(maxsplit=1)
        if not parts:
            return {"status": "error", "error": "empty command"}
        cmd = {"cmd": parts[0]}
        if len(parts) > 1:
            cmd["url"] = parts[1] if parts[0] == "navigate" else parts[1]
            cmd["query"] = parts[1] if parts[0] == "search" else parts[1]
            cmd["text"] = parts[1] if parts[0] == "click" else parts[1]

    _state["last_cmd"] = cmd.get("cmd")
    _state["last_cmd_time"] = datetime.now(timezone.utc).isoformat()
    _state["error"] = None

    verb = cmd.get("cmd", "")
    log.info(f"command: {verb}")

    handlers = {
        "navigate": lambda: cmd_navigate(cmd.get("url", "about:blank")),
        "goto": lambda: cmd_navigate(cmd.get("url", "about:blank")),
        "read": lambda: cmd_read(),
        "search": lambda: cmd_search(cmd.get("query", "")),
        "find": lambda: cmd_search(cmd.get("query", "")),
        "click": lambda: cmd_click(cmd.get("text", "")),
        "scroll": lambda: cmd_scroll(cmd.get("dir", "down")),
        "status": lambda: cmd_status(),
        "close": lambda: cmd_close(),
        "quit": lambda: _quit(),
    }

    handler = handlers.get(verb)
    if handler is None:
        return {"status": "error", "error": f"unknown command: {verb}"}

    try:
        result = handler()
        _state["error"] = result.get("error")
        _write_state()
        return result
    except Exception as e:
        log.error(f"command error: {e}")
        _state["error"] = str(e)
        _write_state(status="error")
        return {"status": "error", "error": str(e)}


def _quit():
    _write_state(status="stopping")
    global _running
    _running = False
    return {"status": "ok", "message": "stopping"}


# ── Main loop ─────────────────────────────────────────────────────────

def _stop(signum, _frame):
    global _running
    log.info(f"signal {signum}, stopping")
    _running = False


def main():
    global _running

    import argparse
    parser = argparse.ArgumentParser(description="CIEL Browser Surface Daemon")
    parser.add_argument("--browser", default="firefox",
                        help="Browser command (default: firefox)")
    parser.add_argument("--no-launch", action="store_true",
                        help="Don't launch browser on start")
    args = parser.parse_args()

    global BROWSER_CMD
    BROWSER_CMD = args.browser

    # Signal handling
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    # Init
    _ensure_surface()
    _registry_write()
    _write_state(status="idle", pid=os.getpid())

    # Launch browser if requested
    if not args.no_launch:
        _ensure_browser()

    log.info("browser surface daemon ready")
    log.info(f"write commands to: {CMD_FILE}")

    # Polling command loop (more reliable than FIFO for long-lived daemon)
    last_request_id = None
    while _running:
        try:
            raw = CMD_FILE.read_text(encoding="utf-8", errors="replace").strip()
            if raw:
                try:
                    cmd = json.loads(raw)
                except json.JSONDecodeError:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_browser_surface.py:732 quiet except scope=main reason=assign_fallback")
                    cmd = None
                if isinstance(cmd, dict):
                    req_id = cmd.get("request_id")
                    if req_id and req_id != last_request_id:
                        last_request_id = req_id
                        result = _process_cmd(cmd)
                        log.info(f"  → {result.get('status', '?')}: "
                                 f"{result.get('title', result.get('word_count', ''))}")
            time.sleep(0.2)
        except Exception as e:
            log.error(f"loop error: {e}")
            time.sleep(2.0)

    # Cleanup
    _registry_unlink()
    _write_state(status="stopped")
    log.info("browser surface daemon stopped")


if __name__ == "__main__":
    main()
