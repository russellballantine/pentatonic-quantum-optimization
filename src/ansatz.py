import pennylane as qml
import numpy as np

def p_qaoa_layer(gamma_1, gamma_2, beta, finance_matrix, acoustic_matrix, wires):
    """
    Applies one decoupled layer of P-QAOA:
    1. Financial Landscape Evolution: exp(-i * gamma_1 * H_finance)
    2. Symmetry-Protected Acoustic Prior Evolution: exp(-i * gamma_2 * H_acoustic)
    3. Ring-Mixer Layer: exp(-i * beta * H_mixer) mapped to a cyclic Qubit Ring
    """
    n_qubits = len(wires)
    
    # -------------------------------------------------------------------------
    # PHASE 1: Financial Data Field Evolution (gamma_1)
    # Allows state amplitudes to shift based on asset correlations
    # -------------------------------------------------------------------------
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            weight = finance_matrix[i, j]
            if np.abs(weight) > 1e-5:
                qml.CNOT(wires=[wires[i], wires[j]])
                qml.RZ(2 * gamma_1 * weight, wires=wires[j])
                qml.CNOT(wires=[wires[i], wires[j]])
                
    # -------------------------------------------------------------------------
    # PHASE 2: Acoustic Prior Field Evolution (gamma_2)
    # Acts as a geometric lens, filtering states into natural untempered resonance
    # -------------------------------------------------------------------------
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            weight = acoustic_matrix[i, j]
            if np.abs(weight) > 1e-5:
                qml.CNOT(wires=[wires[i], wires[j]])
                qml.RZ(2 * gamma_2 * weight, wires=wires[j])
                qml.CNOT(wires=[wires[i], wires[j]])
                
    # -------------------------------------------------------------------------
    # PHASE 3: Symmetry-Preserving Ring Mixer (beta)
    # Restricts quantum walk exploration sequentially along the boundary loop
    # -------------------------------------------------------------------------
    for i in range(n_qubits):
        qml.RX(2 * beta, wires=wires[i])
    for i in range(n_qubits):
        qml.CNOT(wires=[wires[i], wires[(i + 1) % n_qubits]])
