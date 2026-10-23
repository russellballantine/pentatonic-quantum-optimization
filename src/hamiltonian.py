import numpy as np

def generate_spiral_fifths_frequencies(n_qubits=5):
    """Generates frequencies along the pure Spiral of Fifths, folded into [1.0, 2.0)."""
    freqs = []
    current_f = 1.0
    for _ in range(n_qubits):
        freqs.append(current_f)
        current_f = current_f * 1.5
        while current_f >= 2.0:
            current_f /= 2.0
    return np.array(freqs)

def compute_log_distance_matrix(freqs):
    """Computes D_ij = | log2(f_i) - log2(f_j) | mod 1"""
    n = len(freqs)
    log_f = np.log2(freqs)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            diff = np.abs(log_f[i] - log_f[j])
            D[i, j] = diff % 1.0
    return D

def construct_p_qaoa_hamiltonian_matrix(freqs):
    """
    Constructs the cost matrix based on the Hamiltonian rules:
    - Pure Fifths (~0.5849): Lowest energy resonance (-1.0)
    - Minor Seconds / Tritones (~0.0931, ~0.4919): Penalty (+2.5)
    - Background continuous distance field: 0.5 * D_ij
    """
    n = len(freqs)
    D = compute_log_distance_matrix(freqs)
    cost_matrix = 0.5 * D
    
    # Target intervals
    fifth_target = np.log2(1.5) % 1.0        # ~0.5849
    minor_second = np.log2(16/15) % 1.0     # ~0.0931
    tritone = np.log2(45/32) % 1.0          # ~0.4919
    
    tol = 1e-5
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            diff = D[i, j]
            # Check resonance / penalties (accounting for directional symmetry mod 1)
            if np.isclose(diff, fifth_target, atol=tol) or np.isclose(1.0 - diff, fifth_target, atol=tol):
                cost_matrix[i, j] = -1.0
            elif np.isclose(diff, minor_second, atol=tol) or np.isclose(1.0 - diff, minor_second, atol=tol):
                cost_matrix[i, j] = 2.5
            elif np.isclose(diff, tritone, atol=tol) or np.isclose(1.0 - diff, tritone, atol=tol):
                cost_matrix[i, j] = 2.5
                
    return cost_matrix
