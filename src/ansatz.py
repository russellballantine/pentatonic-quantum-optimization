import pennylane as qml
import numpy as np

def p_qaoa_layer(gamma, beta, cost_matrix, wires):
    """
    Applies one layer of P-QAOA:
    1. Symmetry-Protected Cost Layer: exp(-i * gamma * H_cost)
    2. Ring-Mixer Layer: exp(-i * beta * H_mixer) mapped to a Qubit Ring
    """
    n_qubits = len(wires)
    
    # 1. Cost Hamiltonian Evolution (Ising-like ZZ couplings)
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            weight = cost_matrix[i, j]
            if np.abs(weight) > 1e-5:
                qml.CNOT(wires=[wires[i], wires[j]])
                qml.RZ(2 * gamma * weight, wires=wires[j])
                qml.CNOT(wires=[wires[i], wires[j]])
                
    # 2. Symmetry-Preserving Ring Mixer (Ring-coupled X architecture)
    for i in range(n_qubits):
        qml.RX(2 * beta, wires=wires[i])
    for i in range(n_qubits):
        qml.CNOT(wires=[wires[i], wires[(i + 1) % n_qubits]])
