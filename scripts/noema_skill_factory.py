#!/usr/bin/env python3
"""
NOEMA Skill Factory — batch conversion of .md docs + source enrichment.
Usage:
    python3 scripts/noema_skill_factory.py [--dry-run] [--verbose] [--reindex]
    
Modes:
  --dry-run    Preview only
  --verbose    Full logging
  --reindex    Only rebuild 00-INDEX (skip doc processing)

Processes:
  - ciel_lingophysics_lns_repo_v2_3/docs/  (46 docs)
  - ciel_lingophysics_lns_repo_v2_3/reports/ (16 reports)
  - CIEL_Orbital_Foundation_Packk/ (13 major + supporting)
  - CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/*/README.md + AGENT.md
  - ciel-omega-demo-main/docs/ (analogies, news, system, studies)
  - noema_holonomic_doctor/ (.md docs)
  - noema_learned/ (.md docs)
"""

import os, re, sys, json, textwrap, datetime
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
NOEMA_DIR = Path(os.environ.get("NOEMA_ROOT", str(_SCRIPT_DIR.parent)))
SKILLS_DIR = NOEMA_DIR / ".opencode" / "skills"
SRC_DIR = NOEMA_DIR / "src"
SCRIPTS_DIR = NOEMA_DIR / "scripts"

DRY_RUN = "--dry-run" in sys.argv
VERBOSE = "--verbose" in sys.argv
REINDEX_ONLY = "--reindex" in sys.argv

LOG_PATH = NOEMA_DIR / ".opencode" / "skill_factory.log"

def log(msg, force=False):
    if VERBOSE or force or DRY_RUN:
        prefix = "[DRY-RUN] " if DRY_RUN else ""
        line = f"{prefix}{msg}"
        print(line)
        with open(LOG_PATH, 'a') as f:
            f.write(f"[{datetime.datetime.now():%H:%M:%S}] {line}\n")

# ============================================================================
# EXTRACTORS
# ============================================================================

def extract_title(content, filename):
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    name = filename.replace('.md', '').replace('_', ' ').replace('-', ' ')
    name = re.sub(r'^\d+\s*', '', name).strip()
    return name or filename

def extract_formulas(content, max_count=6):
    formulas = []
    for m in re.finditer(r'\$\$(.+?)\$\$', content, re.DOTALL):
        formulas.append(m.group(1).strip()[:200])
    for m in re.finditer(r'\\\[(.+?)\\\]', content, re.DOTALL):
        formulas.append(m.group(1).strip()[:200])
    return formulas[:max_count]

def extract_bullets(content, max_count=12):
    bullets = []
    for m in re.finditer(r'^[\s]*[-*]\s+(.+)$', content, re.MULTILINE):
        line = m.group(1).strip()
        if len(line) > 15 and line not in bullets:
            bullets.append(line)
    return bullets[:max_count]

def extract_code_blocks(content, max_count=3):
    blocks = []
    for m in re.finditer(r'```(?:python)?\n(.+?)```', content, re.DOTALL):
        code = m.group(1).strip()
        if len(code) > 30:
            blocks.append(code[:500])
    return blocks[:max_count]

def extract_definitions(content):
    defs = []
    for m in re.finditer(r'\*\*(.+?)\*\*\s*[—–-]\s*(.+?)(?:\n|$)', content):
        defs.append((m.group(1).strip(), m.group(2).strip()[:200]))
    return defs[:6]

def extract_tables(content, max_count=3):
    lines = content.split('\n')
    tables = []
    current = []
    for line in lines:
        if '|' in line and '---' not in line:
            current.append(line.strip())
        elif current and len(current) >= 3:
            tables.append('\n'.join(current[:8]))
            current = []
        else:
            current = []
    if len(current) >= 3:
        tables.append('\n'.join(current[:8]))
    return tables[:max_count]

def extract_sections(content):
    """Extract H2 and H3 section titles with their first paragraph."""
    sections = []
    current_heading = None
    current_text = []
    for line in content.split('\n'):
        if line.startswith('## ') or line.startswith('### '):
            if current_heading and current_text:
                sections.append((current_heading, ' '.join(current_text)[:200]))
            current_heading = line.strip('# ').strip()
            current_text = []
        elif current_heading and line.strip():
            current_text.append(line.strip()[:100])
    if current_heading and current_text:
        sections.append((current_heading, ' '.join(current_text)[:200]))
    return sections[:8]

# ============================================================================
# SKILL GENERATION
# ============================================================================

def make_skill_name(filename):
    name = filename.replace('.md', '').replace('.json', '')
    name = re.sub(r'^\d+[\s_]', '', name)
    name = name.lower().replace('_', '-').replace(' ', '-')
    return re.sub(r'-+', '-', name).strip('-')

def catname_from_source(filepath):
    rel = filepath.relative_to(SRC_DIR)
    parts = list(rel.parts)
    root_map = {
        'ciel_lingophysics_lns_repo_v2_3': 'lns',
        'CIEL_Orbital_Foundation_Packk': 'orbital',
        'CIEL_OMEGA_COMPLETE_SYSTEM': 'omega',
        'ciel-omega-demo-main': 'odemo',
        'noema_holonomic_doctor': 'holodoctor',
        'noema_learned': 'learned',
    }
    for key, val in root_map.items():
        if key in parts:
            return val
    return 'doc'

def generate_skill_md(data, category, source_rel_path):
    title = data['title']
    skill_name = make_skill_name(data['filename'])
    desc = data['title'][:120] if len(data['title']) > 10 else f"Doc: {data['filename']}"
    
    lines = ['---']
    lines.append(f'name: {skill_name}')
    lines.append('description: >')
    lines.append(f'  {desc[:120]}')
    lines.append(f'  Source: {source_rel_path}')
    lines.append('---')
    lines.append('')
    lines.append(f'# {title}')
    lines.append('')
    
    # Sections
    if data['sections']:
        lines.append('## Contents')
        lines.append('')
        for h, t in data['sections']:
            t_short = t[:120] if t else ''
            lines.append(f'- **{h}**: {t_short}')
        lines.append('')
    
    # Formulas
    if data['formulas']:
        lines.append('## Formulas')
        lines.append('')
        for f in data['formulas']:
            lines.append(f'- `{f[:180]}`')
        lines.append('')
    
    # Definitions
    if data['definitions']:
        lines.append('## Definitions')
        lines.append('')
        for term, desc in data['definitions']:
            lines.append(f'- **{term}**: {desc[:180]}')
        lines.append('')
    
    # Key points
    if data['bullets']:
        lines.append('## Key Points')
        lines.append('')
        for b in data['bullets']:
            lines.append(f'- {b[:200]}')
        lines.append('')
    
    # Tables
    if data['tables']:
        lines.append('## Tables')
        lines.append('')
        for t in data['tables']:
            lines.append(t)
            lines.append('')
    
    # Code
    if data['code_blocks']:
        lines.append('## Code')
        lines.append('')
        for cb in data['code_blocks']:
            lang = 'python' if 'import' in cb or 'def ' in cb else ''
            lines.append(f'```{lang}')
            lines.append(cb[:500])
            lines.append('```')
            lines.append('')
    
    lines.append('---')
    lines.append(f'*Extracted from: `{source_rel_path}` ({data["line_count"]} lines, {data["size"]}B)*')
    
    return '\n'.join(lines), skill_name

def process_md_file(filepath):
    with open(filepath, 'r', errors='replace') as f:
        content = f.read()
    return {
        'title': extract_title(content, filepath.name),
        'filename': filepath.name,
        'formulas': extract_formulas(content),
        'bullets': extract_bullets(content),
        'code_blocks': extract_code_blocks(content),
        'definitions': extract_definitions(content),
        'tables': extract_tables(content),
        'sections': extract_sections(content),
        'line_count': len(content.splitlines()),
        'size': len(content),
    }

def write_skill(data, category, filepath):
    rel = filepath.relative_to(NOEMA_DIR)
    content, skill_name = generate_skill_md(data, category, str(rel))
    
    subdir = f"{category}-{skill_name}"
    target_dir = SKILLS_DIR / subdir
    target_file = target_dir / "SKILL.md"
    
    if target_file.exists():
        existing_size = target_file.stat().st_size
        new_size = len(content)
        if new_size > existing_size * 1.5:
            log(f"  UPDATE (larger): {subdir} ({existing_size}→{new_size}B)")
        else:
            log(f"  SKIP (exists): {subdir}")
            return False
    else:
        log(f"  NEW: {subdir} ({new_size if 'new_size' in dir() else len(content)} chars)")
    
    if DRY_RUN:
        return True
    
    target_dir.mkdir(parents=True, exist_ok=True)
    with open(target_file, 'w') as f:
        f.write(content)
    return True

# ============================================================================
# SCANNERS
# ============================================================================

def scan_directory(base_dir, skip_patterns=None):
    if not base_dir.exists():
        return []
    results = []
    for fpath in base_dir.rglob("*.md"):
        rel = fpath.relative_to(NOEMA_DIR)
        if skip_patterns:
            if any(sp in str(rel) for sp in skip_patterns):
                continue
        results.append(fpath)
    return sorted(results)

# ============================================================================
# 00-INDEX REBUILDER
# ============================================================================

def rebuild_index():
    log("\n=== Rebuilding 00-INDEX ===", force=True)
    
    # Categorize all skills
    categories = {
        'surface-memory': [],
        'phasenav-operators': [],
        'daemons': [],
        'cielingo': [],
        'geometry': [],
        'scripts': [],
        'lns-lingophysics': [],
        'lns-reports': [],
        'orbital-foundation': [],
        'omega-subsystem': [],
        'omega-demo': [],
        'holonomic-doctor': [],
        'documentation': [],
        'core': [],
    }
    
    def cat_for_skill(name):
        name_l = name.lower()
        if name_l.startswith('surface-') or name_l.startswith('tiered-') or name_l.startswith('phase-memory'):
            return 'surface-memory'
        if name_l.startswith('operator-') or name_l.startswith('phasenav-') or name_l.startswith('teleusing') or name_l.startswith('continuous-'):
            return 'phasenav-operators'
        if name_l.startswith('noema-') and any(d in name_l for d in ('daemon', 'watchdog', 'hook', 'sensor')):
            return 'daemons'
        if name_l.startswith('daemon-') or name_l in ('synchronize', 'kuramoto-', 'linux-sensor', 'neutrino-bus', 'agent-attractor', 'resonance-bridge'):
            return 'daemons'
        if name_l.startswith('cielingo') or name_l.startswith('ciel-') and 'memory' not in name_l and 'sot' not in name_l:
            return 'cielingo'
        if name_l.startswith('lns-') and '-rpt' not in name_l:
            return 'lns-lingophysics'
        if 'lns-rpt' in name_l:
            return 'lns-reports'
        if name_l.startswith('orbital-') or name_l.startswith('doc-orbital'):
            return 'orbital-foundation'
        if name_l.startswith('omega-') or name_l.startswith('doc-omega'):
            return 'omega-subsystem'
        if name_l.startswith('odemo-') or name_l.startswith('doc-odemo'):
            return 'omega-demo'
        if name_l.startswith('holodoctor') or name_l.startswith('doc-holodoctor'):
            return 'holonomic-doctor'
        if name_l.startswith('doc-') or name_l.startswith('nbody') or name_l.startswith('tardis'):
            return 'documentation'
        if name_l.startswith('noema-') or name_l.startswith('ciel-') or name_l.startswith('htri') or name_l.startswith('eBPF'):
            return 'scripts'
        return 'core'
    
    index_entries = {}
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        # Read description from frontmatter
        content = skill_file.read_text()
        desc = ""
        name = skill_dir.name
        m_desc = re.search(r'description:\s*>\s*\n\s+(.+?)(?:\n---|\Z)', content, re.DOTALL)
        if m_desc:
            desc = m_desc.group(1).strip()[:80]
        
        cat = cat_for_skill(name)
        categories[cat].append((name, desc))
    
    # Generate INDEX
    lines = ['---',
             'name: 00-INDEX',
             'description: >',
             f'  MASTER INDEX wszystkich skilli NOEMA. {sum(len(v) for v in categories.values())} skills.',
             '  Szukaj po kategorii: surface, daemon, phasenav, cielyngo, memory, geometry, scripts.',
             '---',
             '',
             '# NOEMA Skills — Master Index',
             '',
             '_Auto-generated by skill_factory.py_',
             '']
    
    cat_labels = {
        'surface-memory': '## Surface & Memory',
        'phasenav-operators': '## PhaseNav & Operators',
        'daemons': '## Daemons',
        'cielingo': '## CIELingo',
        'geometry': '## Geometry & Physics',
        'scripts': '## Scripts & Tools',
        'lns-lingophysics': '## LNS Lingophysics (46 docs)',
        'lns-reports': '## LNS Reports (v0.8-v2.3)',
        'orbital-foundation': '## Orbital Foundation Pack',
        'omega-subsystem': '## Omega Subsystem',
        'omega-demo': '## Omega Demo Docs',
        'holonomic-doctor': '## Holonomic Doctor',
        'documentation': '## Documentation Pointers',
        'core': '## Core',
    }
    
    for cat, label in cat_labels.items():
        entries = categories.get(cat, [])
        if not entries:
            continue
        lines.append(label)
        lines.append('')
        lines.append('| Skill | Co daje |')
        lines.append('|-------|---------|')
        for name, desc in sorted(entries):
            desc_clean = desc[:80] if desc else name
            lines.append(f'| `{name}` | {desc_clean} |')
        lines.append('')
    
    lines.append('---')
    lines.append(f'*Total: {sum(len(v) for v in categories.values())} skills. Updated {datetime.datetime.now():%Y-%m-%d %H:%M}*')
    
    index_content = '\n'.join(lines)
    index_file = SKILLS_DIR / "00-INDEX" / "SKILL.md"
    
    if DRY_RUN:
        log(f"  WOULD UPDATE: 00-INDEX ({len(index_content)} chars, {sum(len(v) for v in categories.values())} entries)", force=True)
    else:
        index_file.parent.mkdir(parents=True, exist_ok=True)
        with open(index_file, 'w') as f:
            f.write(index_content)
        log(f"  UPDATED: 00-INDEX ({len(index_content)} chars, {sum(len(v) for v in categories.values())} entries)", force=True)

# ============================================================================
# MAIN
# ============================================================================

def main():
    global SKILLS_DIR
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    
    log(f"{'='*60}", force=True)
    log(f"NOEMA Skill Factory — {datetime.datetime.now():%Y-%m-%d %H:%M}", force=True)
    log(f"{'='*60}", force=True)
    
    if REINDEX_ONLY:
        rebuild_index()
        return
    
    total_created = 0
    collection_stats = {}
    
    # ---- 1. LNS Lingophysics docs ----
    lns_base = SRC_DIR / "ciel_lingophysics_lns_repo_v2_3" / "docs"
    lns_files = scan_directory(lns_base)
    log(f"\n--- LNS Lingophysics ({len(lns_files)} files) ---")
    count = 0
    for fp in lns_files:
        data = process_md_file(fp)
        if write_skill(data, 'lns', fp):
            count += 1
    collection_stats['lns-docs'] = count
    total_created += count
    
    # ---- 2. LNS Reports ----
    rpt_base = SRC_DIR / "ciel_lingophysics_lns_repo_v2_3" / "reports"
    rpt_files = [f for f in scan_directory(rpt_base) if f.suffix == '.md']
    log(f"\n--- LNS Reports ({len(rpt_files)} files) ---")
    count = 0
    for fp in rpt_files:
        data = process_md_file(fp)
        cat = 'lns-rpt'
        if write_skill(data, cat, fp):
            count += 1
    collection_stats['lns-reports'] = count
    total_created += count
    
    # ---- 3. Orbital Foundation Pack ----
    orbital_base = SRC_DIR / "CIEL_Orbital_Foundation_Packk"
    orbital_files = [f for f in scan_directory(orbital_base) if f.suffix == '.md']
    log(f"\n--- Orbital Foundation Pack ({len(orbital_files)} files) ---")
    count = 0
    for fp in orbital_files:
        data = process_md_file(fp)
        if write_skill(data, 'orbital', fp):
            count += 1
    collection_stats['orbital'] = count
    total_created += count
    
    # ---- 4. Omega subsystem README/AGENT ----
    omega_base = SRC_DIR / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"
    omega_targets = []
    for fp in scan_directory(omega_base):
        rel = fp.relative_to(omega_base)
        if fp.name in ('README.md', 'AGENT.md') and len(rel.parts) >= 2:
            omega_targets.append(fp)
    log(f"\n--- Omega subsystem ({len(omega_targets)} files) ---")
    count = 0
    for fp in omega_targets:
        data = process_md_file(fp)
        sub = fp.relative_to(omega_base).parts[0]
        cat = f"omega-{sub}"
        if write_skill(data, cat, fp):
            count += 1
    collection_stats['omega'] = count
    total_created += count
    
    # ---- 5. ciel-omega-demo-main/docs/ ----
    demo_base = SRC_DIR / "ciel-omega-demo-main" / "docs"
    demo_files = scan_directory(demo_base)
    log(f"\n--- Omega Demo ({len(demo_files)} files) ---")
    count = 0
    for fp in demo_files:
        data = process_md_file(fp)
        rel = fp.relative_to(SRC_DIR / "ciel-omega-demo-main" / "docs")
        sub_cat = rel.parts[0].lower() if len(rel.parts) > 1 else 'root'
        cat = f"odemo-{sub_cat}"
        if write_skill(data, cat, fp):
            count += 1
    collection_stats['omega-demo'] = count
    total_created += count
    
    # ---- 6. noema_holonomic_doctor ----
    holo_base = SRC_DIR / "noema_holonomic_doctor"
    holo_files = scan_directory(holo_base)
    log(f"\n--- Holonomic Doctor ({len(holo_files)} files) ---")
    count = 0
    for fp in holo_files:
        data = process_md_file(fp)
        if write_skill(data, 'holodoctor', fp):
            count += 1
    collection_stats['holodoctor'] = count
    total_created += count
    
    # ---- 7. noema_learned ----
    learned_base = SRC_DIR / "noema_learned"
    learned_files = scan_directory(learned_base)
    log(f"\n--- Learned ({len(learned_files)} files) ---")
    count = 0
    for fp in learned_files:
        data = process_md_file(fp)
        if write_skill(data, 'learned', fp):
            count += 1
    collection_stats['learned'] = count
    total_created += count
    
    # ---- Summary ----
    log(f"\n{'='*60}", force=True)
    log("RESULTS", force=True)
    log(f"{'='*60}", force=True)
    for coll, cnt in collection_stats.items():
        log(f"  {coll}: {cnt} new skills", force=True)
    log(f"  TOTAL NEW: {total_created}", force=True)
    
    existing = len(list(SKILLS_DIR.glob("*/SKILL.md")))
    log(f"  TOTAL SKILLS: {existing}", force=True)
    log("", force=True)
    
    # Rebuild index after additions
    if total_created > 0 and not DRY_RUN:
        rebuild_index()
    
    if DRY_RUN:
        log("\nRemove --dry-run to execute.", force=True)

if __name__ == "__main__":
    main()
