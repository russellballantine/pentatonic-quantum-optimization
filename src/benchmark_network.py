import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

import numpy as np
import networkx as nx
import pandas as pd
import pennylane as qml
from scipy.optimize import minimize

from hamiltonian import generate_spiral_fifths_frequencies, construct_p_qaoa_hamiltonian_matrix
from ansatz import p_qaoa_layer

def main():
    # 1. Extract a slice of Zachary's Karate Club graph (Sub-graph scaled to 5 qubits for baseline parity)
    print("🥋 Extracting native community structures from networkx.karate_club_graph()...")
    G = nx.karate_club_graph()
    nodes = [0, 1, 2, 3, 4]  # Focus node core cluster
    subgraph = G.subgraph(nodes)
    adjacency_matrix = nx.to_numpy_array(subgraph)
    
    n_qubits = len(nodes)
    layers = 2
    
    print("\n📊 Sparse Symmetric Network Adjacency Matrix:")
    print(pd.DataFrame(adjacency_matrix).round(1))
    
    # Generate original cyclic modulo-1 acoustic landscape matrix
    freqs = generate_spiral_fifths_frequencies(n_qubits=n_qubits)
    acoustic_hamiltonian = construct_p_qaoa_hamiltonian_matrix(freqs)
    
    combined_cost_matrix = acoustic_hamiltonian * adjacency_matrix
    
    # Map to quantum observables
    obs = []
    coeffs = []
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            weight = combined_cost_matrix[i, j]
            if np.abs(weight) > 1e-5:
                obs.append(qml.PauliZ(i) @ qml.PauliZ(j))
                coeffs.append(weight)
                
    quantum_hamiltonian = qml.Hamiltonian(coeffs, obs)
    
    # 2. Setup Quantum Simulators
    dev_p = qml.device("default.qubit", wires=n_qubits)
    dev_std = qml.device("default.qubit", wires=n_qubits)
    
    # Ring-Coupled P-QAOA Node (topology="ring")
    @qml.qnode(dev_p)
    def p_qaoa_circuit(params):
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
        for p in range(layers):
            idx = p * 3
            g1, g2, b = params[idx], params[idx+1], params[idx+2]
            p_qaoa_layer(g1, g2, b, adjacency_matrix, acoustic_hamiltonian, wires=range(n_qubits), topology="ring")
        return qml.expval(quantum_hamiltonian)

    # Standard QAOA Node
    @qml.qnode(dev_std)
    def standard_qaoa_circuit(params):
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
        for p in range(layers):
            idx = p * 2
            g, b = params[idx], params[idx+1]
            n_qubits_wires = len(range(n_qubits))
            for k in range(n_qubits_wires):
                for m in range(k + 1, n_qubits_wires):
                    w = combined_cost_matrix[k, m]
                    qml.CNOT(wires=[k, m])
                    qml.RZ(2 * g * w, wires=m)
                    qml.CNOT(wires=[k, m])
            for k in range(n_qubits_wires):
                qml.RX(2 * b, wires=k)
        return qml.expval(quantum_hamiltonian)

    # 3. Process Parameters Search Loops
    initial_params_p = np.array([0.1] * (layers * 3), dtype=float)
    initial_params_std = np.array([0.1] * (layers * 2), dtype=float)
    
    print("\n🚀 Commencing sparse geometric parameter optimization loops...")
    res_p = minimize(p_qaoa_circuit, initial_params_p, method="Nelder-Mead")
    res_std = minimize(standard_qaoa_circuit, initial_params_std, method="Nelder-Mead")
    
    print("\n================================================================================")
    print("                BENCHMARK RESULTS: SPARSE GEOMETRIC NETWORK                     ")
    print("================================================================================")
    print(f"Standard Unstructured QAOA Expected Energy   : {res_std.fun:.6f}")
    print(f"Ring-Mixer Pentatonic Variational Energy     : {res_p.fun:.6f}")
    print("================================================================================")

if __name__ == "__main__":
    main()
