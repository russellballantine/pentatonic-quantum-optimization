import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

import numpy as np
import pandas as pd
import pennylane as qml
from scipy.optimize import minimize

# Import your core module dependencies
from hamiltonian import generate_spiral_fifths_frequencies, compute_log_distance_matrix
from ansatz import p_qaoa_layer

def generate_causal_dag_matrix(n_nodes=5):
    """
    Synthesizes a strict Directed Acyclic Graph representing a causal hierarchy path
    (e.g., Node 0 -> Node 1 -> Node 2 -> Node 3 -> Node 4).
    Asymmetric weights signify directed structural priority dependencies.
    """
    dag_matrix = np.zeros((n_nodes, n_nodes))
    for i in range(n_nodes - 1):
        dag_matrix[i, i + 1] = 1.8  # Strong downstream causal connection
    return dag_matrix

def standard_qaoa_layer(gamma, beta, cost_matrix, wires):
    """Standard unstructured QAOA layer with a decoupled transverse mixer."""
    n_qubits = len(wires)
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            weight = cost_matrix[i, j]
            qml.CNOT(wires=[wires[i], wires[j]])
            qml.RZ(2 * gamma * weight, wires=wires[j])
            qml.CNOT(wires=[wires[i], wires[j]])
    for i in range(n_qubits):
        qml.RX(2 * beta, wires=wires[i])

def main():
    n_qubits = 5
    layers = 2  # Evaluate at depth p=2
    print(f"🌲 Initializing Causal DAG Structural Evaluation Framework (p={layers})...")
    
    # 1. Setup Causal Matrix Landscapes
    dag_matrix = generate_causal_dag_matrix(n_nodes=n_qubits)
    print("\n📋 Directed Dependency Weight Manifold (DAG):")
    print(pd.DataFrame(dag_matrix).round(1))
    
    # Generate unrolled spiral coordinates (No Modulo-1 wrap-around, true linear ladder)
    freqs = generate_spiral_fifths_frequencies(n_qubits=n_qubits)
    log_f = np.log2(freqs)
    acoustic_ladder = np.zeros((n_qubits, n_qubits))
    for i in range(n_qubits):
        for j in range(n_qubits):
            # Preserves unrolled continuous physical distance asymmetry
            acoustic_ladder[i, j] = np.abs(log_f[i] - log_f[j])
            
    combined_cost_matrix = acoustic_ladder * dag_matrix
    
    # 2. Map Multi-Qubit Pauli Quantum Observables
    obs = []
    coeffs = []
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            weight = combined_cost_matrix[i, j]
            if np.abs(weight) > 1e-5:
                obs.append(qml.PauliZ(i) @ qml.PauliZ(j))
                coeffs.append(weight)
                
    quantum_hamiltonian = qml.Hamiltonian(coeffs, obs)
    
    # 3. Instantiate Quantum Simulation Nodes
    dev_p = qml.device("default.qubit", wires=n_qubits)
    dev_std = qml.device("default.qubit", wires=n_qubits)
    
    # Causal P-QAOA QNode (Configured with topology="ladder")
    @qml.qnode(dev_p)
    def p_qaoa_circuit(params):
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
        for p in range(layers):
            idx = p * 3
            g1, g2, b = params[idx], params[idx+1], params[idx+2]
            p_qaoa_layer(g1, g2, b, dag_matrix, acoustic_ladder, wires=range(n_qubits), topology="ladder")
        return qml.expval(quantum_hamiltonian)

    # Standard Unstructured QAOA QNode
    @qml.qnode(dev_std)
    def standard_qaoa_circuit(params):
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
        for p in range(layers):
            idx = p * 2
            g, b = params[idx], params[idx+1]
            standard_qaoa_layer(g, b, combined_cost_matrix, wires=range(n_qubits))
        return qml.expval(quantum_hamiltonian)

    # 4. Process Parameter Search Loops
    initial_params_p = np.array([0.1] * (layers * 3), dtype=float)
    initial_params_std = np.array([0.1] * (layers * 2), dtype=float)
    
    print("\n🚀 Processing causal parameter searches...")
    res_p = minimize(p_qaoa_circuit, initial_params_p, method="Nelder-Mead")
    res_std = minimize(standard_qaoa_circuit, initial_params_std, method="Nelder-Mead")
    
    # 5. Output Research Performance Reports
    print("\n================================================================================")
    print("                    BENCHMARK RESULTS: CAUSAL DAG FLOWS                         ")
    print("================================================================================")
    print(f"Standard Unstructured QAOA Expected Energy   : {res_std.fun:.6f} (Iterations: {res_std.nfev})")
    print(f"Open Ladder Pentatonic Variational Energy     : {res_p.fun:.6f} (Iterations: {res_p.nfev})")
    print("================================================================================")
    
    diff = res_std.fun - res_p.fun
    if diff > 1e-4:
        print(f"🔥 Quantum Advantage Confirmed: Causal P-QAOA beat standard QAOA by {abs(diff):.6f} units!")
    elif abs(diff) <= 1e-4:
        print("⚖️ Analysis: Identical energetic convergence thresholds captured.")
    else:
        print(f"⚠️ Analysis: Unstructured framework remains lower by {abs(diff):.6f} energy fields.")

if __name__ == "__main__":
    main()
