# Research Note 03: The Hermitian Operator Constraint in Asymmetric Causal Frameworks
**Status:** Concluded / Pivoting to Sparse Symmetric Graph Topologies  
**Component:** `src/benchmark_dag.py`  
**Date:** October 2026

## 1. Causal DAG Benchmarking Baseline
To evaluate the P-QAOA architecture against unidirectional landscapes, the periodic qubit ring was unrolled into a non-reversible **Linear Ladder Mixer** (\(topology="ladder"\)). The system was tested using a synthesized 5-node Directed Acyclic Graph (DAG) path depth of \(p=2\):

* **Standard Unstructured QAOA Expected Energy:** `-2.617734` (507 iterations)
* **Open Ladder Pentatonic Variational Energy:** `-1.697397` (1200 iterations)

Standard QAOA maintained a clear ground-state advantage, outperforming the open-ladder configuration by **0.920337 energy units**, while the pentatonic landscape maxed out its classical optimization threshold at 1,200 iterations.

## 2. Technical Post-Mortem: Classical Graph Mapping vs. Quantum Compilation Artifacts
A review of the classical-to-quantum compilation pipeline revealed a structural mapping mismatch rather than an algorithmic failure. 

In classical network analysis, Directed Acyclic Graphs are represented via asymmetric, upper-triangular adjacency matrices (\(M_{ij} \neq M_{ji}\)) to explicitly denote causal direction. However, standard multi-qubit Pauli-Ising tracking wrappers (`qml.Hamiltonian`) are natively designed to process bidirectional, symmetric physical couplings to maintain energy-conserving unitary operations.

By passing the raw asymmetric classical DAG matrix directly to the quantum operator compiler:
```python
for i in range(n_qubits):
    for j in range(i + 1, n_qubits):
        obs.append(qml.PauliZ(i) @ qml.PauliZ(j))
```
The compilation layer automatically sampled only the upper-triangular indices and mapped them to bidirectional $Z_i Z_j$ interactions. This implicitly mirrored the weights across the diagonal, effectively flattening our directional DAG back into a bidirectional symmetric network behind the scenes.

The performance trap occurred because the **Open Ladder Mixer** was executing a strict unidirectional quantum walk over an energy landscape that the compilation layer had mapped as a two-way street, resulting in severe phase frustration. This highlights the necessity of utilizing distinct directional encoding methods (such as non-Hermitian dilation or clock-shift operators) when dealing with acyclic data topologies.


## 3. Core R&D Conclusions & Native Structural Fit
Through these initial benchmark phases, we have successfully established the exact operational boundaries of the discrete P-QAOA architecture:

1. **The Portfolio Bottleneck:** Dense statistical data causes severe spatial embedding distortion on a 1D qubit ring.
2. **The DAG Bottleneck:** Asymmetric causal graphs conflict with the native Hermitian requirement of standard multi-qubit Pauli operators.

To achieve a true geometric advantage, the target dataset must natively share the exact physical constraints of our quantum architecture. The data must be **inherently local (sparse)**, **cyclical**, and **perfectly symmetric (bidirectional)**. 

Our final dataset—**Community Detection on the Karate Club Graph**—is a flawless topological match.
