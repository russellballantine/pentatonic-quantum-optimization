import warnings
# Silence the LibreSSL warning from cluttering the terminal output
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

import numpy as np
import pandas as pd
import yfinance as yf
import pennylane as qml
from scipy.optimize import minimize

# Import your core modules
from hamiltonian import generate_spiral_fifths_frequencies, construct_p_qaoa_hamiltonian_matrix
from ansatz import p_qaoa_layer

def fetch_finance_data():
    """Fetches historical data for a 5-ETF sector portfolio."""
    print("📡 Fetching historical sector ETF data via yfinance (Single-Threaded Mode)...")
    tickers = ["SPY", "XLF", "XLK", "XLV", "XLE"]
    
    data = yf.download(
        tickers, 
        period="3y", 
        progress=False, 
        ignore_tz=True,
        threads=False
    )
    
    close_data = data['Close']
    log_returns = np.log(close_data / close_data.shift(1)).dropna()
    correlation_matrix = log_returns.corr().to_numpy()
    return tickers, correlation_matrix

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

def run_classical_simulated_annealing(combined_matrix, steps=1000):
    """Classical Simulated Annealing baseline for portfolio cost minimization."""
    n = len(combined_matrix)
    current_state = np.random.choice([1, -1], size=n)
    
    def get_energy(state):
        return 0.5 * np.dot(state, np.dot(combined_matrix, state))
    
    current_energy = get_energy(current_state)
    best_state = current_state.copy()
    best_energy = current_energy
    
    T = 1.0
    cooling_rate = 0.99
    
    for _ in range(steps):
        T *= cooling_rate
        candidate = current_state.copy()
        idx = np.random.randint(0, n)
        candidate[idx] *= -1
        
        candidate_energy = get_energy(candidate)
        delta_e = candidate_energy - current_energy
        
        if delta_e < 0 or np.random.rand() < np.exp(-delta_e / max(T, 1e-6)):
            current_state = candidate
            current_energy = candidate_energy
            if current_energy < best_energy:
                best_energy = current_energy
                best_state = current_state.copy()
                
    return best_energy, best_state

def main():
    # 1. Load data and setup matrices independently
    tickers, corr_matrix = fetch_finance_data()
    n_qubits = len(tickers)
    layers = 2  # Set depth to p=2
    
    print(f"\n📊 System configured for p={layers} layers.")
    
    # Generate pure acoustic landscape prior matrix
    freqs = generate_spiral_fifths_frequencies(n_qubits=n_qubits)
    acoustic_hamiltonian = construct_p_qaoa_hamiltonian_matrix(freqs)
    
    # Classical optimization targets standard combination for benchmarking baseline
    combined_cost_matrix = acoustic_hamiltonian * corr_matrix
    
    # Convert combination into a multi-qubit Pauli operator for tracking expectation value
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
    
    # Quantum Node for Decoupled P-QAOA (p=2 layers, 6 parameters)
    @qml.qnode(dev_p)
    def p_qaoa_circuit(params):
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
            
        # Loop through p=2 layers
        for p in range(layers):
            idx = p * 3
            g1, g2, b = params[idx], params[idx+1], params[idx+2]
            p_qaoa_layer(g1, g2, b, corr_matrix, acoustic_hamiltonian, wires=range(n_qubits))
            
        return qml.expval(quantum_hamiltonian)

    # Quantum Node for Standard QAOA (p=2 layers, 4 parameters)
    @qml.qnode(dev_std)
    def standard_qaoa_circuit(params):
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
            
        # Loop through p=2 layers
        for p in range(layers):
            idx = p * 2
            g, b = params[idx], params[idx+1]
            standard_qaoa_layer(g, b, combined_cost_matrix, wires=range(n_qubits))
            
        return qml.expval(quantum_hamiltonian)

    # 3. Execution & Optimization Loops Setup
    initial_params_p = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1], dtype=float)  # 6 parameters
    initial_params_std = np.array([0.1, 0.1, 0.1, 0.1], dtype=float)        # 4 parameters
    
    print("🚀 Commencing deep variational optimization loops (p=2)...")
    
    res_p = minimize(p_qaoa_circuit, initial_params_p, method="Nelder-Mead", options={'maxiter': 1000})
    res_std = minimize(standard_qaoa_circuit, initial_params_std, method="Nelder-Mead", options={'maxiter': 1000})
    sa_energy, sa_state = run_classical_simulated_annealing(combined_cost_matrix)
    
    # 4. Output Research Performance Reports
    print("\n================================================================================")
    print("                DEEP LAYER BENCHMARK RESULTS (p=2): PORTFOLIO                  ")
    print("================================================================================")
    print(f"Classical Simulated Annealing Minimum Energy : {sa_energy:.6f}")
    print(f"Standard Unstructured QAOA Expected Energy   : {res_std.fun:.6f} (Iterations: {res_std.nfev})")
    print(f"Decoupled Pentatonic Variational Energy      : {res_p.fun:.6f} (Iterations: {res_p.nfev})")
    print("================================================================================")
    
    diff = res_std.fun - res_p.fun
    if diff > 1e-4:
        print(f"🔥 Success: At p=2, decoupled P-QAOA broke the layout bottleneck by {abs(diff):.6f} units!")
    elif abs(diff) <= 1e-4:
        print("⚖️ Analysis: Both circuits converged to identical spectral thresholds at p=2.")
    else:
        print(f"⚠️ Analysis: Unstructured framework remains lower by {abs(diff):.6f} energy fields.")

if __name__ == "__main__":
    main()
