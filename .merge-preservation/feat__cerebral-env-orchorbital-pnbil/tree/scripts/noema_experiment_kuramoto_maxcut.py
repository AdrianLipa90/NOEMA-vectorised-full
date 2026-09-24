#!/usr/bin/env python3
"""Experiment (2026-07-11): does NOEMA's own Kuramoto phase-coupling math
converge to correct MAX-CUT solutions, per the "oscillator-based Ising
machine" literature (see docs/science/OSCILLATOR_ISING_MACHINES_BIBLIOGRAPHY.md)?

Adrian's framing, verbatim context: PhaseNav should be exactly this kind of
tool — a phase-coupling solver — but with semantics/logic on "hidden"
parameters that are explicit to us, not opaque generic spins. Before mapping
anything semantic onto it, this validates the RAW mechanism: does anti-phase
Kuramoto coupling actually find good/optimal graph cuts on a small, brute-
force-checkable test graph?

Method (per Max-Cut via Kuramoto-Type Oscillators, SIAM J. Applied Dynamical
Systems, and the OIM papers): MAX-CUT maps to antiferromagnetic Ising
coupling (J_ij = -1 per edge — want endpoints OUT of phase). Kuramoto ODE:
    dphi_i/dt = omega_i + sum_j K_ij * sin(phi_j - phi_i)
For MAX-CUT, K_ij = -coupling_strength for each edge (i,j) — negative
coupling drives anti-synchronization (phase difference -> pi) instead of
the usual positive-coupling synchronization (phase difference -> 0).
After integration, threshold each oscillator's final phase against the mean
phase: two sides of the partition = which side of the mean each phase falls
on (same binary-partition-from-phase-sign idea the literature uses).
"""
from __future__ import annotations

import itertools
import numpy as np


def brute_force_max_cut(adj: np.ndarray) -> tuple[float, tuple[int, ...]]:
    """Exact optimum via 2^n enumeration — only feasible for small n,
    exactly why this test graph is kept small (n<=14)."""
    n = adj.shape[0]
    best_cut = -1.0
    best_partition = None
    for bits in itertools.product([0, 1], repeat=n):
        cut = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if adj[i, j] != 0 and bits[i] != bits[j]:
                    cut += adj[i, j]
        if cut > best_cut:
            best_cut = cut
            best_partition = bits
    return best_cut, best_partition


def kuramoto_max_cut(
    adj: np.ndarray,
    *,
    steps: int = 4000,
    dt: float = 0.01,
    coupling_strength: float = 1.0,
    seed: int = 0,
    n_restarts: int = 20,
) -> tuple[float, np.ndarray]:
    """Anti-phase Kuramoto relaxation for MAX-CUT, exactly the mechanism
    already used elsewhere in this codebase (orch_orbital.py's
    run_entity_mini_pass(), phasenav_learning_gate.py's
    _vector_phase_coupling()) — same Euler-integrated coupled-oscillator
    ODE, just with NEGATIVE coupling on graph edges (antiferromagnetic,
    per the MAX-CUT-via-Kuramoto literature) instead of positive.

    n_restarts: Kuramoto relaxation finds LOCAL minima of the coupling
    energy, same caveat the OIM papers note explicitly — multiple random
    phase-initializations and keeping the best result is the standard
    mitigation, not a deviation from the method."""
    n = adj.shape[0]
    rng = np.random.default_rng(seed)

    best_cut = -1.0
    best_phi = None

    for restart in range(n_restarts):
        phi = rng.uniform(0, 2 * np.pi, n)
        K = -coupling_strength * adj  # antiferromagnetic: negative coupling

        for _ in range(steps):
            # dphi_i/dt = sum_j K_ij * sin(phi_j - phi_i)  (omega_i = 0, no
            # natural frequency spread — pure relaxation to the coupling
            # graph's structure, matching the Ising-ground-state framing)
            diff = phi[None, :] - phi[:, None]  # phi_j - phi_i, shape (n,n)
            force = np.sum(K * np.sin(diff), axis=1)
            phi = (phi + dt * force) % (2 * np.pi)

        # Partition: which side of the circular mean each oscillator falls
        mean_phi = np.angle(np.mean(np.exp(1j * phi)))
        bits = tuple(int(((p - mean_phi) % (2 * np.pi)) > np.pi) for p in phi)

        cut = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if adj[i, j] != 0 and bits[i] != bits[j]:
                    cut += adj[i, j]

        if cut > best_cut:
            best_cut = cut
            best_phi = phi.copy()

    return best_cut, best_phi


def main():
    # Test graph 1: unweighted 5-cycle + one chord (n=6) — small enough for
    # brute force, has a nontrivial (not all-or-nothing) optimal cut.
    print("=== Test graph 1: 6-node cycle + chord ===")
    adj1 = np.zeros((6, 6))
    edges1 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)]
    for i, j in edges1:
        adj1[i, j] = adj1[j, i] = 1.0
    opt_cut1, opt_part1 = brute_force_max_cut(adj1)
    kur_cut1, _ = kuramoto_max_cut(adj1)
    print(f"n_edges={len(edges1)}  brute-force optimum={opt_cut1}  kuramoto found={kur_cut1}")
    print(f"match: {kur_cut1 == opt_cut1}")

    # Test graph 2: weighted random graph, n=10, moderate density
    print("\n=== Test graph 2: weighted random graph, n=10 ===")
    rng = np.random.default_rng(42)
    n2 = 10
    adj2 = np.zeros((n2, n2))
    for i in range(n2):
        for j in range(i + 1, n2):
            if rng.random() < 0.4:
                w = round(rng.uniform(0.5, 2.0), 2)
                adj2[i, j] = adj2[j, i] = w
    n_edges2 = int(np.count_nonzero(adj2) / 2)
    opt_cut2, opt_part2 = brute_force_max_cut(adj2)
    kur_cut2, _ = kuramoto_max_cut(adj2)
    print(f"n_edges={n_edges2}  brute-force optimum={opt_cut2:.2f}  kuramoto found={kur_cut2:.2f}")
    print(f"ratio (kuramoto/optimum): {kur_cut2/opt_cut2:.4f}")

    # Test graph 3: n=13 (near the practical brute-force ceiling), sparser
    print("\n=== Test graph 3: weighted random graph, n=13, sparser ===")
    n3 = 13
    adj3 = np.zeros((n3, n3))
    rng3 = np.random.default_rng(7)
    for i in range(n3):
        for j in range(i + 1, n3):
            if rng3.random() < 0.25:
                w = round(rng3.uniform(0.5, 2.0), 2)
                adj3[i, j] = adj3[j, i] = w
    n_edges3 = int(np.count_nonzero(adj3) / 2)
    opt_cut3, _ = brute_force_max_cut(adj3)
    kur_cut3, _ = kuramoto_max_cut(adj3)
    print(f"n_edges={n_edges3}  brute-force optimum={opt_cut3:.2f}  kuramoto found={kur_cut3:.2f}")
    print(f"ratio (kuramoto/optimum): {kur_cut3/opt_cut3:.4f}")


if __name__ == "__main__":
    main()
