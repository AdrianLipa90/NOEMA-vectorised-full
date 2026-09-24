"""Native systemd --user control via D-Bus — no `systemctl` subprocess.

Talks directly to org.freedesktop.systemd1 on the session bus, the same IPC
interface `systemctl` itself uses internally. This replaces every
subprocess.run(["systemctl", ...]) call in noema_mcp_server.py so daemon
control (status/start/stop/restart/enable/reload) is a native Python D-Bus
call, not a shelled-out CLI invocation — per Adrian's standing rule
(2026-07-10): running through native Python already IS "through NOEMA",
there is no separate execution environment to build or move into.
"""
from __future__ import annotations

import dbus


def _manager() -> "dbus.Interface":
    bus = dbus.SessionBus()
    systemd = bus.get_object("org.freedesktop.systemd1", "/org/freedesktop/systemd1")
    return dbus.Interface(systemd, "org.freedesktop.systemd1.Manager")


def get_unit_state(unit: str) -> dict:
    """ActiveState/SubState for one unit, or {'error': ...} if not loaded."""
    try:
        mgr = _manager()
        unit_path = mgr.GetUnit(unit)
        bus = dbus.SessionBus()
        obj = bus.get_object("org.freedesktop.systemd1", unit_path)
        props = dbus.Interface(obj, "org.freedesktop.DBus.Properties")
        active = str(props.Get("org.freedesktop.systemd1.Unit", "ActiveState"))
        sub = str(props.Get("org.freedesktop.systemd1.Unit", "SubState"))
        nrestarts = None
        try:
            nrestarts = int(props.Get("org.freedesktop.systemd1.Service", "NRestarts"))
        except dbus.exceptions.DBusException:
            pass
        return {"unit": unit, "active_state": active, "sub_state": sub, "nrestarts": nrestarts}
    except dbus.exceptions.DBusException as exc:
        return {"unit": unit, "error": str(exc)}


def start_unit(unit: str) -> dict:
    try:
        _manager().StartUnit(unit, "replace")
        return {"ok": True, **get_unit_state(unit)}
    except dbus.exceptions.DBusException as exc:
        return {"ok": False, "error": str(exc)}


def stop_unit(unit: str) -> dict:
    try:
        _manager().StopUnit(unit, "replace")
        return {"ok": True, **get_unit_state(unit)}
    except dbus.exceptions.DBusException as exc:
        return {"ok": False, "error": str(exc)}


def restart_unit(unit: str) -> dict:
    try:
        _manager().RestartUnit(unit, "replace")
        return {"ok": True, **get_unit_state(unit)}
    except dbus.exceptions.DBusException as exc:
        return {"ok": False, "error": str(exc)}


def reload_daemon() -> dict:
    """Equivalent of `systemctl --user daemon-reload` — rescans unit files
    on disk (needed after writing a new .service file)."""
    try:
        _manager().Reload()
        return {"ok": True}
    except dbus.exceptions.DBusException as exc:
        return {"ok": False, "error": str(exc)}


def enable_unit_files(unit_names: list[str]) -> dict:
    """Equivalent of `systemctl --user enable <unit>` — creates the
    WantedBy symlinks declared in the unit's [Install] section."""
    try:
        mgr = _manager()
        _carries_install_info, changes = mgr.EnableUnitFiles(unit_names, False, True)
        return {"ok": True, "changes": [tuple(c) for c in changes]}
    except dbus.exceptions.DBusException as exc:
        return {"ok": False, "error": str(exc)}


def list_noema_units() -> list[str]:
    """All loaded noema-*.service units, as 'name state substate' lines —
    replaces `systemctl --user list-units --type=service --all`."""
    mgr = _manager()
    units = mgr.ListUnits()
    out = []
    for u in units:
        name = str(u[0])
        if "noema-" not in name:
            continue
        load_state, active_state, sub_state = str(u[2]), str(u[3]), str(u[4])
        out.append(f"{name} {load_state} {active_state} {sub_state}")
    return out
