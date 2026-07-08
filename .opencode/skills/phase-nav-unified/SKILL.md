# PhaseNav Unified Index + Multiskill

Połączone indeksy PhaseNav: UnifiedPhaseNavIndex + MultiskillOrchestrator. Łączy skills, knowledge_db, linux_cards, TaskPlan DB, task_queue, system_map w jeden 24D indeks.

---

## Źródła

- **src/ciel_geometry/phasenav_unified.py** → moduł `ciel_geometry.phasenav_unified` (675 linii)
  ```python
  # Import:
  from ciel_geometry.phasenav_unified import ...
  ```
- **src/ciel_geometry/multiskill.py** → moduł `ciel_geometry.multiskill` (237 linii)
  ```python
  # Import:
  from ciel_geometry.multiskill import ...
  ```

---

## src/ciel_geometry/phasenav_unified.py

```python
from ciel_geometry.phasenav_unified import ...
```

**Klasy:**
- `UnifiedPhaseNavIndex`
**Funkcje:**
- `__init__()`
- `_build()`
- `_add()`
- `_load_skills()`
- `_load_knowledge_db()`
- `_load_palace_rooms()`
- `_load_linux_cards()`
- `_load_taskplan_db()`
- `_load_task_queue()`
- `_load_system_map()`
- `_text_to_phi()`
- `_angular_sim()`
- `count()`
- `search()`
- `_search_linux_cards_structured()`
- `search_by_phi()`
- `filter_by_source()`
- `_log_stats()`
- `stats()`
- `rebuild()`

---

## src/ciel_geometry/multiskill.py

```python
from ciel_geometry.multiskill import ...
```

**Klasy:**
- `MultiskillOrchestrator`
**Funkcje:**
- `__init__()`
- `_text_to_phi()`
- `_load()`
- `count()`
- `resolve()`
- `resolve_chain()`
- `neighbors()`
- `cluster()`
- `save_index()`
- `describe()`

---
