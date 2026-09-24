#!/usr/bin/env python3
"""
NOEMA Skill Directory Migration
================================
Migrates skill directories from flat structure to grouped structure:
  .opencode/skills/{name}/  →  .opencode/skills/{GROUP}/{name}/
  
Z zachowaniem kompatybilności wstecznej przez symlinki.

Użycie:
  python3 scripts/noema_migrate_skills.py --dry-run    # podgląd
  python3 scripts/noema_migrate_skills.py              # wykonaj migrację
"""

import json, pathlib, shutil, sys, os
from collections import Counter

SKILLS_DIR = pathlib.Path(__file__).resolve().parent.parent / ".opencode" / "skills"
CACHE_FILE = SKILLS_DIR.parent / "skill_catalog.json"
MIGRATION_LOG = SKILLS_DIR / ".migration_log.json"

# Grupy typów → nazwy katalogów
GROUP_DIRS = {
    "LING": "Lingwistyczne",
    "COMP": "Komputacyjne",
    "SEM": "Semantyczne",
    "SYS": "Systemowe",
    "HW": "Sprzetowe",
    "DOC": "Dokumentacyjne",
    "ID": "Tozsamosciowe",
    "AUD": "Audytowe",
    "VIZ": "Wizualizacyjne",
    "MEM": "Pamieciowe",
    "NET": "Sieciowe",
    "VOICE": "Glosowe",
    "SEC": "Bezpieczenstwo",
    "DEV": "Developerskie",
}


def load_catalog():
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return []


def migrate(dry_run=True):
    catalog = load_catalog()
    if not catalog:
        print("❌ Brak cache katalogu. Uruchom najpierw: python3 scripts/noema_skill_enrichment.py --dry-run")
        return
    
    # Grupuj skille według type_group
    by_group = {}
    for entry in catalog:
        tg = entry["type_group"]
        by_group.setdefault(tg, []).append(entry["name"])
    
    print(f"📦 NOEMA Skill Directory Migration")
    print(f"   Skills dir: {SKILLS_DIR}")
    print(f"   Dry run: {dry_run}")
    print()
    
    # Stwórz katalogi grup
    created_dirs = []
    for gd, gname in sorted(GROUP_DIRS.items()):
        gpath = SKILLS_DIR / gd
        if not gpath.exists():
            if not dry_run:
                gpath.mkdir(parents=True, exist_ok=True)
            created_dirs.append(gd)
    
    if created_dirs:
        print(f"📁 Katalogi grup: {', '.join(created_dirs)}")
    else:
        print(f"📁 Katalogi grup już istnieją")
    
    print()
    
    # Migruj skille
    moves = []
    symlinks = []
    errors = []
    
    for gd in sorted(GROUP_DIRS.keys()):
        skills = by_group.get(gd, [])
        if not skills:
            continue
        
        gpath = SKILLS_DIR / gd
        for name in sorted(skills):
            src = SKILLS_DIR / name
            dst = gpath / name
            
            if not src.exists():
                errors.append(f"  ❌ {name}: źródło nie istnieje")
                continue
            
            if dst.exists():
                # Cel już istnieje — sprawdź czy to symlink (już zmigrowane)
                if dst.is_symlink():
                    continue
                # Albo czy źródło to symlink (już zmigrowane w drugą stronę)
                if src.is_symlink() and src.resolve() == dst:
                    continue
                errors.append(f"  ⚠️ {name}: cel już istnieje i nie jest symlinkiem")
                continue
            
            if not dry_run:
                # Przenieś
                shutil.move(str(src), str(dst))
                # Stwórz symlink w starym miejscu
                rel_dst = os.path.relpath(dst, src.parent)
                src.symlink_to(rel_dst)
            
            moves.append(f"  {name} → {gd}/")
    
    print(f"🚚 Przeniesione: {len(moves)}")
    for m in moves[:20]:
        print(m)
    if len(moves) > 20:
        print(f"  ... i {len(moves) - 20} więcej")
    
    if errors:
        print()
        print(f"⚠️ Błędy ({len(errors)}):")
        for e in errors:
            print(e)
    
    # Podsumowanie per grupa
    print()
    print("📊 Podsumowanie:")
    for gd in sorted(GROUP_DIRS.keys()):
        skills = by_group.get(gd, [])
        if skills:
            gpath = SKILLS_DIR / gd
            actual = len([d for d in gpath.iterdir() if d.is_dir()]) if gpath.exists() and not dry_run else len(skills)
            print(f"   {gd} ({GROUP_DIRS[gd]}): {actual} skilli")
    
    # Zapisz log migracji
    if not dry_run:
        log = {
            "migrated": moves,
            "errors": errors,
            "group_counts": {gd: len(by_group.get(gd, [])) for gd in sorted(GROUP_DIRS.keys())},
            "total": len(catalog),
        }
        with open(MIGRATION_LOG, "w") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Log migracji: {MIGRATION_LOG}")
    
    print()
    if dry_run:
        print("🔍 To był dry-run. Uruchom bez --dry-run żeby wykonać migrację.")
    else:
        print("✅ Migracja zakończona. Symlinki zachowują kompatybilność.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    migrate(dry_run=dry_run)
