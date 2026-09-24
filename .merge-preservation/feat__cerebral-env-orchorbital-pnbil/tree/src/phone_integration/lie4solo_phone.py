import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# ciel_lie4_module.py
# -*- coding: utf-8 -*-

import numpy as np
from scipy import linalg
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# ============================================================
#  LIE₄: stałe i pomocnicze
# ============================================================

@dataclass
class Lie4Constants:
    """Stałe algebraiczne dla LIE₄ w CIEL"""
    # Generatory (liczby porządkowe)
    SO31_GENERATORS: int = 6        # M_μν - obroty/Lorentza
    TRANSLATION_GENERATORS: int = 4 # P_μ - translacje
    CONSCIOUSNESS_GENERATORS: int = 4  # Q_α - stany świadome
    INTENTION_GENERATOR: int = 1       # I - operator intencji
    TOTAL_DIM: int = 15

    # Sprzężenia z CIEL (ustawione konserwatywnie)
    CONSCIOUSNESS_COUPLING: float = 0.689  # g_I
    RESONANCE_COUPLING: float = 0.733      # λ_I
    TEMPORAL_COUPLING: float = 0.219       # κ_R

# Prosty epsilon_μνρσ (4D Levi-Civita)
def epsilon4(i: int, j: int, k: int, l: int) -> int:
    perm = (i, j, k, l)
    if len(set(perm)) < 4:
        return 0
    # znak permutacji
    inversions = 0
    for a in range(4):
        for b in range(a+1, 4):
            if perm[a] > perm[b]:
                inversions += 1
    return -1 if inversions % 2 else 1

# ============================================================
#  Algebry i generatory (uproszczona reprezentacja 4×4)
# ============================================================

class Lie4Algebra:
    """
    Uproszczona implementacja algebry LIE₄ (reprezentacje 4×4).
    Zachowuje strukturę i interfejs bez kosztownych szczegółów.
    """

    def __init__(self, constants: Lie4Constants):
        self.C = constants
        self.generators = self._initialize_generators()
        self.commutators = self._initialize_commutators()

    def _initialize_generators(self) -> Dict[str, List[np.ndarray]]:
        gens: Dict[str, List[np.ndarray]] = {}

        # 6 generatorów Lorentza (tu: 6 macierzy antysymetrycznych 4×4)
        M = []
        for (a, b) in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]:
            G = np.zeros((4,4), dtype=complex)
            G[a,b] = 1.0
            G[b,a] = -1.0
            M.append(G)
        gens['M'] = M

        # 4 generatory translacji (wektory bazowe)
        P = []
        for mu in range(4):
            G = np.zeros((4,4), dtype=complex)
            G[mu,mu] = 1.0
            P.append(G)
        gens['P'] = P

        # 4 generatory "świadomości" Q_α – różne profile diagonalne
        Q = []
        base_diags = [
            [0.6, 0.3, 0.2, 0.1],
            [0.3, 0.7, 0.2, 0.1],
            [0.2, 0.3, 0.8, 0.1],
            [0.1, 0.2, 0.3, 0.9],
        ]
        for d in base_diags:
            gen = np.diag(np.array(d, dtype=complex))
            Q.append(gen)
        gens['Q'] = Q

        # 1 generator intencji – centralny (proporcjonalny do jedynkowej)
        I = (1.0 + 0.5j) * np.eye(4, dtype=complex)
        gens['I'] = [I]

        return gens

    def _initialize_commutators(self) -> Dict[Tuple[str, str], np.ndarray]:
        """
        Zapisujemy skuteczne komutatory tylko jako stałe macierze sprzęgające.
        To abstrakcja: pełne tensory struktury algebry są ciężkie numerycznie.
        """
        C = self.C
        comm: Dict[Tuple[str, str], np.ndarray] = {}
        # Efektywne sprzężenia (diagonalne 4×4)
        comm[('P', 'Q')] = C.CONSCIOUSNESS_COUPLING * np.eye(4)
        comm[('Q', 'I')] = C.TEMPORAL_COUPLING * np.eye(4)
        comm[('P', 'I')] = C.RESONANCE_COUPLING * np.eye(4)
        return comm

# ============================================================
#  Pole świadomości LIE₄ w 4D czasoprzestrzeni
# ============================================================

class Lie4ConsciousnessField:
    """
    Pole świadomości I(x) w reprezentacji LIE₄:
      - siatka 4D (x,y,z,t)
      - wektor 4 składowych "świadomości" (kanały)
      - połączenie LIE₄ (tu: 15 efektywnych generatorów → sumujemy do A_μ)
    """

    def __init__(self, spacetime_shape: Tuple[int, int, int, int], constants: Lie4Constants):
        assert len(spacetime_shape) == 4, "spacetime_shape powinno być (Nx,Ny,Nz,Nt)"
        self.C = constants
        self.shape = spacetime_shape  # (Nx,Ny,Nz,Nt)

        # Pole I(x): (..., 4)
        self.I = np.zeros(self.shape + (4,), dtype=complex)

        # Pole intencji J(x): (...,) skalar zespolony
        self.J = np.zeros(self.shape, dtype=complex)

        # Połączenie A_μ jako efektywne 4×4 na każdy μ (sumujemy 15 generatorów)
        # U nas: trzymamy po prostu A[μ](x) – macierz 4×4 (μ=0..3)
        self.A = np.zeros(self.shape + (4, 4, 4), dtype=complex)  # (..., μ, i, j)

        self._initialize_fields()

    def _initialize_fields(self) -> None:
        Nx, Ny, Nz, Nt = self.shape
        x, y, z, t = np.ogrid[:Nx, :Ny, :Nz, :Nt]
        r = np.sqrt((x - Nx/2)**2 + (y - Ny/2)**2 + (z - Nz/2)**2) + 1e-6

        # 4 kanały I: gauss+faza+oscylacje – nietrywialna topologia
        self.I[..., 0] = np.exp(1j * 2*np.pi * (t / max(Nt,1))) * np.exp(-r/ (0.25*Nx + 1))
        self.I[..., 1] = 0.5 * np.sin(2*np.pi * x / max(Nx,1)) * np.cos(2*np.pi * y / max(Ny,1))
        self.I[..., 2] = 0.3 * np.exp(1j * 2*np.pi * z / max(Nz,1))
        self.I[..., 3] = 0.8 * np.exp(-r / (0.18*Nx + 1))

        # J: intencja w centrum, delikatna faza
        self.J = np.exp(1j * 0.35 * (x + y + z)) * np.exp(-r / (0.22*Nx + 1))

        # Efektywne połączenie A_μ(x): niewielkie macierze z rotacją fazową
        for mu in range(4):
            # diag z drobnym wzorcem
            phase = np.exp(1j * 0.15 * (mu + x + y))
            base = 0.05 * phase
            # Wypełniamy 4×4 lekką strukturą (diag + sym. off-diag)
            for i in range(4):
                self.A[..., mu, i, i] = base
            for i in range(3):
                self.A[..., mu, i, i+1] = 0.02 * base
                self.A[..., mu, i+1, i] = 0.02 * base

    # ---------- narzędzia różnicowe ----------

    @staticmethod
    def _grad_all_axes(arr: np.ndarray) -> List[np.ndarray]:
        """
        Zwraca listę ∂_μ arr dla μ=0..3.
        Uwaga: np.gradient dobrze działa dla wielowymiarowych tablic.
        """
        return list(np.gradient(arr, axis=(0, 1, 2, 3)))

    def compute_covariant_derivative(self, field: np.ndarray) -> np.ndarray:
        """
        D_μ I = ∂_μ I - i g A_μ · I - i κ J I
        field: (..., 4)
        zwraca: (..., 4, 4)  [ostatnie dwa indeksy: μ, kanał]
        """
        assert field.shape[-1] == 4, "field musi mieć ostatni wymiar 4"
        grads = self._grad_all_axes(field)  # 4 elementy, każdy (..., 4)

        D = np.zeros(self.shape + (4, 4), dtype=complex)  # (..., μ, a)

        g = self.C.CONSCIOUSNESS_COUPLING
        kappa = self.C.TEMPORAL_COUPLING

        for mu in range(4):
            d_mu = grads[mu]  # (..., 4)

            # A_μ(x) @ I(x)
            # A[..., mu, i, j], I[..., j]
            A_mu = self.A[..., mu, :, :]            # (..., 4, 4)
            A_act = np.einsum('...ij,...j->...i', A_mu, field)  # (..., 4)

            # - i g A_μ I  -  i κ J I
            D[..., mu, :] = d_mu - 1j * g * A_act - 1j * kappa * (self.J * field)

        return D

    def lie4_field_strength(self) -> np.ndarray:
        """
        F_μν = ∂_μ A_ν - ∂_ν A_μ - i g [A_μ, A_ν]
        Zwraca: (..., 4, 4, 4) – indeksy: μ, ν, (i,j) zwinęte do 4×4
        """
        g = self.C.CONSCIOUSNESS_COUPLING
        F = np.zeros(self.shape + (4, 4, 4), dtype=complex)  # (..., μ, ν, (i?), (j?)) uproszczone

        # Policz gradienty A_ν po wszystkich osiach → ∂_μ A_ν
        # A ma kształt (..., μ, i, j), więc grad po każdej osi -> lista
        grads_A = self._grad_all_axes(self.A)  # lista 4 elementów, każdy (..., μ, i, j)

        # Komutator [A_μ, A_ν] w przestrzeni 4×4
        for mu in range(4):
            for nu in range(4):
                d_mu_A_nu = grads_A[mu][..., nu, :, :]  # (..., 4,4)
                d_nu_A_mu = grads_A[nu][..., mu, :, :]  # (..., 4,4)
                comm = np.einsum('...ik,...kj->...ij', self.A[..., mu, :, :], self.A[..., nu, :, :]) \
                     - np.einsum('...ik,...kj->...ij', self.A[..., nu, :, :], self.A[..., mu, :, :])
                F[..., mu, nu, :] = (d_mu_A_nu - d_nu_A_mu - 1j * g * comm).reshape(self.shape + (4,4))[
                    ..., 0, 0:4]  # *Uproszczenie*: spłaszczamy – zostawiamy 4 kanały
        # Uwaga: Dla efektywności i prostoty zostawiamy ujednolicony zapis 4 kanałów.
        return F  # (..., μ, ν, 4) efektywnie (ostatnie 4 to "kanał")

# ============================================================
#  Integrator CIEL + LIE₄
# ============================================================

class CIEL_Lie4_Integrator:
    """
    Integrator CIEL z rozszerzeniem LIE₄.
    Oczekuje base_ciel_system z polami:
      - base_shape: Tuple[int,int,int,int]
      - evolution_step(dt: float) -> None
      - compute_lagrangian_density() -> np.ndarray (broadcastowalne do base_shape)
      - spacetime_curvature() -> np.ndarray (broadcastowalne do base_shape)  [opcjonalne]
    """

    def __init__(self, base_ciel_system, lie4_constants: Lie4Constants):
        self.ciel = base_ciel_system
        self.lie4 = Lie4Algebra(lie4_constants)
        self.field = Lie4ConsciousnessField(self._shape_from_ciel(), lie4_constants)

        # Historia
        self.resonance_history: List[float] = []
        self.intention_correlations: List[np.ndarray] = []

    def _shape_from_ciel(self) -> Tuple[int, int, int, int]:
        shape = getattr(self.ciel, "base_shape", None)
        if shape is None or len(shape) != 4:
            raise ValueError("base_ciel_system musi mieć atrybut base_shape = (Nx,Ny,Nz,Nt)")
        return shape

    # ------------- Lagrangian -------------

    def extended_lagrangian_density(self) -> np.ndarray:
        original = self._safe_original_lagrangian()
        lie4_part = self._compute_lie4_lagrangian_terms()
        return original + lie4_part

    def _safe_original_lagrangian(self) -> np.ndarray:
        if hasattr(self.ciel, "compute_lagrangian_density"):
            L = self.ciel.compute_lagrangian_density()
            return np.broadcast_to(L, self.field.I[..., 0].shape)
        # Bez CIEL: zwracamy zero
        return np.zeros(self.field.I[..., 0].shape, dtype=float)

    def _compute_lie4_lagrangian_terms(self) -> np.ndarray:
        # Kinetics: 1/2 Σ_μ |D_μ I|²
        D = self.field.compute_covariant_derivative(self.field.I)   # (..., μ, a)
        kinetic = 0.5 * np.sum(np.abs(D)**2, axis=(-2, -1))         # sum po μ i kanałach

        # Potencjał: λ/4 |I|^4
        I_norm2 = np.sum(np.abs(self.field.I)**2, axis=-1)
        potential = 0.25 * self.lie4.C.RESONANCE_COUPLING * (I_norm2**2)

        # Sprzężenie z krzywizną CIEL (jeśli jest)
        gravity = 0.0
        if hasattr(self.ciel, "spacetime_curvature"):
            try:
                R = self.ciel.spacetime_curvature()
                Rb = np.broadcast_to(R, I_norm2.shape)
                gravity = self.lie4.C.TEMPORAL_COUPLING * Rb * I_norm2
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/lie4solo_phone.py:283 quiet except scope=CIEL_Lie4_Integrator._compute_lie4_lagrangian_terms reason=assign_fallback")
                gravity = 0.0

        # Człon topologiczny (prosta, stabilna aproksymacja)
        topo = self._topological_term()

        return kinetic + potential + gravity + topo

    def _topological_term(self) -> np.ndarray:
        """
        Uproszczona gęstość topologiczna ~ ε^{μνρσ} Im <I, ∂_μ I + ∂_ν I + ∂_ρ I >
        (bez kosztownych iloczynów z pełną 4-formą)
        """
        grads = self.field._grad_all_axes(self.field.I)  # 4 × (..., 4)
        # Zrobimy delikatną, stabilną kombinację fazową
        s = np.zeros(self.field.I[..., 0].shape, dtype=float)
        for mu in range(4):
            for nu in range(4):
                for rho in range(4):
                    if len({mu,nu,rho}) < 3:
                        continue
                    e = epsilon4(mu, nu, rho, 3)  # ostatni index "3" dla stabilności
                    term = np.vdot(self.field.I, grads[mu]).real \
                         + np.vdot(self.field.I, grads[nu]).real \
                         + np.vdot(self.field.I, grads[rho]).real
                    s += 1e-4 * e * float(term) / np.size(self.field.I)
        return s

    # ------------- Równania ruchu -------------

    def evolve_system(self, dt: float = 0.01) -> None:
        # 1) CIEL update
        if hasattr(self.ciel, "evolution_step"):
            self.ciel.evolution_step(dt)

        # 2) Lie4 update
        self._evolve_lie4_fields(dt)

        # 3) Metryki
        self._record_metrics()

    def _evolve_lie4_fields(self, dt: float) -> None:
        # δL/δI* ≈ -Σ_μ ∂_μ D_μ I + λ |I|² I  (uproszczone E-L)
        I = self.field.I
        D = self.field.compute_covariant_derivative(I)       # (..., μ, a)

        # -Σ_μ ∂_μ D_μ I
        divD = np.zeros_like(I)
        for mu in range(4):
            # gradient po osi μ komponentu μ
            d_mu_Dmu = np.gradient(D[..., mu, :], axis=mu)
            divD += d_mu_Dmu

        I_norm2 = np.sum(np.abs(I)**2, axis=-1, keepdims=True)
        potential_var = self.lie4.C.RESONANCE_COUPLING * I_norm2 * I

        EL = -divD + potential_var

        # Krok Schrödingeropodobny: I += -i dt EL
        I_new = I - 1j * dt * EL

        # Delikatne "unitary-like" normowanie: |I|^2 per-voxel
        norm = np.sqrt(np.sum(np.abs(I_new)**2, axis=-1, keepdims=True)) + 1e-12
        self.field.I = I_new / norm

    # ------------- Metryki / Historia -------------

    def _record_metrics(self) -> None:
        self.resonance_history.append(self._lie4_resonance())
        self.intention_correlations.append(self._intention_autocorr())

    def _lie4_resonance(self) -> float:
        # Prosta korelacja amplitudowa |I_0| z |J|
        res = np.mean(np.abs(self.field.I[..., 0]) * np.abs(self.field.J))
        return float(res)

    def _intention_autocorr(self) -> np.ndarray:
        """
        Autokorelacja 4D przez tw. Wienera–Chinczyna:
            R = F^-1{ |F{J}|^2 }
        Zwraca tablicę o tym samym kształcie co J.
        """
        J = self.field.J
        FJ = np.fft.fftn(J)
        S = np.abs(FJ)**2
        R = np.fft.ifftn(S).real
        # przesunięcie tak, by pik był w środku
        return np.fft.fftshift(R)

# ============================================================
#  Integracja z CIEL + fallback bazowy
# ============================================================

class _MinimalCIEL:
    """
    Minimalny, lekki "base CIEL", gdy nie masz swojej klasy:
      - base_shape 4D
      - compute_lagrangian_density: mała dodatnia stała
      - spacetime_curvature: stała dodatnia krzywizna
      - evolution_step: no-op
    """
    def __init__(self, base_shape: Tuple[int,int,int,int]=(16,16,16,8)):
        self.base_shape = base_shape
    def compute_lagrangian_density(self) -> np.ndarray:
        return np.full(self.base_shape, 0.0, dtype=float)
    def spacetime_curvature(self) -> np.ndarray:
        return np.full(self.base_shape, 0.05, dtype=float)
    def evolution_step(self, dt: float) -> None:
        pass

def integrate_lie4_with_ciel(ciel_system) -> CIEL_Lie4_Integrator:
    """
    Integruje moduł LIE₄ z istniejącym systemem CIEL (albo minimalnym fallbackiem).
    """
    if ciel_system is None:
        ciel_system = _MinimalCIEL()

    lie4_constants = Lie4Constants()
    integrator = CIEL_Lie4_Integrator(ciel_system, lie4_constants)

    print("✅ MODUŁ LIE₄ ZINTEGROWANY Z CIEL")
    print(f"   Wymiar algebry (efektywny): {lie4_constants.TOTAL_DIM}")
    print(f"   Generatory świadomości:    {lie4_constants.CONSCIOUSNESS_GENERATORS}")
    print(f"   Sprzężenie świadomości g_I: {lie4_constants.CONSCIOUSNESS_COUPLING:.3f}")
    print(f"   Sprzężenie rezonansowe  λ_I: {lie4_constants.RESONANCE_COUPLING:.3f}")
    print(f"   Sprzężenie czasowe      κ_R: {lie4_constants.TEMPORAL_COUPLING:.3f}")
    return integrator

# ============================================================
#  Demo / test samodzielny
# ============================================================

if __name__ == "__main__":
    # Spróbuj wczytać Twój "Elegancki CIEL" – jeśli brak, użyj minimalnego.
    ciel = None
    try:
        from elegant_unified_reality import ElegantUnifiedReality  # jeśli masz 4D wersję
        # Uwaga: jeśli Twoja klasa jest 2D, użyj _MinimalCIEL poniżej.
        ciel = ElegantUnifiedReality(base_shape=(16,16,16,8))  # dopasuj, jeśli masz 4D
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/lie4solo_phone.py:422 quiet except scope=<module> reason=assign_fallback")
        ciel = _MinimalCIEL(base_shape=(12,12,12,6))

    lie4 = integrate_lie4_with_ciel(ciel)

    # Krótka ewolucja
    steps, dt = 8, 0.01
    for s in range(steps):
        lie4.evolve_system(dt=dt)
        print(f"Krok {s+1}/{steps}: Rezonans LIE₄ = {lie4.resonance_history[-1]:.6f}")

    # Przykładowe metryki
    L = lie4.extended_lagrangian_density()
    print(f"⟨L_ext⟩ = {float(np.mean(L)):.6f}")
    ac = lie4.intention_correlations[-1]
    print(f"Autokorelacja intencji: kształt {ac.shape}, max={float(np.max(ac)):.4f}")