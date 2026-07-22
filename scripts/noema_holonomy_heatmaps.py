#!/usr/bin/env python3
"""
NOEMA Catalog Holonomy Heatmap Generator
=========================================
Generuje macierze holonomii (co-occurrence) między tagami w 3 katalogach:
  - SKILLS.md (umiejętności)
  - FUNCTIONS.md (funkcje/moduly)
  - PLANS.md (plany)

Wynik: JSON w site/assets/data/heatmaps/ — do wizualizacji w Portalu NOEMA.
"""

import json, re, os, sys
from collections import defaultdict, Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

NOEMA_ROOT = Path(__file__).resolve().parent.parent
SKILL_CACHE = NOEMA_ROOT / ".opencode" / "skill_catalog.json"
FUNCTIONS_FILE = NOEMA_ROOT / "FUNCTIONS.md"
PLANS_FILE = NOEMA_ROOT / "PLANS.md"
OUTPUT_DIR = NOEMA_ROOT / "site" / "assets" / "data" / "heatmaps"


# ============================================================
# 1. SKILLS — co-occurrence matrices from skill_catalog.json
# ============================================================

def load_skills():
    with open(SKILL_CACHE) as f:
        return json.load(f)


def build_skills_heatmaps(skills):
    heatmaps = {}

    # ── type_group × app_group ──
    type_app = defaultdict(lambda: defaultdict(int))
    type_app_rows = set()
    type_app_cols = set()
    for s in skills:
        tg = s["type_group"] or "NONE"
        ag = s["app_group"] or "NONE"
        type_app[tg][ag] += 1
        type_app_rows.add(tg)
        type_app_cols.add(ag)
    heatmaps["type_vs_app"] = {
        "title": "Grupa typów × Grupa zastosowań",
        "description": "Które typy skilli najczęściej mają które zastosowania",
        "x_label": "Grupa zastosowań (app_group)",
        "y_label": "Grupa typów (type_group)",
        "rows": sorted(type_app_rows),
        "cols": sorted(type_app_cols),
        "matrix": [[type_app[r][c] for c in sorted(type_app_cols)] for r in sorted(type_app_rows)]
    }

    # ── type_group × function_tags ──
    type_func = defaultdict(lambda: defaultdict(int))
    type_func_rows = set()
    type_func_cols = set()
    for s in skills:
        tg = s["type_group"] or "NONE"
        for ft in s["function_tags"]:
            type_func[tg][ft] += 1
            type_func_rows.add(tg)
            type_func_cols.add(ft)
    heatmaps["type_vs_function"] = {
        "title": "Grupa typów × Tagi funkcji",
        "description": "Które funkcje dominują w której grupie typów",
        "x_label": "Tagi funkcji",
        "y_label": "Grupa typów (type_group)",
        "rows": sorted(type_func_rows),
        "cols": sorted(type_func_cols),
        "matrix": [[type_func[r][c] for c in sorted(type_func_cols)] for r in sorted(type_func_rows)]
    }

    # ── type_group × primary_orbital ──
    type_orb = defaultdict(lambda: defaultdict(int))
    type_orb_rows = set()
    type_orb_cols = set()
    for s in skills:
        tg = s["type_group"] or "NONE"
        orb = s["primary_orbital"] or "NONE"
        type_orb[tg][orb] += 1
        type_orb_rows.add(tg)
        type_orb_cols.add(orb)
    heatmaps["type_vs_orbital"] = {
        "title": "Grupa typów × Orbital primary",
        "description": "Które orbitale dominują w której grupie typów",
        "x_label": "Orbital (M0-M8)",
        "y_label": "Grupa typów (type_group)",
        "rows": sorted(type_orb_rows),
        "cols": sorted(type_orb_cols),
        "matrix": [[type_orb[r][c] for c in sorted(type_orb_cols)] for r in sorted(type_orb_rows)]
    }

    # ── function_tags × primary_orbital ──
    func_orb = defaultdict(lambda: defaultdict(int))
    func_orb_rows = set()
    func_orb_cols = set()
    for s in skills:
        orb = s["primary_orbital"] or "NONE"
        for ft in s["function_tags"]:
            func_orb[ft][orb] += 1
            func_orb_rows.add(ft)
            func_orb_cols.add(orb)
    heatmaps["function_vs_orbital"] = {
        "title": "Tagi funkcji × Orbital primary",
        "description": "Które funkcje najczęściej mapują na który orbital",
        "x_label": "Orbital (M0-M8)",
        "y_label": "Tag funkcji",
        "rows": sorted(func_orb_rows),
        "cols": sorted(func_orb_cols),
        "matrix": [[func_orb[r][c] for c in sorted(func_orb_cols)] for r in sorted(func_orb_rows)]
    }

    # ── status × type_group ──
    status_type = defaultdict(lambda: defaultdict(int))
    status_type_rows = set()
    status_type_cols = set()
    for s in skills:
        st = s["status"] or "unknown"
        tg = s["type_group"] or "NONE"
        status_type[st][tg] += 1
        status_type_rows.add(st)
        status_type_cols.add(tg)
    heatmaps["status_vs_type"] = {
        "title": "Status × Grupa typów",
        "description": "Rozkład statusów (stable/draft/referenced/stub) per grupa typów",
        "x_label": "Grupa typów",
        "y_label": "Status",
        "rows": sorted(status_type_rows),
        "cols": sorted(status_type_cols),
        "matrix": [[status_type[r][c] for c in sorted(status_type_cols)] for r in sorted(status_type_rows)]
    }

    # ── Holonomia: co-occurrence tagów M0-M8 ──
    m_tags = ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]
    m_cooc = defaultdict(lambda: defaultdict(int))
    for s in skills:
        tags = [h for h in s["holonomy"] if h in m_tags]
        for i, a in enumerate(tags):
            for b in tags[i:]:
                if a != b:
                    m_cooc[a][b] += 1
                    m_cooc[b][a] += 1
    heatmaps["holonomy_m_cooc"] = {
        "title": "Ko-okurencja tagów holonomii M0-M8",
        "description": "Które orbitale najczęściej występują razem w tagach holonomii skilli",
        "x_label": "Orbital (M0-M8)",
        "y_label": "Orbital (M0-M8)",
        "rows": m_tags,
        "cols": m_tags,
        "matrix": [[m_cooc[r][c] for c in m_tags] for r in m_tags]
    }

    # ── type_group × semantic_mass (średnia) ──
    type_mass = defaultdict(list)
    for s in skills:
        tg = s["type_group"] or "NONE"
        sm = s.get("semantic_mass", 0)
        if sm:
            type_mass[tg].append(sm)
    type_mass_avg = {tg: round(sum(vals)/len(vals), 3) for tg, vals in type_mass.items()}
    heatmaps["type_vs_mass"] = {
        "title": "Średnia masa semantyczna per grupa typów",
        "description": "Gęstość informacji w skillach każdej grupy typów",
        "x_label": "Grupa typów",
        "y_label": "Średnia masa semantyczna",
        "rows": sorted(type_mass_avg.keys()),
        "cols": ["semantic_mass"],
        "matrix": [[type_mass_avg[r]] for r in sorted(type_mass_avg.keys())]
    }

    # ── function_tags co-occurrence ──
    func_cooc = defaultdict(lambda: defaultdict(int))
    all_funcs = set()
    for s in skills:
        fts = s["function_tags"]
        for f in fts:
            all_funcs.add(f)
        for i, a in enumerate(fts):
            for b in fts[i:]:
                if a != b:
                    func_cooc[a][b] += 1
                    func_cooc[b][a] += 1
    func_list = sorted(all_funcs)
    heatmaps["function_cooc"] = {
        "title": "Ko-okurencja tagów funkcji",
        "description": "Które funkcje najczęściej występują razem w skillach",
        "x_label": "Funkcje",
        "y_label": "Funkcje",
        "rows": func_list,
        "cols": func_list,
        "matrix": [[func_cooc[r][c] for c in func_list] for r in func_list]
    }

    return heatmaps


# ============================================================
# 2. PLANS — co-occurrence matrices from PLANS.md
# ============================================================

def parse_plans():
    """Parse PLANS.md to extract plan metadata from tables."""
    with open(PLANS_FILE) as f:
        content = f.read()

    plans = []

    # Extract plan blocks: PL-XXX with tables
    # Match all ### PL-XXX: Title blocks
    plan_blocks = re.findall(
        r'### (PL-\d+):\s*(.*?)(?=\n### PL-|\n## |\n---|\Z)',
        content,
        re.DOTALL
    )

    for pid, body in plan_blocks:
        body = body.strip()
        lines = body.split('\n')
        title = lines[0].strip() if lines else ""

        plan = {
            "nr": pid,
            "title": title,
            "thematic": [],
            "priority": "",
            "status": "",
            "modules": [],
            "skills": [],
            "taski": [],
        }

        # Extract tag values from table rows
        # Patterns like: | **Tematyczne** | `CORE`, `PORTAL` |
        tag_map = {
            "tematyczne": "thematic",
            "priorytet": "priority",
            "status": "status",
            "moduły": "modules",
            "moduł": "modules",
            "skille": "skills",
            "taski": "taski",
        }

        for line in body.split('\n'):
            line = line.strip()
            # Match | **Tag** | `value1` `value2` |
            tm = re.match(r'\|\s*\*\*([\wąęćłńóśźż]+)\*\*\s*\|\s*(.+?)\s*\|', line)
            if tm:
                key_raw = tm.group(1).lower()
                key_ascii = key_raw.replace('ę', 'e').replace('ł', 'l').replace('ó', 'o')
                val = tm.group(2)
                # Szukaj najpierw z oryginalnym kluczem (z polskimi znakami), potem z ascii
                mapped = tag_map.get(key_raw) or tag_map.get(key_ascii)
                if mapped == "thematic":
                    plan["thematic"] = re.findall(r'`(\w+)`', val)
                elif mapped == "priority":
                    p = re.findall(r'`([^`]+)`', val)
                    plan["priority"] = p[0] if p else val.strip()
                elif mapped == "status":
                    s = re.findall(r'`([^`]+)`', val)
                    plan["status"] = s[0] if s else val.strip()
                elif mapped == "modules":
                    plan["modules"] = re.findall(r'`([^`]+)`', val)
                elif mapped == "skills":
                    plan["skills"] = re.findall(r'`([^`]+)`', val)
                elif mapped == "taski":
                    plan["taski"] = re.findall(r'\*\*T\d\*\*.*', val)

            # Match task items: **T1** | text
            tm2 = re.match(r'\*\*(T\d)\*\*\s*\|\s*(.+)', line)
            if tm2:
                plan["taski"].append(f"{tm2.group(1)}: {tm2.group(2).strip()}")

        if plan["thematic"] or plan["modules"]:
            plans.append(plan)

    return plans


def build_plans_heatmaps(plans):
    heatmaps = {}

    # ── thematic × module ──
    th_mod = defaultdict(lambda: defaultdict(int))
    th_mod_rows = set()
    th_mod_cols = set()
    for p in plans:
        for th in p["thematic"]:
            for mod in p["modules"]:
                th_mod[th][mod] += 1
                th_mod_rows.add(th)
                th_mod_cols.add(mod)
    heatmaps["thematic_vs_module"] = {
        "title": "Tag tematyczny × Moduł systemu",
        "description": "Które moduły są zaangażowane w który obszar tematyczny planów",
        "x_label": "Moduły (M-)",
        "y_label": "Tagi tematyczne",
        "rows": sorted(th_mod_rows) if th_mod_rows else [],
        "cols": sorted(th_mod_cols) if th_mod_cols else [],
        "matrix": [[th_mod[r][c] for c in sorted(th_mod_cols)] for r in sorted(th_mod_rows)] if th_mod_rows else []
    }

    # ── thematic × status ──
    th_st = defaultdict(lambda: defaultdict(int))
    th_st_rows = set()
    th_st_cols = set()
    for p in plans:
        for th in p["thematic"]:
            st = p["status"]
            if st:
                th_st[th][st] += 1
                th_st_rows.add(th)
                th_st_cols.add(st)
    heatmaps["thematic_vs_status"] = {
        "title": "Tag tematyczny × Status wykonania",
        "description": "Które statusy dominują w którym obszarze tematycznym",
        "x_label": "Status",
        "y_label": "Tag tematyczny",
        "rows": sorted(th_st_rows) if th_st_rows else [],
        "cols": sorted(th_st_cols) if th_st_cols else [],
        "matrix": [[th_st[r][c] for c in sorted(th_st_cols)] for r in sorted(th_st_rows)] if th_st_rows else []
    }

    # ── priority × status ──
    pri_st = defaultdict(lambda: defaultdict(int))
    pri_st_rows = set()
    pri_st_cols = set()
    for p in plans:
        pri = p["priority"]
        st = p["status"]
        if pri and st:
            pri_st[pri][st] += 1
            pri_st_rows.add(pri)
            pri_st_cols.add(st)
    heatmaps["priority_vs_status"] = {
        "title": "Priorytet × Status wykonania",
        "description": "Rozkład planów według priorytetu i statusu",
        "x_label": "Status",
        "y_label": "Priorytet",
        "rows": sorted(pri_st_rows) if pri_st_rows else [],
        "cols": sorted(pri_st_cols) if pri_st_cols else [],
        "matrix": [[pri_st[r][c] for c in sorted(pri_st_cols)] for r in sorted(pri_st_rows)] if pri_st_rows else []
    }

    # ── module co-occurrence ──
    mod_cooc = defaultdict(lambda: defaultdict(int))
    all_mods = set()
    for p in plans:
        mods = p["modules"]
        for m in mods:
            all_mods.add(m)
        for i, a in enumerate(mods):
            for b in mods[i:]:
                if a != b:
                    mod_cooc[a][b] += 1
                    mod_cooc[b][a] += 1
    mod_list = sorted(all_mods) if all_mods else []
    heatmaps["module_cooc"] = {
        "title": "Ko-okurencja modułów w planach",
        "description": "Które moduły najczęściej występują razem w planach",
        "x_label": "Moduły",
        "y_label": "Moduły",
        "rows": mod_list,
        "cols": mod_list,
        "matrix": [[mod_cooc[r][c] for c in mod_list] for r in mod_list]
    }

    # ── thematic co-occurrence ──
    th_cooc = defaultdict(lambda: defaultdict(int))
    all_th = set()
    for p in plans:
        ths = p["thematic"]
        for th in ths:
            all_th.add(th)
        for i, a in enumerate(ths):
            for b in ths[i:]:
                if a != b:
                    th_cooc[a][b] += 1
                    th_cooc[b][a] += 1
    th_list = sorted(all_th) if all_th else []
    heatmaps["thematic_cooc"] = {
        "title": "Ko-okurencja tagów tematycznych w planach",
        "description": "Które obszary tematyczne najczęściej współwystępują w planach",
        "x_label": "Tagi tematyczne",
        "y_label": "Tagi tematyczne",
        "rows": th_list,
        "cols": th_list,
        "matrix": [[th_cooc[r][c] for c in th_list] for r in th_list]
    }

    return heatmaps


# ============================================================
# 3. FUNCTIONS — co-occurrence from FUNCTIONS.md structure
# ============================================================

def parse_functions():
    """Parse FUNCTIONS.md to extract module groupings."""
    with open(FUNCTIONS_FILE) as f:
        content = f.read()

    sections = []
    # Find all ## headers (module categories)
    section_pattern = re.finditer(r'^## (\d+)\.\s+`([^`]+)`\s*—\s*(.+)$', content, re.MULTILINE)
    for m in section_pattern:
        sections.append({
            "num": m.group(1),
            "path": m.group(2),
            "desc": m.group(3).strip(),
            "files": []
        })

    # Find ### sub-headers for groups within sections
    # And extract file entries
    # Simpler approach: just count table rows per section
    lines = content.split('\n')
    current_section = None
    for line in lines:
        # Section header
        sm = re.match(r'^## (\d+)\.\s+`([^`]+)`', line)
        if sm:
            current_section = sm.group(1)
            continue
        # Table row with file reference
        if current_section and '|' in line and '**' in line:
            tm = re.match(r'\|\s*\*\*([^*]+)\*\*', line)
            if tm:
                fname = tm.group(1).strip()
                for s in sections:
                    if s["num"] == current_section:
                        s["files"].append(fname)
                        break

    return sections


def build_functions_heatmaps(sections):
    heatmaps = {}

    # ── Section × file count ──
    if sections:
        heatmaps["section_file_count"] = {
            "title": "Liczba plików per sekcja FUNCTIONS.md",
            "description": "Ile plików w każdej kategorii modułów",
            "x_label": "Kategoria",
            "y_label": "Liczba plików",
            "rows": [s["path"] for s in sections],
            "cols": ["file_count"],
            "matrix": [[len(s["files"])] for s in sections]
        }

    # ── Sekcje: kategorie modułów (uporządkowane) ──
    cat_names = [s["path"] for s in sections]
    heatmaps["section_overview"] = {
        "title": "Przegląd kategorii modułów FUNCTIONS.md",
        "description": "Podział plików między kategorie modułów",
        "x_label": "Kategoria modułów",
        "y_label": "Liczba plików",
        "rows": cat_names,
        "cols": ["files"],
        "matrix": [[len(s["files"])] for s in sections]
    }

    return heatmaps


# ============================================================
# MAIN
# ============================================================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_data = {}

    # ── Skills ──
    print("📘 Skills: processing...")
    skills = load_skills()
    skills_h = build_skills_heatmaps(skills)
    all_data["skills"] = {
        "label": "SKILLS.md — Katalog Umiejętności",
        "count": len(skills),
        "heatmaps": skills_h
    }
    print(f"   {len(skills)} skills, {len(skills_h)} heatmaps")

    # ── Plans ──
    print("📗 Plans: processing...")
    plans = parse_plans()
    plans_h = build_plans_heatmaps(plans)
    all_data["plans"] = {
        "label": "PLANS.md — Katalog Planów",
        "count": len(plans),
        "heatmaps": plans_h
    }
    print(f"   {len(plans)} plans, {len(plans_h)} heatmaps")

    # ── Functions ──
    print("📙 Functions: processing...")
    functions = parse_functions()
    func_h = build_functions_heatmaps(functions)
    all_data["functions"] = {
        "label": "FUNCTIONS.md — Katalog Modułów",
        "count": len(functions),
        "heatmaps": func_h
    }
    print(f"   {len(functions)} sections, {len(func_h)} heatmaps")

    # ── Write output ──
    output_file = OUTPUT_DIR / "holonomy_heatmaps.json"
    with open(output_file, "w") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Zapisano: {output_file} ({os.path.getsize(output_file)} bajtów)")

    # Quick summary
    total_h = sum(len(v["heatmaps"]) for v in all_data.values())
    print(f"   Łącznie: {total_h} heatmapów")

    # ── Rejestracja w CIELingo + PhaseNav + NOEMA ──
    try:
        from ciel_geometry.writing_logger import log_creation
        log_creation(
            name="holonomy_heatmaps.json",
            description=f"Generator heatmap holonomii — {total_h} heatmapów ({len(skills)} skilli, {len(plans)} planów, {len(functions)} funkcji)",
            tags=["HEATMAP", "CATALOG", "HOLONOMY", "SKILLS", "PLANS", "FUNCTIONS"],
            wtype="HEATMAP",
            filepath="site/assets/data/heatmaps/holonomy_heatmaps.json",
            size_bytes=os.path.getsize(output_file),
        )
    except Exception as e:
        print(f"   ⚠ log_creation: {e}")


if __name__ == "__main__":
    main()
