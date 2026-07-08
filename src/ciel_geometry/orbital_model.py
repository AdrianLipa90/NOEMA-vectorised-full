#!/usr/bin/env python3
"""
orbital_model.py — autopoiesis orbitalna NOEMY.

Systemy emergują z orbit. Nie ma osobnej definicji systemu —
system jest zbiorem swoich relacji orbitalnych.

Każda orbita = attractor → satelita z właściwościami:
  - weight: siła sprzężenia (W_ij w Kuramoto)
  - phase_shift: przesunięcie fazowe Δφ
  - resonance: stosunek częstotliwości (np. "3:2", "1:1")
  - harmonic: numer harmonicznej

Model jest IDEMPOTENTNY: ten sam zestaw orbit zawsze daje ten sam wszechświat.
"""

import json
import math
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


# ========================================================================
# CORE DATA
# ========================================================================

@dataclass
class Orbit:
    """Pojedyncza orbita — jedyny byt pierwszo-klasowy."""
    attractor_id: str
    satellite_id: str
    weight: float = 0.5        # W_ij (0..1)
    phase_shift: float = 0.0   # Δφ w radianach (0..2π)
    resonance_num: int = 1     # licznik rezonansu (np. 3 dla 3:2)
    resonance_den: int = 1     # mianownik rezonansu (np. 2 dla 3:2)
    harmonic: int = 1          # numer harmonicznej
    label: str = ""
    
    @property
    def id(self) -> str:
        return f"{self.attractor_id}→{self.satellite_id}"
    
    @property
    def resonance_ratio(self) -> float:
        """Stosunek częstotliwości satelita/attractor."""
        return self.resonance_num / self.resonance_den if self.resonance_den else 1.0
    
    @property
    def orbital_radius(self) -> float:
        """Promień orbitalny = odwrotność wagi, znormalizowany."""
        return 1.0 / (self.weight + 0.1) - 0.5
    
    def to_dict(self) -> dict:
        return {
            "attractor_id": self.attractor_id,
            "satellite_id": self.satellite_id,
            "weight": self.weight,
            "phase_shift": round(self.phase_shift, 4),
            "resonance": f"{self.resonance_num}:{self.resonance_den}",
            "harmonic": self.harmonic,
            "label": self.label,
            "orbital_radius": round(self.orbital_radius, 4),
        }


@dataclass
class System:
    """System — emerguje z orbit. Nie istnieje samodzielnie."""
    id: str
    name: str = ""
    type: str = "system"
    ordinal: str = ""
    
    # Wypełniane przez OrbitalUniverse
    orbits_as_attractor: list = field(default_factory=list)
    orbits_as_satellite: list = field(default_factory=list)
    
    @property
    def attractor_count(self) -> int:
        return len(self.orbits_as_attractor)
    
    @property
    def satellite_count(self) -> int:
        return len(self.orbits_as_satellite)
    
    @property
    def total_orbits(self) -> int:
        return self.attractor_count + self.satellite_count
    
    @property
    def net_gravity(self) -> float:
        """Grawitacja netto: + attractor, - satellite."""
        return self.attractor_count - self.satellite_count
    
    @property
    def total_weight(self) -> float:
        """Suma wag wszystkich orbit systemu."""
        w = sum(o.weight for o in self.orbits_as_attractor)
        w += sum(o.weight for o in self.orbits_as_satellite)
        return w
    
    @property
    def mean_phase(self) -> float:
        """Średnia faza systemu (ważona)."""
        phases = [(o.weight, o.phase_shift) for o in self.orbits_as_attractor]
        phases += [(o.weight, -o.phase_shift) for o in self.orbits_as_satellite]
        if not phases:
            return 0.0
        total_w = sum(w for w, _ in phases)
        if total_w == 0:
            return 0.0
        return sum(w * p for w, p in phases) / total_w


# ========================================================================
# ORBITAL UNIVERSE — jedyne źródło prawdy
# ========================================================================

class OrbitalUniverse:
    """Wszechświat orbitalny. Przechowuje tylko orbity. Systemy emergują."""
    
    def __init__(self):
        self._orbits: dict[str, Orbit] = {}
        self._system_meta: dict[str, dict] = {}  # id → {name, type, ordinal}
    
    # --- ORBITY ---
    
    def add_orbit(self, attractor_id: str, satellite_id: str,
                  weight: float = 0.5, phase_shift: float = 0.0,
                  resonance: str = "1:1", harmonic: int = 1,
                  label: str = "") -> Orbit:
        """Dodaje orbitę. Idempotentne — drugi raz zwraca istniejącą."""
        key = f"{attractor_id}→{satellite_id}"
        if key in self._orbits:
            return self._orbits[key]
        
        # Parsuj rezonans "3:2" → (3, 2)
        if ':' in resonance:
            parts = resonance.split(':')
            rn = int(parts[0])
            rd = int(parts[1]) if len(parts) > 1 else 1
        else:
            rn, rd = 1, 1
        
        orb = Orbit(
            attractor_id=attractor_id,
            satellite_id=satellite_id,
            weight=weight,
            phase_shift=phase_shift,
            resonance_num=rn,
            resonance_den=rd,
            harmonic=harmonic,
            label=label
        )
        self._orbits[key] = orb
        return orb
    
    def add_orbit_raw(self, attr_id: str, sat_id: str, 
                      weight: float = 0.5, phase_shift: float = 0.0,
                      resonance: str = "1:1", harmonic: int = 1,
                      label: str = "") -> Orbit:
        """Alias dla add_orbit."""
        return self.add_orbit(attr_id, sat_id, weight, phase_shift, resonance, harmonic, label)
    
    def add_mutual_orbit(self, a_id: str, b_id: str,
                         weight_ab: float = 0.5, weight_ba: float = 0.5,
                         phase_shift_ab: float = 0.0, phase_shift_ba: float = 0.0,
                         resonance: str = "1:1",
                         label_ab: str = "", label_ba: str = ""):
        """Układ podwójny: A ←→ B."""
        self.add_orbit(a_id, b_id, weight_ab, phase_shift_ab, resonance, label=label_ab)
        self.add_orbit(b_id, a_id, weight_ba, phase_shift_ba, resonance, label=label_ba)
    
    @property
    def orbits(self) -> dict[str, Orbit]:
        return dict(self._orbits)
    
    @property
    def orbit_count(self) -> int:
        return len(self._orbits)
    
    # --- SYSTEMY (emergują z orbit) ---
    
    @property
    def systems(self) -> dict[str, System]:
        """Systemy emergują z orbit — dynamicznie."""
        ids = set()
        for orb in self._orbits.values():
            ids.add(orb.attractor_id)
            ids.add(orb.satellite_id)
        
        result = {}
        for sid in ids:
            meta = self._system_meta.get(sid, {})
            sys = System(
                id=sid,
                name=meta.get("name", sid),
                type=meta.get("type", "system"),
                ordinal=meta.get("ordinal", ""),
            )
            sys.orbits_as_attractor = [o for o in self._orbits.values() 
                                        if o.attractor_id == sid]
            sys.orbits_as_satellite = [o for o in self._orbits.values()
                                        if o.satellite_id == sid]
            result[sid] = sys
        return result
    
    def get_system(self, sid: str) -> Optional[System]:
        return self.systems.get(sid)
    
    def set_system_meta(self, sid: str, name: str = "", type: str = "system",
                        ordinal: str = ""):
        """Ustawia metadane systemu (nie wpływa na emergencję)."""
        if sid not in self._system_meta:
            self._system_meta[sid] = {}
        if name:
            self._system_meta[sid]["name"] = name
        if type:
            self._system_meta[sid]["type"] = type
        if ordinal:
            self._system_meta[sid]["ordinal"] = ordinal
    
    @property
    def system_count(self) -> int:
        return len(self.systems)
    
    # --- KWERENDY ---
    
    def get_satellites(self, attractor_id: str) -> list[tuple[System, Orbit]]:
        """Satelici atraktora."""
        sys_map = self.systems
        return [(sys_map[o.satellite_id], o) 
                for o in self._orbits.values() 
                if o.attractor_id == attractor_id
                and o.satellite_id in sys_map]
    
    def get_attractors(self, satellite_id: str) -> list[tuple[System, Orbit]]:
        """Atraktorzy satelity."""
        sys_map = self.systems
        return [(sys_map[o.attractor_id], o) 
                for o in self._orbits.values() 
                if o.satellite_id == satellite_id
                and o.attractor_id in sys_map]
    
    def get_orbit_between(self, a_id: str, b_id: str) -> Optional[Orbit]:
        """Zwraca orbitę A→B jeśli istnieje."""
        return self._orbits.get(f"{a_id}→{b_id}")
    
    def has_mutual(self, a_id: str, b_id: str) -> bool:
        """Czy istnieją orbity w obie strony (układ podwójny)?"""
        return (f"{a_id}→{b_id}" in self._orbits and 
                f"{b_id}→{a_id}" in self._orbits)
    
    def get_primary_attractors(self, min_gravity: int = 1) -> list[System]:
        """Systemy które są bardziej attractorami niż satelitami."""
        return sorted(
            [s for s in self.systems.values() if s.net_gravity >= min_gravity],
            key=lambda s: -s.net_gravity
        )
    
    def get_multi_orbit_systems(self, min_orbits: int = 3) -> list[System]:
        """Systemy na wielu orbitach."""
        return sorted(
            [s for s in self.systems.values() if s.total_orbits >= min_orbits],
            key=lambda s: -s.total_orbits
        )
    
    # --- FAZOWE ---
    
    def compute_phase_field(self) -> dict[str, float]:
        """Oblicza pole fazowe: każdy system dostaje φ z sumy orbit."""
        sys_map = self.systems
        phases = {}
        for sid, sys in sys_map.items():
            phases[sid] = sys.mean_phase
        return phases
    
    def compute_coherence(self) -> float:
        """Koherencja globalna: |Σ e^{iφ}| / N (jak w Kuramoto)."""
        phases = self.compute_phase_field()
        if not phases:
            return 0.0
        real = sum(math.cos(p) for p in phases.values())
        imag = sum(math.sin(p) for p in phases.values())
        n = len(phases)
        return math.sqrt(real*real + imag*imag) / n if n > 0 else 0.0
    
    # --- WIZUALIZACJA ---
    
    def render(self, center_id: Optional[str] = None, max_depth: int = 4) -> str:
        if center_id:
            return self._render_from(center_id, max_depth)
        return self._render_nbody(max_depth)
    
    def _render_nbody(self, max_depth: int) -> str:
        lines = ["=== ORBITAL UNIVERSE — AUTOPOIESIS ===", ""]
        lines.append(f"Orbits: {len(self._orbits)} | Systems: {self.system_count} | "
                    f"Coherence: {self.compute_coherence():.4f}")
        lines.append("")
        
        primary = self.get_primary_attractors(min_gravity=0)
        
        # Znajdź układy podwójne
        binaries = []
        seen = set()
        for a in primary:
            if a.id in seen:
                continue
            for b in primary:
                if b.id == a.id or b.id in seen:
                    continue
                if self.has_mutual(a.id, b.id):
                    binaries.append((a, b))
                    seen.add(a.id)
                    seen.add(b.id)
                    break
        
        solo = [p for p in primary if p.id not in seen]
        
        if binaries:
            lines.append(f"── UKŁADY PODWÓJNE ({len(binaries)}) ──")
            lines.append("")
            for a, b in binaries:
                ab = self.get_orbit_between(a.id, b.id)
                ba = self.get_orbit_between(b.id, a.id)
                lines.append(f"  ★ {a.ordinal} {a.name} [{a.type}]  ←→  "
                           f"★ {b.ordinal} {b.name} [{b.type}]")
                lines.append(f"     w={ab.weight:.2f}/{ba.weight:.2f}  "
                           f"φ={ab.phase_shift:.2f}/{ba.phase_shift:.2f}  "
                           f"r={ab.resonance_num}:{ab.resonance_den}")
                lines.append("")
                for s, orb in self.get_satellites(a.id):
                    if s.id != b.id:
                        lines.append(f"     ◇ {s.name}  w={orb.weight:.2f} φ={orb.phase_shift:.2f}")
                        self._render_subs(s.id, lines, 2, max_depth)
                for s, orb in self.get_satellites(b.id):
                    if s.id != a.id:
                        lines.append(f"     ◇ {s.name}  w={orb.weight:.2f} φ={orb.phase_shift:.2f}")
                        self._render_subs(s.id, lines, 2, max_depth)
                lines.append("")
        
        if solo:
            if binaries:
                lines.append(f"── POZOSTAŁE ATRAKTORY ({len(solo)}) ──")
                lines.append("")
            for a in solo:
                lines.append(f"  ★ {a.ordinal} {a.name} [{a.type}]  gravity={a.net_gravity}  "
                           f"w_sum={a.total_weight:.2f}  φ={a.mean_phase:.2f}")
                for s, orb in self.get_satellites(a.id):
                    lines.append(f"     ◇ {s.name}  w={orb.weight:.2f} φ={orb.phase_shift:.2f}")
                    self._render_subs(s.id, lines, 2, max_depth)
                lines.append("")
        
        # Czyste satelity (bez własnych attractorów)
        pure_sats = sorted(
            [s for s in self.systems.values()
             if s.attractor_count == 0 and s.satellite_count > 0],
            key=lambda s: -s.total_weight
        )
        if pure_sats:
            lines.append(f"── CZYSTE SATELITY ({len(pure_sats)}) ──")
            for s in pure_sats[:10]:
                attrs = self.get_attractors(s.id)
                a_str = ", ".join(f"{a.name}(w={o.weight:.2f})" for a, o in attrs[:3])
                if len(attrs) > 3:
                    a_str += f" ... +{len(attrs)-3}"
                lines.append(f"     ◇ {s.name} ← {a_str}")
            if len(pure_sats) > 10:
                lines.append(f"     ... i {len(pure_sats)-10} więcej")
        
        lines.append("")
        lines.append(self._stats())
        return '\n'.join(lines)
    
    def _render_from(self, center_id: str, max_depth: int) -> str:
        center = self.get_system(center_id)
        if not center:
            return f"System '{center_id}' nie istnieje"
        
        lines = [f"=== ORBITAL VIEW: {center.name} ===", ""]
        lines.append(f"  ★ {center.ordinal} {center.name} [{center.type}]")
        lines.append(f"     attractor of {center.attractor_count} | "
                    f"satellite of {center.satellite_count} | "
                    f"net gravity: {center.net_gravity}")
        
        sats = self.get_satellites(center_id)
        if sats:
            lines.append("")
            lines.append(f"  ── SATELLITES ({len(sats)}) ──")
            for s, orb in sats:
                lines.append(f"     ◇ {s.ordinal} {s.name}  "
                           f"w={orb.weight:.2f} φ={orb.phase_shift:.2f} "
                           f"r={orb.resonance_num}:{orb.resonance_den}")
                self._render_subs(s.id, lines, 2, max_depth)
        
        attrs = self.get_attractors(center_id)
        if attrs:
            lines.append("")
            lines.append(f"  ── ATTRACTORS ({len(attrs)}) ──")
            for a, orb in attrs:
                lines.append(f"     ★ {a.ordinal} {a.name}  "
                           f"w={orb.weight:.2f} φ={orb.phase_shift:.2f} "
                           f"r={orb.resonance_num}:{orb.resonance_den}")
        
        lines.append("")
        lines.append(f"Phase: {center.mean_phase:.4f} rad")
        return '\n'.join(lines)
    
    def _render_subs(self, sid: str, lines: list, depth: int = 1, max_depth: int = 3):
        if depth >= max_depth:
            return
        sats = self.get_satellites(sid)
        indent = "     " + "  " * (depth - 1)
        for s, orb in sats:
            lines.append(f"{indent}  ◇ {s.name}  w={orb.weight:.2f} φ={orb.phase_shift:.2f}")
            self._render_subs(s.id, lines, depth + 1, max_depth)
    
    def _stats(self) -> str:
        primary = len(self.get_primary_attractors(1))
        multi = len(self.get_multi_orbit_systems(3))
        binaries = sum(1 for a in self.systems for b in self.systems
                      if a < b and self.has_mutual(a, b))
        coherence = self.compute_coherence()
        return (f"Systems: {self.system_count} | Orbits: {self.orbit_count} | "
                f"Primaries: {primary} | Binaries: {binaries} | "
                f"Multi-orbit(3+): {multi} | Coherence: {coherence:.4f}")
    
    # --- SERIALIZACJA ---
    
    def to_dict(self) -> dict:
        return {
            "orbits": [o.to_dict() for o in self._orbits.values()],
            "system_meta": dict(self._system_meta),
        }
    
    def save(self, path: Optional[Path] = None):
        """Zapisuje do system_map_v3.json."""
        if path is None:
            path = Path(__file__).resolve().parent.parent.parent / "system_map_v3.json"
        data = self.to_system_map_v2()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Zapisano: {path} ({self.system_count} sys, {self.orbit_count} orb)")
    
    def to_system_map_v2(self) -> dict:
        """Eksport do formatu system_map_v2.json."""
        sys_map = self.systems
        
        systems_list = []
        for sid, sys in sys_map.items():
            meta = self._system_meta.get(sid, {})
            systems_list.append({
                "id": sid,
                "name": meta.get("name", sys.name),
                "type": meta.get("type", sys.type),
                "ordinal": meta.get("ordinal", sys.ordinal),
                "gravity": sys.net_gravity,
                "total_orbits": sys.total_orbits,
                "mean_phase": round(sys.mean_phase, 4),
                "total_weight": round(sys.total_weight, 4),
            })
        
        connections = []
        for orb in self._orbits.values():
            connections.append({
                "from": orb.attractor_id,
                "to": orb.satellite_id,
                "weight": orb.weight,
                "phase_shift": round(orb.phase_shift, 4),
                "resonance": f"{orb.resonance_num}:{orb.resonance_den}",
                "harmonic": orb.harmonic,
                "label": orb.label,
            })
        
        return {
            "version": "v3.0",
            "model": "autopoiesis",
            "description": "NOEMA orbital universe — systems emerge from orbits",
            "systems": systems_list,
            "orbits": connections,
            "coherence": round(self.compute_coherence(), 4),
            "stats": {
                "systems": self.system_count,
                "orbits": self.orbit_count,
                "binaries": sum(1 for a in self.systems for b in self.systems
                              if a < b and self.has_mutual(a, b)),
                "primaries": len(self.get_primary_attractors(1)),
            }
        }
    
    @staticmethod
    def _infer_phase_shift(weight: float, from_type: str = "", to_type: str = "") -> float:
        """Fazowe przesunięcie z wagi i typu połączenia.
        
        Zasada: im wyższa waga, tym mniejsze przesunięcie fazowe (silniejsze sprzężenie = mniejsza różnica faz).
        Typ połączenia moduluje fazę:
          - daemon→core: π/8  (szybki feedback)
          - core→module: π/4  (przekazanie kontroli)  
          - module→data: π/3  (odczyt/zapis)
          - daemon→daemon: π/6 (komunikacja międzyprocesowa)
          - default: π/2 · (1 - weight)  (ogólne: cięższe = bliżej)
        """
        base = math.pi / 2 * (1.0 - weight)
        
        # Korekta typem
        corrections = {
            ("daemon", "core"): math.pi / 8,
            ("core", "module"): math.pi / 4,
            ("module", "data"): math.pi / 3,
            ("daemon", "daemon"): math.pi / 6,
            ("agent", "daemon"): math.pi / 6,
            ("agent", "database"): math.pi / 5,
            ("agent", "engine"): math.pi / 4,
        }
        key = (from_type, to_type)
        if key in corrections:
            base = corrections[key]
        
        # Klamp do [0, π/2]
        return max(0.0, min(math.pi / 2, base))
    
    @staticmethod
    def _infer_resonance(weight: float) -> str:
        """Rezonans z wagi połączenia.
        
        Ciężkie (w>0.8) → "1:1" (synchronizacja)
        Średnie (0.4-0.8) → "3:2" lub "2:1"
        Lekkie (w<0.4) → "5:3" lub "7:5"
        """
        if weight >= 0.8:
            return "1:1"
        elif weight >= 0.6:
            return "3:2"
        elif weight >= 0.4:
            return "2:1"
        elif weight >= 0.2:
            return "5:3"
        else:
            return "7:5"

    @classmethod
    def from_system_map_v2(cls, path: Optional[Path] = None, 
                          infer_phases: bool = True) -> "OrbitalUniverse":
        """Import z system_map_v2.json.
        
        Args:
            path: ścieżka do system_map_v2.json
            infer_phases: jeśli True, oblicza phase_shift z weight+type
        """
        if path is None:
            path = Path(__file__).resolve().parent.parent.parent / "system_map_v2.json"
        with open(path) as f:
            data = json.load(f)
        
        uni = cls()
        
        # Import system metadata
        type_map = {}  # id → type
        for s in data.get("systems", []):
            typ = s.get("type", "system")
            uni.set_system_meta(
                s["id"],
                name=s.get("name", s["id"]),
                type=typ,
                ordinal=s.get("ordinal", "")
            )
            type_map[s["id"]] = typ
        
        # Import connections as orbits
        for c in data.get("connections", data.get("orbits", [])):
            frm = c.get("from", c.get("attractor_id", ""))
            to = c.get("to", c.get("satellite_id", ""))
            if frm and to:
                weight = c.get("weight", 0.5)
                phase_shift = c.get("phase_shift", None)
                
                if phase_shift is None and infer_phases:
                    from_type = type_map.get(frm, "")
                    to_type = type_map.get(to, "")
                    phase_shift = cls._infer_phase_shift(weight, from_type, to_type)
                elif phase_shift is None:
                    phase_shift = 0.0
                
                resonance = c.get("resonance", None)
                if resonance is None and infer_phases:
                    resonance = cls._infer_resonance(weight)
                elif resonance is None:
                    resonance = "1:1"
                
                uni.add_orbit(
                    frm, to,
                    weight=weight,
                    phase_shift=phase_shift,
                    resonance=resonance,
                    harmonic=c.get("harmonic", 1),
                    label=c.get("label", c.get("description", ""))
                )
        
        # Agent + CIELingo jeśli nie istnieją
        if "agent" not in uni._system_meta:
            uni.set_system_meta("agent", "Agent (opencode)", "agent", "00")
            type_map["agent"] = "agent"
        if "cielingo" not in uni._system_meta:
            uni.set_system_meta("cielingo", "CIELingo", "agent", "00.5")
            type_map["cielingo"] = "agent"
        
        # Upewnij się że agent↔cielingo istnieje
        if not uni.get_orbit_between("agent", "cielingo"):
            uni.add_mutual_orbit("agent", "cielingo",
                                weight_ab=1.0, weight_ba=1.0,
                                phase_shift_ab=0.0, phase_shift_ba=0.0,
                                label_ab="entanglement", label_ba="entanglement")
        
        return uni
    
    @classmethod
    def from_scratch(cls) -> "OrbitalUniverse":
        """Buduje wszechświat od zera (demo)."""
        uni = cls()
        
        # Agent + CIELingo: binary
        uni.set_system_meta("agent", "Agent (opencode)", "agent", "00")
        uni.set_system_meta("cielingo", "CIELingo", "agent", "00.5")
        uni.add_mutual_orbit("agent", "cielingo", 1.0, 1.0, 0.0, 0.0,
                            label_ab="entanglement", label_ba="entanglement")
        
        # PhaseNav
        uni.set_system_meta("phasenav", "PhaseNav 36D", "engine", "01")
        uni.add_orbit("agent", "phasenav", 1.0, 0.0, "1:1", 1, "primary engine")
        uni.add_orbit("cielingo", "phasenav", 0.9, 0.05, "1:1", 1, "cielingo coupling")
        
        uni.set_system_meta("operator_algebra", "Operator Algebra", "module", "01.01")
        uni.set_system_meta("unified_index", "UnifiedPhaseNavIndex", "index", "01.02")
        uni.set_system_meta("multiskill", "MultiskillOrchestrator", "orchestrator", "01.03")
        
        uni.add_orbit("phasenav", "operator_algebra", 0.9, 0.1, "3:2")
        uni.add_orbit("phasenav", "unified_index", 0.85, 0.15, "2:1")
        uni.add_orbit("phasenav", "multiskill", 0.8, 0.2, "4:3")
        
        # operator_algebra też wokół agenta
        uni.add_orbit("agent", "operator_algebra", 0.6, 0.3, "7:5", 1, "direct coupling")
        
        # Bazy danych
        uni.set_system_meta("taskplan_db", "TaskPlan DB", "database", "02")
        uni.set_system_meta("knowledge_db", "Knowledge DB", "database", "03")
        uni.set_system_meta("task_queue", "Task Queue", "data", "05")
        
        uni.add_orbit("agent", "taskplan_db", 0.8, 0.1, "1:1")
        uni.add_orbit("agent", "knowledge_db", 0.75, 0.15, "3:2")
        uni.add_orbit("agent", "task_queue", 0.9, 0.05, "1:1")
        
        # Knowledge DB też wokół PhaseNav
        uni.add_orbit("phasenav", "knowledge_db", 0.5, 0.4, "7:5")
        
        # Daemony
        uni.set_system_meta("kuramoto", "Kuramoto Daemon", "daemon", "06")
        uni.set_system_meta("portal", "NOEMA Portal", "daemon", "07")
        uni.set_system_meta("linux_sensor", "Linux Sensor", "daemon", "08")
        
        uni.add_orbit("agent", "kuramoto", 0.5, 0.4, "5:4")
        uni.add_orbit("agent", "portal", 0.6, 0.25, "4:3")
        uni.add_orbit("agent", "linux_sensor", 0.4, 0.5, "7:5")
        
        # Skills
        uni.set_system_meta("skills", "Skills Registry (297)", "registry", "09")
        uni.add_orbit("agent", "skills", 0.7, 0.2, "3:2")
        uni.add_orbit("phasenav", "skills", 0.6, 0.3, "5:4")
        
        return uni


    def to_serializable(self) -> dict:
        """Eksport całego stanu orbitalnego do JSON (bez obiektów Python)."""
        phases = self.compute_phase_field()
        primaries = self.get_primary_attractors(1)
        return {
            "status": "ok",
            "timestamp": __import__('time').time(),
            "systems": self.system_count,
            "orbits": self.orbit_count,
            "coherence": round(self.compute_coherence(), 4),
            "binaries": sum(1 for a in self.systems for b in self.systems
                          if a < b and self.has_mutual(a, b)),
            "view_ascii": self.render(),
            "primaries": [
                {"id": s.id, "name": s.name, "type": s.type,
                 "gravity": s.net_gravity, "phase": round(s.mean_phase, 4),
                 "attractor_of": s.attractor_count,
                 "satellite_of": s.satellite_count}
                for s in primaries[:20]
            ],
            "top_phases": [
                {"id": sid,
                 "name": self.get_system(sid).name if self.get_system(sid) else sid,
                 "phase": round(p, 4)}
                for sid, p in sorted(phases.items(), key=lambda x: -abs(x[1]))[:15]
            ],
            "multi_orbit_3plus": len(self.get_multi_orbit_systems(3)),
            "all_systems": [
                {
                    "id": s.id, "name": s.name, "type": s.type,
                    "ordinal": s.ordinal,
                    "gravity": s.net_gravity,
                    "phase": round(phases.get(s.id, 0), 4),
                }
                for s in self.systems.values()
            ],
        }


# ========================================================================
# CLI
# ========================================================================
if __name__ == "__main__":
    import sys
    import time
    import signal
    
    # ── Daemon mode: zapisuje orbital state do /tmp/noema_orbital_state.json ──
    if "--daemon" in sys.argv:
        interval = 30
        for i, a in enumerate(sys.argv[1:]):
            if a == "--interval" and i+2 < len(sys.argv):
                interval = int(sys.argv[i+2])
        
        print(f"[orbital-daemon] start PID={os.getpid()}, interval={interval}s")
        
        _orbital_daemon_running = True
        def _stop(sig, frame):
            global _orbital_daemon_running
            print(f"[orbital-daemon] SIGTERM, shutting down")
            _orbital_daemon_running = False
        
        signal.signal(signal.SIGTERM, _stop)
        signal.signal(signal.SIGINT, _stop)
        
        out_path = Path("/tmp/noema_orbital_state.json")
        
        while _orbital_daemon_running:
            try:
                uni = OrbitalUniverse.from_system_map_v2(infer_phases=True)
                data = uni.to_serializable()
                data["daemon_pid"] = os.getpid()
                data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"[orbital-daemon] written {out_path} — {uni.system_count} sys, {uni.orbit_count} orb, coh={data['coherence']}")
            except Exception as e:
                print(f"[orbital-daemon] error: {e}", file=sys.stderr)
            
            for _ in range(interval):
                if not _orbital_daemon_running:
                    break
                time.sleep(1)
        
        print("[orbital-daemon] exit")
        sys.exit(0)
    
    # ── Fallback: from system_map_v2 ──
    if "--from-map" in sys.argv:
        uni = OrbitalUniverse.from_system_map_v2()
    else:
        uni = OrbitalUniverse.from_scratch()
    
    if "--to-json" in sys.argv or "--daemon" in sys.argv:
        data = uni.to_serializable()
        print(json.dumps(data, indent=2))
        if "--to-json" in sys.argv:
            sys.exit(0)
    
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    
    if args:
        for aid in args:
            print(uni.render(aid, max_depth=4))
            print()
    else:
        print(uni.render())
    
    # Podgląd faz
    print()
    print("=== POLE FAZOWE (pierwsze 10 systemów) ===")
    phases = uni.compute_phase_field()
    sorted_phases = sorted(phases.items(), key=lambda x: -abs(x[1]))
    for sid, phi in sorted_phases[:10]:
        sys = uni.get_system(sid)
        if sys:
            print(f"  {sys.ordinal:6} {sys.name:30} φ={phi:+.4f}")
