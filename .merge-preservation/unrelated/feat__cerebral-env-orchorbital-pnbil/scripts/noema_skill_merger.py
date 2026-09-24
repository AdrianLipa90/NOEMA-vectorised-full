#!/usr/bin/env python3
"""
noema_skill_merger.py — merge'owanie i tworzenie nowych skilli przez import.

Użycie:
  python3 scripts/noema_skill_merger.py --list                    # lista merge grup
  python3 scripts/noema_skill_merger.py --group lns-reports       # merge grupy
  python3 scripts/noema_skill_merger.py --custom "nazwa" --skills "skill1,skill2"  # custom merge
  python3 scripts/noema_skill_merger.py --from-code --code "..." --name "nowy-skill"  # z kodu

Wszystkie zmiany rejestrowane w skill_registry + Writing Logger.
"""

import argparse, json, sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / ".opencode" / "skills"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from ciel_geometry.taskplan_db import TaskPlanDB
from ciel_geometry.writing_logger import log_creation


def merge_skills(group_name: str, skill_names: list[str], title: str, desc: str):
    """Tworzy merged skill z listy nazw skilli."""
    db = TaskPlanDB()
    group_dir = SKILLS_DIR / group_name
    group_dir.mkdir(parents=True, exist_ok=True)

    # Pobierz dane z registry
    all_skills = db.list_skills(limit=300)
    skills_in = [s for s in all_skills if s["name"] in skill_names]

    if not skills_in:
        print(f"❌ Brak skilli do merge. Sprawdź nazwy.")
        return

    # Buduj zawartość
    lines = [f"# {title}", "", desc, "", "---", ""]
    lines.append("## Importy")
    lines.append("")
    lines.append("Ten skill agreguje poniższe skille źródłowe:")
    lines.append("")
    for s in skills_in:
        lines.append(f"- `{s['name']}` → [`{s['file_path']}`]({s['file_path']}) ({s['lines']} linii)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sekcje
    for i, s in enumerate(skills_in, 1):
        source = Path(s["file_path"])
        if source.exists():
            content = source.read_text()
            lines.append(f"## {i}. {s['name']}")
            lines.append("")
            lines.append(f"*Źródło: [`{s['file_path']}`]({s['file_path']})*")
            lines.append("")
            header_skipped = False
            for cl in content.split('\n'):
                if not header_skipped and cl.startswith('# '):
                    header_skipped = True
                    continue
                lines.append(cl)
            lines.append("")
            lines.append("---")
            lines.append("")

    merged = '\n'.join(lines)
    skill_file = group_dir / "SKILL.md"
    skill_file.write_text(merged)

    # Rejestruj w bazie
    db.add_skill(
        name=group_name, title=title,
        category="merged", file_path=str(skill_file),
        lines=len(merged.split('\n')), frequency=0.5,
        tags=["merge", *skill_names[:5]]
    )

    # Writing Logger
    log_creation(f'.opencode/skills/{group_name}/SKILL.md',
                 f'Merged skill: {len(skills_in)} skilli → {title} ({len(merged.split("\\n"))} linii)',
                 ['SKILL', 'MERGE', group_name.upper()], 'SKILL')

    print(f"✅ Utworzono '{group_name}' — {len(skills_in)} skilli, {len(merged.split(chr(10)))} linii")
    return {"name": group_name, "skills": len(skills_in), "lines": len(merged.split(chr(10)))}


def from_code(name: str, code: str):
    """Tworzy nowy skill z surowego kodu/tekstu."""
    db = TaskPlanDB()
    group_dir = SKILLS_DIR / name
    group_dir.mkdir(parents=True, exist_ok=True)
    skill_file = group_dir / "SKILL.md"
    skill_file.write_text(code)

    lines_count = len(code.split('\n'))
    title = code.strip().split('\n')[0].replace('# ', '').strip() if code.strip().startswith('# ') else name

    db.add_skill(
        name=name, title=title,
        category="custom", file_path=str(skill_file),
        lines=lines_count, frequency=0.3,
        tags=["custom", "from-code"]
    )

    log_creation(f'.opencode/skills/{name}/SKILL.md',
                 f'Nowy skill z kodu: {name} ({lines_count} linii)',
                 ['SKILL', 'CUSTOM', name.upper()], 'SKILL')

    print(f"✅ Utworzono '{name}' z kodu ({lines_count} linii)")
    return {"name": name, "lines": lines_count}


def from_import(name: str, file_paths: list[str], title: str = "", desc: str = ""):
    """Tworzy skill z importu istniejących plików kodu.
    
    Dla plików .py tworzy SKILL.md z przykładem importu + opisem.
    Dla innych plików kopiuje zawartość jako dokumentację.
    """
    db = TaskPlanDB()
    group_dir = SKILLS_DIR / name
    group_dir.mkdir(parents=True, exist_ok=True)
    
    total_lines = 0
    sections = []
    
    for fp in file_paths:
        path = Path(fp)
        if not path.exists():
            print(f"  ⚠️ Plik nie istnieje: {fp}")
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.count('\n') + 1
        total_lines += lines
        ext = path.suffix.lower()
        
        if ext == ".py":
            # Dla Pythona: skonstruuj import + opisz
            rel_path = path.relative_to(Path(__file__).resolve().parent.parent) if path.is_relative_to(Path(__file__).resolve().parent.parent) else path
            module_path = str(rel_path).replace('/', '.').replace('\\', '.').replace('.py', '')
            # Usuń prefiks 'src.' bo src/ jest w sys.path
            if module_path.startswith('src.'):
                module_path = module_path[4:]
            sections.append({
                "path": str(rel_path),
                "module": module_path,
                "lines": lines,
                "ext": ".py",
                "content": content,
            })
        else:
            # Inne pliki: wklej jako kod
            sections.append({
                "path": str(path),
                "module": "",
                "lines": lines,
                "ext": ext,
                "content": content,
            })
    
    if not sections:
        print("❌ Żaden plik nie istnieje")
        return
    
    # Buduj SKILL.md
    title = title or f"Import: {name}"
    desc = desc or f"Skill utworzony z {len(sections)} plików ({total_lines} linii)"
    
    lines_out = [f"# {title}", "", desc, "", "---", ""]
    lines_out.append("## Źródła")
    lines_out.append("")
    for s in sections:
        if s["ext"] == ".py" and s["module"]:
            lines_out.append(f"- **{s['path']}** → moduł `{s['module']}` ({s['lines']} linii)")
            lines_out.append(f"  ```python")
            lines_out.append(f"  # Import:")
            lines_out.append(f"  from {s['module']} import ...")
            lines_out.append(f"  ```")
        else:
            lines_out.append(f"- **{s['path']}** ({s['lines']} linii, {s['ext']})")
    lines_out.append("")
    lines_out.append("---")
    lines_out.append("")
    
    # Dodaj opisy funkcji/klas (dla .py)
    for s in sections:
        if s["ext"] != ".py":
            continue
        lines_out.append(f"## {s['path']}")
        lines_out.append("")
        lines_out.append(f"```python")
        lines_out.append(f"from {s['module']} import ...")
        lines_out.append(f"```")
        lines_out.append("")
        # Wyciągnij funkcje i klasy
        funcs = []
        classes = []
        for line in s["content"].split('\n'):
            stripped = line.strip()
            if stripped.startswith('def '):
                funcs.append(stripped.split('(')[0].replace('def ', ''))
            elif stripped.startswith('class '):
                classes.append(stripped.split('(')[0].replace('class ', '').replace(':', ''))
        if classes:
            lines_out.append("**Klasy:**")
            for c in classes:
                lines_out.append(f"- `{c}`")
        if funcs:
            lines_out.append("**Funkcje:**")
            for f in funcs:
                lines_out.append(f"- `{f}()`")
        lines_out.append("")
        lines_out.append("---")
        lines_out.append("")
    
    merged = '\n'.join(lines_out)
    skill_file = group_dir / "SKILL.md"
    skill_file.write_text(merged)
    
    # Rejestruj w bazie
    db.add_skill(
        name=name, title=title,
        category="imported", file_path=str(skill_file),
        lines=total_lines, frequency=0.3,
        tags=["import", *[s['ext'].replace('.','') for s in sections]]
    )
    
    log_creation(f'.opencode/skills/{name}/SKILL.md',
                 f'Imported skill: {len(sections)} plików → {title} ({total_lines} linii)',
                 ['SKILL', 'IMPORT', name.upper()], 'SKILL')
    
    print(f"✅ Utworzono '{name}' z {len(sections)} plików ({total_lines} linii)")
    print(f"   Skille źródłowe automatycznie zmapowane do decyzji najbliższych semanticznie")
    return {"name": name, "files": len(sections), "lines": total_lines}


def list_groups():
    """Wyświetla istniejące merge grupy."""
    db = TaskPlanDB()
    stats = db.get_skill_stats()
    print(f"=== Merge grupy ({len(stats['merge_groups'])}) ===")
    for mg in stats['merge_groups']:
        print(f"  {mg['group']}: {mg['count']} skilli")

    print(f"\n=== Wszystkie kategorie ===")
    for c in stats['categories']:
        print(f"  {c['name']}: {c['count']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NOEMA Skill Merger — merge'owanie i tworzenie skilli przez import")
    parser.add_argument("--list", action="store_true", help="Lista merge grup i kategorii")
    parser.add_argument("--group", type=str, help="Nazwa merge grupy (np. lns-reports)")
    parser.add_argument("--skills", type=str, help="Lista skilli do merge (oddzielone przecinkami)")
    parser.add_argument("--title", type=str, default="", help="Tytuł nowego skillu")
    parser.add_argument("--desc", type=str, default="", help="Opis nowego skillu")
    parser.add_argument("--from-code", action="store_true", help="Utwórz skill z kodu")
    parser.add_argument("--code", type=str, help="Kod/treść nowego skillu")
    parser.add_argument("--from-import", type=str, nargs="+", help="Importuj pliki źródłowe (.py, etc.) jako skill")
    parser.add_argument("--name", type=str, help="Nazwa nowego skillu (katalog)")

    args = parser.parse_args()

    if args.list:
        list_groups()
        sys.exit(0)

    if args.from_import:
        if not args.name:
            print("❌ --from-import wymaga --name")
            sys.exit(1)
        from_import(args.name, args.from_import, args.title or "", args.desc or "")
        sys.exit(0)

    if args.from_code:
        if not args.name or not args.code:
            print("❌ --from-code wymaga --name i --code")
            sys.exit(1)
        from_code(args.name, args.code)
        sys.exit(0)

    if args.group or args.skills:
        if args.group:
            # Użyj merge grupy z bazy
            db = TaskPlanDB()
            skills_in = db.list_skills(merge_group=args.group)
            skill_names = [s["name"] for s in skills_in]
            title = args.title or f"Merged: {args.group}"
            desc = args.desc or f"{len(skill_names)} skilli zmergowanych w jeden"
        else:
            skill_names = [s.strip() for s in args.skills.split(",") if s.strip()]
            title = args.title or f"Merged: {len(skill_names)} skilli"
            desc = args.desc or f"Custom merge {len(skill_names)} skilli"

        if not skill_names:
            print("❌ Brak skilli do merge")
            sys.exit(1)

        group_name = args.group or f"custom-{skill_names[0]}"
        merge_skills(group_name, skill_names, title, desc)
        sys.exit(0)

    parser.print_help()
