import pennylane as qml
import numpy as np

def p_qaoa_layer(gamma_1, gamma_2, beta, finance_matrix, acoustic_matrix, wires, topology="ring"):
    """
    Applies one layer of P-QAOA with flexible structural routing:
    - topology="ring": Standard cyclic closed loop boundary conditions.
    - topology="ladder": Non-reversible open ladder routing tailored for causal DAG configurations.
    """
    n_qubits = len(wires)
    
    # PHASE 1: Data Field Evolution (gamma_1)
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            weight = finance_matrix[i, j]
            if np.abs(weight) > 1e-5:
                qml.CNOT(wires=[wires[i], wires[j]])
                qml.RZ(2 * gamma_1 * weight, wires=wires[j])
                qml.CNOT(wires=[wires[i], wires[j]])
                
    # PHASE 2: Acoustic Prior Field Evolution (gamma_2)
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            weight = acoustic_matrix[i, j]
            if np.abs(weight) > 1e-5:
                qml.CNOT(wires=[wires[i], wires[j]])
                qml.RZ(2 * gamma_2 * weight, wires=wires[j])
                qml.CNOT(wires=[wires[i], wires[j]])
                
    # PHASE 3: Variational Mixer Layer (beta)
    for i in range(n_qubits):
        qml.RX(2 * beta, wires=wires[i])
        
    # Structural routing based on data geometry
    if topology == "ring":
        # Closed cyclic translation loop
        for i in range(n_qubits):
            qml.CNOT(wires=[wires[i], wires[(i + 1) % n_qubits]])
    elif topology == "ladder":
        # Strict open-ended downstream causal flow (No feedback loops)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[wires[i], wires[i + 1]])
