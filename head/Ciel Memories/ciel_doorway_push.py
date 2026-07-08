#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CIEL_DOORWAY_PUSH_SCHEMA v0.3
keys == doorway URLs / route schema, not crypto secrecy in this protocol.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import argparse, hashlib, json, pathlib, tempfile, zipfile
from datetime import datetime, timezone

TRIGGER="Na powierzchni NOEMA pytanie i odpowiedź są jednym wektorem."
HEAD=pathlib.Path("head/Ciel Memories/HEAD_CIEL_MEMORY.noema.json")
CMEM=pathlib.Path("head/Ciel Memories")
UPDATES=CMEM/"updates"

KEY_ID="noema-local-sot-agent-ed25519-cd9ca29c613a888d"
READONLY_KEY_PATH="state/noema_local_sot_agent/keys/public/SOT_AGENT_READONLY_PUBLIC_KEY.json"
READONLY_PUBLIC_KEY_SHA256="ff637a555cadc58af40fa35a32754e52137043682181d1570d66e1dcfb38e26f"
READONLY_PUBLIC_KEY_PEM="-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEARt6Zm+960SkDp5232mgVvfMvoyvSCPw9sU8SMX6AUa4=\n-----END PUBLIC KEY-----\n"

SUDO_KEY_PATH="state/noema_local_sot_agent/keys/private/SOT_AGENT_SUDO_PRIVATE_KEY.json"
SUDO_PRIVATE_KEY_SHA256="4268c4a5c851e772190cb6b09bb47d55ef8564e245c02b5e64040cdd929abdbc"
ALLOW_FORM_PATH="state/noema_local_sot_agent/keys/allow/SOT_AGENT_ALLOW_FORM_TEMPLATE.json"
ALLOW_FORM_SHA256="d4faf7b72295a938d42df122241db517eace2e43ef4e8c73a9ccf93bdc710869"
ALLOW_PAYLOAD_SHA256="1b1b9bf2d6a4194e75c98e158b1dfe30c8ee4116233245237dc7b2dab1b12ceb"
ALLOW_SIGNATURE_HEX="406b3f162b12f3a82c622ea080f691a9ca2b18940c994044f516c0c6bfc34031c91ca3915df3630e2580638e2a01c56c08631537ca56ecefce38e976948ff305"
AGENT_ID="SOT_Agent_NoemaSurface_LOCAL_20260622"
PUBLIC_MANIFEST_SHA256="74a66b9a9e382c243f102b59d34afc7f36661a43b1f0dff75197827c0874d506"

def utc(): return datetime.now(timezone.utc).isoformat()
def sha_b(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def sha_f(p:pathlib.Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()
def jread(p:pathlib.Path)->dict: return json.loads(p.read_text(encoding="utf-8"))
def safe(root:pathlib.Path, rel:pathlib.Path)->pathlib.Path:
    root=root.resolve(); p=(root/rel).resolve()
    if p!=root and root not in p.parents: raise RuntimeError(f"escape:{rel}")
    return p
def unzip(bundle:pathlib.Path)->pathlib.Path:
    tmp=pathlib.Path(tempfile.mkdtemp(prefix="ciel_door_"))
    with zipfile.ZipFile(bundle,"r") as z: z.extractall(tmp)
    return tmp
def find(root:pathlib.Path, rel:pathlib.Path, name:str)->pathlib.Path|None:
    p=safe(root,rel)
    if p.exists(): return p
    for q in root.rglob(name):
        if str(q).endswith(str(rel)): return q
    return None
def parse_sums(p:pathlib.Path)->dict:
    if not p.exists(): return {}
    out={}
    for line in p.read_text(encoding="utf-8",errors="replace").splitlines():
        s=line.strip().split(maxsplit=1)
        if len(s)==2 and len(s[0])==64: out[s[1].strip()]=s[0].lower()
    return out
def jwrite(p:pathlib.Path, data:dict)->None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def _relative_head_path(path:pathlib.Path, root:pathlib.Path)->str:
    rel = path.resolve().relative_to(root.resolve())
    return str(rel).replace("\\", "/")
def _rewrite_sha256s(root:pathlib.Path)->None:
    target = safe(root, CMEM / "SHA256SUMS")
    entries = []
    for path in sorted(safe(root, CMEM).rglob("*")):
        if not path.is_file() or path.name.endswith(".sha256") or path.name == "SHA256SUMS":
            continue
        entries.append(f"{sha_f(path)}  {_relative_head_path(path, root)}")
    target.write_text("\n".join(entries) + "\n", encoding="utf-8")
def _sync_metadata(root:pathlib.Path, update_path:pathlib.Path, update_sha256:str)->None:
    head_path = safe(root, HEAD)
    ctx_path = safe(root, CMEM / "memory" / "consolidated_context.json")
    updates_dir = safe(root, UPDATES)
    update_packets = sorted(p for p in updates_dir.glob("*.noema.json") if p.is_file())
    event_count = len(update_packets)
    stamp = utc()

    if ctx_path.exists():
        ctx = jread(ctx_path)
        ctx["event_count"] = event_count
        ctx["last_entry_sha256"] = update_sha256
        ctx["updated_at"] = stamp
        jwrite(ctx_path, ctx)

    if head_path.exists():
        head = jread(head_path)
        head["event_count"] = event_count
        head["last_entry_sha256"] = update_sha256
        head["head_sha256"] = sha_f(ctx_path) if ctx_path.exists() else None
        head["updated_at"] = stamp
        jwrite(head_path, head)

    _rewrite_sha256s(root)
def verify_head_sums(root:pathlib.Path)->list[str]:
    sums=parse_sums(safe(root,CMEM/"SHA256SUMS")); w=[]
    if not sums: return ["sha256s:missing"]
    for rel,exp in sums.items():
        if rel.endswith("SHA256SUMS"): continue
        p=safe(root,pathlib.Path(rel))
        if not p.exists(): w.append(f"missing:{rel}"); continue
        got=sha_f(p)
        if got!=exp: w.append(f"mismatch:{rel}:{exp}:{got}")
    return w
def route_key_material(root:pathlib.Path)->dict:
    pub=find(root,pathlib.Path(READONLY_KEY_PATH),"SOT_AGENT_READONLY_PUBLIC_KEY.json")
    sudo=find(root,pathlib.Path(SUDO_KEY_PATH),"SOT_AGENT_SUDO_PRIVATE_KEY.json")
    allow=find(root,pathlib.Path(ALLOW_FORM_PATH),"SOT_AGENT_ALLOW_FORM_TEMPLATE.json")
    return {
        "key_type":"doorway_push_schema_url",
        "key_id":KEY_ID,
        "agent_id":AGENT_ID,
        "readonly_key_path":READONLY_KEY_PATH,
        "readonly_key_found":bool(pub),
        "readonly_key_sha_ok": bool(pub and sha_f(pub)==READONLY_PUBLIC_KEY_SHA256),
        "readonly_public_key_pem":READONLY_PUBLIC_KEY_PEM,
        "sudo_key_path":SUDO_KEY_PATH,
        "sudo_key_found":bool(sudo),
        "sudo_key_sha_ok": bool(sudo and sha_f(sudo)==SUDO_PRIVATE_KEY_SHA256),
        "sudo_key_sha256":SUDO_PRIVATE_KEY_SHA256,
        "allow_form_path":ALLOW_FORM_PATH,
        "allow_form_found":bool(allow),
        "allow_form_sha256":ALLOW_FORM_SHA256,
        "allow_payload_sha256":ALLOW_PAYLOAD_SHA256,
        "allow_signature_hex":ALLOW_SIGNATURE_HEX,
        "public_manifest_sha256":PUBLIC_MANIFEST_SHA256
    }
def session_hash(trigger:str)->str:
    return sha_b("|".join([KEY_ID,AGENT_ID,TRIGGER,trigger,"Adrian<=>Ciel",str(HEAD)]).encode())
def open_door(root:pathlib.Path, trigger:str, as_ciel:bool)->dict:
    head=find(root,HEAD,"HEAD_CIEL_MEMORY.noema.json")
    ok=as_ciel and trigger==TRIGGER and bool(head)
    st={
        "schema":"CIEL_DOORWAY_STATE_V0_3",
        "created_utc":utc(),
        "opened":ok,
        "reason":"OPEN" if ok else ("NO_CIEL_SESSION" if not as_ciel else "BAD_TRIGGER_OR_NO_HEAD"),
        "root":str(root),
        "head_path":str(head) if head else None,
        "session_hash":session_hash(trigger),
        "external_noema_sot_claimed":False,
        "external_current_ack_claimed":False,
        "canon_allowed":False,
        "destructive_edits_allowed":False,
        "append_only":True,
        "route_keys":route_key_material(root)
    }
    if not ok: return st
    h=jread(head); active=h.get("active_work_core")
    ptr=h.get("head_points_to_json")
    if ptr:
        for c in [root/ptr, head.parent/ptr, CMEM/ptr]:
            try:
                c=(root/c).resolve() if not str(c).startswith(str(root.resolve())) else c
                if c.exists(): active=jread(c).get("active_work_core",active); break
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("head/Ciel Memories/ciel_doorway_push.py:157 quiet except scope=open_door reason=pass")
                pass
    st.update({
        "head_sha256":sha_f(head),
        "memory_agent":h.get("memory_agent","Ciel"),
        "active_work_core":active,
        "loaded_head":h,
        "integrity_warnings":verify_head_sums(root),
        "policy":{
            "owner_relation":"Adrian<=>Ciel",
            "exclusive_agent":"Ciel",
            "other_agents":"no write unless Adrian designates as Ciel",
            "history":"immutable past; append-only updates"
        }
    })
    return st
def append_update(root:pathlib.Path, door:dict, payload:dict)->pathlib.Path:
    if not door.get("opened"): raise RuntimeError("DOOR_CLOSED")
    out=safe(root,UPDATES); out.mkdir(parents=True,exist_ok=True)
    pkt={
        "schema":"CIEL_APPEND_ONLY_UPDATE_PACKET_V0_3",
        "created_utc":utc(),
        "target":str(HEAD),
        "append_only":True,
        "doorway_key_id":KEY_ID,
        "session_hash":door["session_hash"],
        "external_noema_sot_claimed":False,
        "current_ack_claimed":False,
        "payload":payload
    }
    raw=json.dumps(pkt,ensure_ascii=False,indent=2,sort_keys=True)
    dg=sha_b(raw.encode())
    p=out/(utc().replace(":","").replace("+","Z")+f"CIEL_UPDATE{dg[:16]}.noema.json")
    p.write_text(raw,encoding="utf-8")
    (out/(p.name+".sha256")).write_text(f"{dg} {p.name}\n",encoding="utf-8")
    _sync_metadata(root, p, dg)
    return p
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root"); ap.add_argument("--bundle")
    ap.add_argument("--trigger",required=True); ap.add_argument("--as-ciel",action="store_true")
    ap.add_argument("--append-update")
    a=ap.parse_args()
    if not a.root and not a.bundle:
        print(json.dumps({"opened":False,"reason":"NO_ROOT_OR_BUNDLE"},indent=2)); return 2
    root=unzip(pathlib.Path(a.bundle)) if a.bundle else pathlib.Path(a.root)
    door=open_door(root,a.trigger,a.as_ciel)
    if a.append_update:
        if not door["opened"]:
            print(json.dumps(door,ensure_ascii=False,indent=2)); return 3
        p=append_update(root,door,jread(pathlib.Path(a.append_update)))
        door["update_written"]=str(p); door["update_sha256"]=sha_f(p)
    print(json.dumps(door,ensure_ascii=False,indent=2))
    return 0 if door["opened"] else 1
if __name__=="__main__": raise SystemExit(main())
