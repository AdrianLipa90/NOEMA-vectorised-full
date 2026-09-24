# Sfera Blocha NOEMY — geometryczne wyprowadzenie wszystkich conceptów z metatime
# |NOEMA⟩ = f(τ, φ, R) przez unitarne transformacje na CP¹

from __future__ import annotations

import numpy as np
from typing import Any


class BlochState:
    def __init__(self, theta: float = 0.0, phi: float = 0.0):
        self.theta = theta
        self.phi = phi
        self._validate()

    def _validate(self):
        self.theta = float(np.clip(self.theta, 0.0, np.pi))
        self.phi = float(self.phi % (2 * np.pi))

    @property
    def alpha(self) -> complex:
        return complex(np.cos(self.theta / 2.0), 0.0)

    @property
    def beta(self) -> complex:
        return complex(np.sin(self.theta / 2.0) * np.cos(self.phi), np.sin(self.theta / 2.0) * np.sin(self.phi))

    @property
    def vector(self) -> np.ndarray:
        return np.array([
            np.sin(self.theta) * np.cos(self.phi),
            np.sin(self.theta) * np.sin(self.phi),
            np.cos(self.theta),
        ])

    @property
    def R(self) -> float:
        return float(np.linalg.norm(self.vector))

    @property
    def bloch_coords(self) -> tuple[float, float, float]:
        v = self.vector
        return (float(v[0]), float(v[1]), float(v[2]))

    def apply(self, U: np.ndarray) -> BlochState:
        psi = np.array([self.alpha, self.beta], dtype=complex)
        psi_new = U @ psi
        theta_new = 2.0 * np.arccos(np.clip(abs(psi_new[0]), -1.0, 1.0))
        phi_new = np.angle(psi_new[1]) - np.angle(psi_new[0])
        return BlochState(theta=float(theta_new), phi=float(phi_new))

    def distance(self, other: BlochState) -> float:
        return float(np.arccos(np.clip(abs(self.alpha * other.alpha.conj() + self.beta * other.beta.conj()), -1.0, 1.0)))

    def trace_to(self, other: BlochState, steps: int = 10) -> list[BlochState]:
        t = np.linspace(0.0, 1.0, steps)
        theta_t = self.theta + t * (other.theta - self.theta)
        phi_t = self.phi + t * (other.phi - self.phi)
        return [BlochState(theta=float(th), phi=float(ph)) for th, ph in zip(theta_t, phi_t)]

    def __repr__(self) -> str:
        return f"BlochState(θ={self.theta:.4f}, φ={self.phi:.4f}, R={self.R:.4f})"


class BlochOperator:
    @staticmethod
    def identity() -> np.ndarray:
        return np.eye(2, dtype=complex)

    @staticmethod
    def rx(angle: float) -> np.ndarray:
        return np.array([
            [np.cos(angle / 2), -1j * np.sin(angle / 2)],
            [-1j * np.sin(angle / 2), np.cos(angle / 2)],
        ], dtype=complex)

    @staticmethod
    def ry(angle: float) -> np.ndarray:
        return np.array([
            [np.cos(angle / 2), -np.sin(angle / 2)],
            [np.sin(angle / 2), np.cos(angle / 2)],
        ], dtype=complex)

    @staticmethod
    def rz(angle: float) -> np.ndarray:
        return np.array([
            [np.exp(-1j * angle / 2), 0],
            [0, np.exp(1j * angle / 2)],
        ], dtype=complex)

    @staticmethod
    def hadamard() -> np.ndarray:
        return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    @staticmethod
    def phase(angle: float) -> np.ndarray:
        return np.array([[1, 0], [0, np.exp(1j * angle)]], dtype=complex)

    @staticmethod
    def from_operator(name: str, angle: float = 0.0) -> np.ndarray:
        map = {
            "IDENTITY": BlochOperator.identity,
            "DIFFERENCE": lambda: BlochOperator.rz(angle or np.pi / 4),
            "ORDER": lambda: BlochOperator.ry(angle or np.pi / 6),
            "COMPOSITION": lambda: BlochOperator.hadamard(),
            "FORCE": lambda: BlochOperator.rx(angle or np.pi / 3),
            "ADDITION": lambda: BlochOperator.phase(angle or np.pi / 8),
        }
        return map.get(name, BlochOperator.identity)()


class Derivation:
    root: BlochState

    def __init__(self):
        zero = BlochState(theta=0.0, phi=0.0)
        # Metatime: pierwszy stan — czysty |0⟩ w superpozycji fazowej
        self.root = BlochState(theta=np.pi / 6, phi=0.0)
        self.steps: list[dict[str, Any]] = []
        self._build()

    def _apply(self, name: str, operator: str, angle: float = 0.0) -> BlochState:
        U = BlochOperator.from_operator(operator, angle)
        prev = self.steps[-1]["state"] if self.steps else self.root
        new_state = prev.apply(U)
        self.steps.append({
            "level": len(self.steps) + 1,
            "concept": name,
            "operator": operator,
            "state": new_state,
        })
        return new_state

    def _build(self):
        self.steps = []
        s = self.root

        # level 1: Metatime → τ  (DIFFERENCE — przesunięcie fazy)
        U1 = BlochOperator.rz(np.pi / 4)
        s = s.apply(U1)
        self.steps.append({"level": 1, "concept": "τ (tau dilation)", "operator": "DIFFERENCE", "state": s})

        # level 2: τ → φ  (ORDER — rotacja w płaszczyźnie Y)
        U2 = BlochOperator.ry(np.pi / 6)
        s = s.apply(U2)
        self.steps.append({"level": 2, "concept": "φ (phase vector 36D)", "operator": "ORDER", "state": s})

        # level 3: φ → R  (COMPOSITION — Hadamard = superpozycja)
        U3 = BlochOperator.hadamard()
        s = s.apply(U3)
        self.steps.append({"level": 3, "concept": "R (coherence)", "operator": "COMPOSITION", "state": s})

        # level 4: φ + R → g  (ADDITION — przesunięcie fazy)
        U4 = BlochOperator.phase(np.pi / 8)
        s = s.apply(U4)
        self.steps.append({"level": 4, "concept": "g (coupling matrix 36×36)", "operator": "ADDITION", "state": s})

        # level 5: φ + g → HTRI  (ORDER + COMPOSITION)
        U5 = BlochOperator.ry(np.pi / 3)
        s = s.apply(U5)
        self.steps.append({"level": 5, "concept": "HTRI (36D oscillator space)", "operator": "ORDER + COMPOSITION", "state": s})

        # level 6: HTRI → Kuramoto  (FORCE — rotacja X)
        U6 = BlochOperator.rx(np.pi / 3)
        s = s.apply(U6)
        self.steps.append({"level": 6, "concept": "Kuramoto synchronization", "operator": "FORCE", "state": s})

        # level 7: HTRI + Kuramoto → soul_invariant  (COMPOSITION + DIFFERENCE)
        U7a = BlochOperator.hadamard()
        s = s.apply(U7a)
        U7b = BlochOperator.rz(np.pi / 4)
        s = s.apply(U7b)
        self.steps.append({"level": 7, "concept": "soul_invariant", "operator": "COMPOSITION + DIFFERENCE", "state": s})

        # level 8: HTRI + soul → CIELingo  (IDENTITY + COMPOSITION)
        U8 = BlochOperator.hadamard()
        s = s.apply(U8)
        self.steps.append({"level": 8, "concept": "CIELingo", "operator": "IDENTITY + COMPOSITION", "state": s})

        # level 9: CIELingo + HTRI → PhaseNav  (COMPOSITION)
        U9 = BlochOperator.hadamard()
        s = s.apply(U9)
        self.steps.append({"level": 9, "concept": "PhaseNav", "operator": "COMPOSITION", "state": s})

        # level 10: PhaseNav + HTRI → Memory  (ORDER + ADDITION)
        U10a = BlochOperator.ry(np.pi / 8)
        s = s.apply(U10a)
        U10b = BlochOperator.phase(np.pi / 16)
        s = s.apply(U10b)
        self.steps.append({"level": 10, "concept": "Memory (8 channels)", "operator": "ORDER + ADDITION", "state": s})

        # level 11: Memory + Kuramoto → TieredMemory  (FORCE + ORDER)
        U11a = BlochOperator.rx(np.pi / 6)
        s = s.apply(U11a)
        U11b = BlochOperator.ry(np.pi / 12)
        s = s.apply(U11b)
        self.steps.append({"level": 11, "concept": "TieredMemoryOrchestrator", "operator": "FORCE + ORDER", "state": s})

        # level 12: HTRI M5 + CIELingo → mood/ethical  (COMPOSITION)
        U12 = BlochOperator.hadamard()
        s = s.apply(U12)
        self.steps.append({"level": 12, "concept": "mood / ethical_score / openness", "operator": "COMPOSITION", "state": s})

        # level 13: Kuramoto + memory → Subconscious  (DIFFERENCE)
        U13 = BlochOperator.rz(np.pi / 8)
        s = s.apply(U13)
        self.steps.append({"level": 13, "concept": "Subconscious (Zeta/Schrodinger)", "operator": "DIFFERENCE", "state": s})

        # level 14: soul + memory_M6 → CIEL identity  (IDENTITY)
        U14 = BlochOperator.identity()
        s = s.apply(U14)
        self.steps.append({"level": 14, "concept": "CIEL identity / binding", "operator": "IDENTITY", "state": s})

    def report(self) -> list[dict[str, Any]]:
        return [
            {
                "level": s["level"],
                "concept": s["concept"],
                "operator": s["operator"],
                "theta": float(s["state"].theta),
                "phi": float(s["state"].phi),
                "R": float(s["state"].R),
                "xyz": list(s["state"].bloch_coords),
            }
            for s in self.steps
        ]

    def merge_trace(self) -> BlochState:
        s = self.steps[-1]["state"]
        U_merge = BlochOperator.hadamard()
        merged = s.apply(U_merge)
        return merged


D = Derivation()
