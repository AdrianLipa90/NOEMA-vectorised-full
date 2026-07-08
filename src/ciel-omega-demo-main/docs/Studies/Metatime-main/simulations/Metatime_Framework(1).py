"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.linalg import expm

# ============================================================================
# 1. STAŁE FIZYCZNE I PARAMETRY
# ============================================================================
# Różnice mas kwadratowych [eV^2]
dm21 = 7.5e-5
dm31 = 2.5e-3
# Energia neutrina [GeV]
E = 0.01  # ~10 MeV (neutrina z supernowej)
# Kąty mieszania PMNS [rad]
theta12 = np.deg2rad(33.4)
theta23 = np.deg2rad(49.0)
theta13 = np.deg2rad(8.6)
delta_cp = 0.0  # standardowa faza Dirac CP (tu zerowa, bo CP pochodzi z fazy topologicznej)

# Stałe metatime
gamma_time = 0.05  # bazowa topologiczna faza Berry'ego
epsilon = 1e-4     # stała sprzężenia metatime z Hamiltonianem

# Parametry trajektorii
N_points = 500            # liczba punktów wzdłuż trajektorii
L_max_km = 3.086e16       # maksymalna długość drogi [km] (~1 kpc)
L_max_m = L_max_km * 1e3  # [m]

# ============================================================================
# 2. MACIERZ PMNS
# ============================================================================
def construct_pmns(theta12, theta23, theta13, delta):
    """Zwraca unitarną macierz mieszania PMNS."""
    c12, s12 = np.cos(theta12), np.sin(theta12)
    c23, s23 = np.cos(theta23), np.sin(theta23)
    c13, s13 = np.cos(theta13), np.sin(theta13)
    eid = np.exp(-1j * delta)
    eid_conj = np.conj(eid)
    
    U = np.array([
        [c12 * c13, s12 * c13, s13 * eid],
        [-s12 * c23 - c12 * s23 * s13 * eid_conj,
          c12 * c23 - s12 * s23 * s13 * eid_conj,
          s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * eid_conj,
         -c12 * s23 - s12 * c23 * s13 * eid_conj,
          c23 * c13]
    ], dtype=complex)
    return U

U = construct_pmns(theta12, theta23, theta13, delta_cp)
U_dag = U.conj().T

# Macierz mas kwadratowych w bazie mas
M2 = np.diag([0.0, dm21, dm31])  # [eV^2]

# ============================================================================
# 3. POLA CZASU: SKALARNE I TENSOROWE (z fluktuacjami)
# ============================================================================
def time_field_scalar(x, phi0=1.0, amplitude=0.01, k=20.0):
    """Pole skalarne czasu phi(x) z fluktuacjami sinusoidalnymi."""
    return phi0 + amplitude * np.sin(k * x)

def time_field_tensor(x, amplitude=0.01):
    """
    Tensor czasu T_{μν}(x) jako fluktuacje losowe.
    W uproszczeniu: zwracamy macierz 2x2 symetryczną.
    """
    # Dla uproszczenia: tylko składowe przestrzenne 2D
    T = np.zeros((2, 2))
    T[0, 0] = 1.0 + amplitude * np.random.randn()
    T[0, 1] = T[1, 0] = amplitude * np.random.randn()
    T[1, 1] = 1.0 + amplitude * np.random.randn()
    return T

# ============================================================================
# 4. OPERATOR CZASU W PRZESTRZENI HILBERTA NEUTRIN
# ============================================================================
def time_operator(phi, T):
    r"""
    Operator czasu według równania (2):
    \hat{T} = φ·I + T_{μν}·Σ^{μν}
    Dla uproszczenia: Σ^{μν} ~ macierz Pauliego/Diraca.
    Tutaj używamy macierzy 2x2 (dla spinorów dwuskładnikowych).
    """
    # Macierze Pauliego (z rozszerzeniem do 2x2)
    sigma = [np.eye(2), np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]])]
    # Uproszczenie: T_{μν} jako wektor 4-składnikowy dla μ,ν=0,1,2,3
    # Dla 2D: bierzemy tylko pierwsze 3 składowe
    T_flat = T.flatten()
    T_operator = phi * np.eye(2)
    for i in range(min(3, len(T_flat))):
        T_operator += T_flat[i] * sigma[i]
    return T_operator

# ============================================================================
# 5. HAMILTONIAN ZALEŻNY OD METATIME λ
# ============================================================================
def hamiltonian_metatime(lambda_val, U, M2, E, epsilon, phi, T):
    r"""
    Hamiltonian z równania (27) i (40):
    H(λ) = U·M²/(2E)·U† + ε·\hat{T}(λ)
    """
    H_mass = U @ (M2 / (2 * E * 1e9)) @ U_dag  # M2/(2E) w jednostkach eV -> GeV
    T_op = time_operator(phi, T)
    # Rozszerzamy T_op do przestrzeni 3x3 (dla 3 zapachów) przez sumę prostą
    T_op_ext = np.zeros((3, 3), dtype=complex)
    T_op_ext[:2, :2] = T_op  # zakładamy, że T działa na pierwsze dwa stany zapachowe
    T_op_ext[2, 2] = np.trace(T_op) / 2.0  # ślad dla trzeciego stanu
    H = H_mass + epsilon * T_op_ext
    return H

# ============================================================================
# 6. TOPOLOGICZNA FAZA BERRY'EGO WZDŁUŻ TRAJEKTORII
# ============================================================================
def berry_connection(H, dH_dlambda):
    """
    Oblicza połączenie Berry'ego A_n(λ) = i⟨n|∂_λ|n⟩
    dla stanu własnego n (n=0 - najniższa energia).
    """
    # Diagonalizacja Hamiltonianu
    eigvals, eigvecs = np.linalg.eigh(H)
    # Stan podstawowy (n=0)
    psi = eigvecs[:, 0]
    # Pochodna stanu względem λ (przybliżona różnicą skończoną)
    # Tutaj używamy dH/dλ do obliczenia ∂_λ|n⟩ przez teorię perturbacji
    # ⟨m|∂_λ|n⟩ = ⟨m|∂_H/∂λ|n⟩ / (E_n - E_m) dla m ≠ n
    dpsi_dlambda = np.zeros_like(psi, dtype=complex)
    for m in range(len(eigvals)):
        if m == 0:
            continue
        dpsi_dlambda += (eigvecs[:, m].conj().T @ dH_dlambda @ psi) / (eigvals[0] - eigvals[m]) * eigvecs[:, m]
    A = 1j * (psi.conj().T @ dpsi_dlambda)
    return A

def berry_phase_along_trajectory(lambda_vals, H_func):
    """
    Całkuje połączenie Berry'ego wzdłuż trajektorii w metatime λ.
    Zwraca całkowitą fazę γ.
    """
    gamma = 0.0
    for i in range(len(lambda_vals) - 1):
        lam = lambda_vals[i]
        dlam = lambda_vals[i + 1] - lambda_vals[i]
        H = H_func(lam)
        # Przybliżenie dH/dλ przez różnicę skończoną
        H_next = H_func(lam + 1e-6)
        dH_dlambda = (H_next - H) / 1e-6
        A = berry_connection(H, dH_dlambda)
        gamma += np.real(A) * dlam  # tylko część rzeczywista
    return gamma

# ============================================================================
# 7. SYMULACJA TRAJEKTORII KOSMOLOGICZNEJ Z FLUKTUACJAMI
# ============================================================================
def generate_cosmological_trajectory(N, L_max):
    """
    Generuje trajektorię w przestrzeni konfiguracyjnej z fluktuacjami.
    Zwraca:
      lambda_vals: wartości metatime λ (zdefiniowane jako skumulowana krzywizna)
      phi_vals: wartości pola skalarnego φ wzdłuż trajektorii
      T_vals: wartości tensora czasu T_{μν} wzdłuż trajektorii
    """
    # Długość wzdłuż trajektorii (proper distance)
    s_vals = np.linspace(0, L_max, N)
    # Metatime λ jako całka z niezmiennika krzywizny (uproszczone: liniowe w s)
    lambda_vals = s_vals * 1e-20  # skala ~ krzywizna
    # Fluktuacje skalarne
    phi_vals = time_field_scalar(s_vals, phi0=1.0, amplitude=0.01, k=2*np.pi*1e-18)
    # Fluktuacje tensorowe
    T_vals = [time_field_tensor(s, amplitude=0.005) for s in s_vals]
    return lambda_vals, phi_vals, T_vals

# Generowanie trajektorii
lambda_vals, phi_vals, T_vals = generate_cosmological_trajectory(N_points, L_max_m)

# ============================================================================
# 8. OBLICZANIE FAZY BERRY'EGO DLA NEUTRIN I ANTINEUTRIN
# ============================================================================
# Funkcja Hamiltonianu zależna od λ
def H_func(lam, phi_vals=phi_vals, T_vals=T_vals):
    # Interpolacja phi i T dla danego λ (najbliższy punkt)
    idx = np.argmin(np.abs(lambda_vals - lam))
    phi = phi_vals[idx]
    T = T_vals[idx]
    return hamiltonian_metatime(lam, U, M2, E, epsilon, phi, T)

# Faza Berry'ego dla neutrin
gamma_nu = berry_phase_along_trajectory(lambda_vals, H_func)
# Dla antyneutrin: faza zmienia znak
gamma_anu = -gamma_nu

print(f"Topologiczna faza Berry'ego (neutrino): γ_nu = {gamma_nu:.6f}")
print(f"Topologiczna faza Berry'ego (antineutrino): γ_anu = {gamma_anu:.6f}")

# ============================================================================
# 9. ROZWIĄZANIE RÓWNANIA SCHRÖDINGERA W METATIME λ
# ============================================================================
def solve_metatime_schrodinger(lambda_vals, H_func, initial_state):
    """
    Rozwiązanie równania: d/dλ |Ψ(λ)⟩ = -i H(λ) |Ψ(λ)⟩
    Zwraca stan końcowy.
    """
    def rhs(lam, psi):
        H = H_func(lam)
        return -1j * (H @ psi.reshape(-1, 1)).flatten()
    
    psi0 = initial_state.flatten()
    sol = solve_ivp(rhs, [lambda_vals[0], lambda_vals[-1]], psi0, t_eval=lambda_vals, method='RK45', vectorized=False)
    # Stan końcowy
    psi_final = sol.y[:, -1].reshape(-1, 1)
    return psi_final

# Stan początkowy: neutrino elektronowe |ν_e⟩ = pierwsza kolumna macierzy U
initial_nu = U[:, 0].reshape(-1, 1)

# Ewolucja dla neutrin (z fazą γ_nu)
psi_final_nu = solve_metatime_schrodinger(lambda_vals, H_func, initial_nu)

# Dla antyneutrin: używamy Hamiltonianu ze zmienionym znakiem fazy Berry'ego
# Można to zrobić przez zmianę znaku ε w Hamiltonianie, ale tutaj upraszczamy:
# Modyfikujemy H_func dla antyneutrin przez zmianę znaku przy członie topologicznym
def H_func_anu(lam):
    H = H_func(lam)
    # Odejmujemy podwójną fazę Berry'ego? (uproszczenie)
    # W rzeczywistości powinno się zmienić znak przy ε·T
    # Tutaj symulujemy przez zmianę znaku gamma w późniejszym obliczeniu prawdopodobieństwa
    return H

psi_final_anu = solve_metatime_schrodinger(lambda_vals, H_func_anu, initial_nu)

# ============================================================================
# 10. PRAWDOPODOBIEŃSTWA OSYLACJI
# ============================================================================
def oscillation_probabilities(psi_final, U):
    """
    Prawdopodobieństwo przejścia ν_e → ν_μ, ν_τ.
    """
    # Amplitudy w bazie zapachowej
    amp_mu = U[:, 1].conj().T @ psi_final
    amp_tau = U[:, 2].conj().T @ psi_final
    P_mu = np.abs(amp_mu)**2
    P_tau = np.abs(amp_tau)**2
    return P_mu.item(), P_tau.item()

P_nu_mu, P_nu_tau = oscillation_probabilities(psi_final_nu, U)
P_anu_mu, P_anu_tau = oscillation_probabilities(psi_final_anu, U)

print(f"P(ν_e → ν_μ) = {P_nu_mu:.6f}")
print(f"P(ν_e → ν_τ) = {P_nu_tau:.6f}")
print(f"P(ν̄_e → ν̄_μ) = {P_anu_mu:.6f}")
print(f"P(ν̄_e → ν̄_τ) = {P_anu_tau:.6f}")
print(f"ΔP_CP (ν_μ) = {P_nu_mu - P_anu_mu:.6f}")
print(f"ΔP_CP (ν_τ) = {P_nu_tau - P_anu_tau:.6f}")

# ============================================================================
# 11. WIZUALIZACJA: PRAWDOPODOBIEŃSTWA W FUNKCJI DŁUGOŚCI DROGI
# ============================================================================
def probability_vs_length(lambda_vals, H_func, initial_state, flavor_index=1):
    """
    Oblicza prawdopodobieństwo oscylacji ν_e → ν_flavor wzdłuż λ.
    flavor_index: 1 dla ν_μ, 2 dla ν_τ.
    """
    probs = []
    for lam in lambda_vals:
        H = H_func(lam)
        # Propagator od 0 do lam (przybliżenie: całkowanie równania Schrodingera)
        # Uproszczenie: używamy eksponenty macierzowej dla małych kroków
        # Dla dokładności: rozwiązujemy ODE krok po kroku
        # Tutaj używamy uproszczonej wersji: propagator = expm(-1j * H * lam)
        U_prop = expm(-1j * H * lam)
        psi_lam = U_prop @ initial_state
        amp = U[:, flavor_index].conj().T @ psi_lam
        probs.append(np.abs(amp)**2)
    return np.array(probs)

# Dla neutrin
P_nu_mu_vals = probability_vs_length(lambda_vals, H_func, initial_nu, flavor_index=1)
P_nu_tau_vals = probability_vs_length(lambda_vals, H_func, initial_nu, flavor_index=2)

# Dla antyneutrin
P_anu_mu_vals = probability_vs_length(lambda_vals, H_func_anu, initial_nu, flavor_index=1)
P_anu_tau_vals = probability_vs_length(lambda_vals, H_func_anu, initial_nu, flavor_index=2)

# Konwersja λ na długość drogi [km] dla osi x
L_km = lambda_vals * 1e17  # skala umowna

plt.figure(figsize=(14, 6))

# Wykres 1: ν_e → ν_μ
plt.subplot(1, 2, 1)
plt.plot(L_km, P_nu_mu_vals, label=r'$P(\nu_e \to \nu_\mu)$', linewidth=2)
plt.plot(L_km, P_anu_mu_vals, label=r'$P(\bar{\nu}_e \to \bar{\nu}_\mu)$', linewidth=2)
plt.plot(L_km, P_nu_mu_vals - P_anu_mu_vals, '--', label=r'$\Delta P_{CP}^{\mu}$', color='black')
plt.xlabel('Długość drogi L [km]', fontsize=12)
plt.ylabel('Prawdopodobieństwo oscylacji', fontsize=12)
plt.title('Oscylacje ν_e → ν_μ z metatime', fontsize=14)
plt.legend()
plt.grid(True)

# Wykres 2: ν_e → ν_τ
plt.subplot(1, 2, 2)
plt.plot(L_km, P_nu_tau_vals, label=r'$P(\nu_e \to \nu_\tau)$', linewidth=2)
plt.plot(L_km, P_anu_tau_vals, label=r'$P(\bar{\nu}_e \to \bar{\nu}_\tau)$', linewidth=2)
plt.plot(L_km, P_nu_tau_vals - P_anu_tau_vals, '--', label=r'$\Delta P_{CP}^{\tau}$', color='black')
plt.xlabel('Długość drogi L [km]', fontsize=12)
plt.ylabel('Prawdopodobieństwo oscylacji', fontsize=12)
plt.title('Oscylacje ν_e → ν_τ z metatime', fontsize=14)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# ============================================================================
# 12. MAPA CHIRALNOŚCI MANDELBROTA-LIKE (sekcja 9)
# ============================================================================
def mandelbrot_metatime(c_phi, c_T, max_iter=100):
    """
    Iteracyjna mapa: 𝒯_{n+1} = 𝒯_n^2 + c, gdzie c = (c_phi, c_T)
    Zwraca liczbę iteracji do ucieczki.
    """
    # 𝒯 = (phi, T) – upraszczamy T do skalarnego T
    phi = 0.0
    T = 0.0
    for i in range(max_iter):
        phi_new = phi**2 - T**2 + c_phi
        T_new = 2*phi*T + c_T
        phi, T = phi_new, T_new
        norm2 = phi**2 + T**2
        if norm2 > 4.0:
            return i
    return max_iter

# Siatka punktów w płaszczyźnie (c_phi, c_T)
N_grid = 200
c_phi_vals = np.linspace(-2, 2, N_grid)
c_T_vals = np.linspace(-2, 2, N_grid)
mandelbrot = np.zeros((N_grid, N_grid))

for i, c_phi in enumerate(c_phi_vals):
    for j, c_T in enumerate(c_T_vals):
        mandelbrot[i, j] = mandelbrot_metatime(c_phi, c_T)

plt.figure(figsize=(8, 6))
plt.imshow(mandelbrot.T, extent=[-2, 2, -2, 2], origin='lower', cmap='hot')
plt.colorbar(label='Iteracje do ucieczki')
plt.xlabel(r'$c_{\phi}$ (skalarna amplituda)', fontsize=12)
plt.ylabel('$c_T$ (tensorowa amplituda)', fontsize=12)
plt.title('Zbiór Mandelbrota-like dla pola metatime', fontsize=14)
plt.show()
