# Research Note 03: The Hermitian Operator Constraint in Asymmetric Causal Frameworks
**Status:** Concluded / Pivoting to Sparse Symmetric Graph Topologies  
**Component:** `src/benchmark_dag.py`  
**Date:** October 2026

## 1. Causal DAG Benchmarking Baseline
To evaluate the P-QAOA architecture against unidirectional landscapes, the periodic qubit ring was unrolled into a non-reversible **Linear Ladder Mixer** (\(topology="ladder"\)). The system was tested using a synthesized 5-node Directed Acyclic Graph (DAG) path depth of \(p=2\):

* **Standard Unstructured QAOA Expected Energy:** `-2.617734` (507 iterations)
* **Open Ladder Pentatonic Variational Energy:** `-1.697397` (1200 iterations)

Standard QAOA maintained a clear ground-state advantage, outperforming the open-ladder configuration by **0.920337 energy units**, while the pentatonic landscape maxed out its classical optimization threshold at 1,200 iterations.

## 2. Theoretical Post-Mortem: The Hermiticity Backaction
A deep-dive analysis of the quantum-to-classical compilation step revealed a fundamental physical constraint: **Standard discrete qubit physics is strictly Hermitian.**

By definition, a DAG represents a non-reversible causal hierarchy path (e.g., Node \(i \rightarrow Node\ j\), but \(Node\ j \not\rightarrow Node\ i\)). This causes the dataset matrix to be entirely upper triangular and asymmetric (\(M_{ij} \neq M_{ji}\)). 

However, in standard quantum information processing, physical observables and time-evolution operators must be Hermitian (\(M = M^\dagger\)) to maintain unitary probability conservation. When the asymmetric matrix was mapped to standard Pauli-Z operators:

```python
for i in range(n_qubits):
    for j in range(i + 1, n_qubits):
        obs.append(qml.PauliZ(i) @ qml.PauliZ(j))
```

The simulator only read the upper triangular couplings ($i < j$) and converted them into standard, bidirectional $Z_i Z_j$ interactions. This implicitly forced the physical landscape to become perfectly symmetric behind the scenes. 

The quantum simulation effectively transformed a one-way causal stream into a **two-way bidirectional pipeline**. The open-ladder mixer—which was designed to march information strictly forward—encountered severe phase frustration when fighting against the bidirectional energy bonds forced by the Pauli mechanics.

## 3. Core R&D Conclusions & Native Structural Fit
Through these initial benchmark phases, we have successfully established the exact operational boundaries of the discrete P-QAOA architecture:

1. **The Portfolio Bottleneck:** Dense statistical data causes severe spatial embedding distortion on a 1D qubit ring.
2. **The DAG Bottleneck:** Asymmetric causal graphs conflict with the native Hermitian requirement of standard multi-qubit Pauli operators.

To achieve a true geometric advantage, the target dataset must natively share the exact physical constraints of our quantum architecture. The data must be **inherently local (sparse)**, **cyclical**, and **perfectly symmetric (bidirectional)**. 

Our final dataset—**Community Detection on the Karate Club Graph**—is a flawless topological match.
