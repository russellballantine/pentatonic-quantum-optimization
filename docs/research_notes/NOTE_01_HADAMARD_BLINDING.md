# Research Note 01: Bypassing the Hadamard Blinding Constraint
**Status:** Closed / Superseded by Variational Operator Decoupling  
**Component:** `src/benchmark_finance.py`  
**Date:** October 2026

## 1. Summary of Initial Condition & Defect Discovery
In Phase 1 of the P-QAOA benchmarking, a rigid element-wise Hadamard product was utilized to construct the cost landscape:
$$J_{\text{combined}} = H_{\text{acoustic}} \odot M_{\text{finance}}$$

Initial benchmarking against a 5-ETF sector portfolio yielded an unexpected energy entrapment for the Pentatonic architecture:
* **Classical Simulated Annealing:** `-1.046713`
* **Standard Unstructured QAOA:** `-0.783202` (91 iterations)
* **Pentatonic Geometrically Prior-QAOA (P-QAOA):** `-0.148976` (78 iterations)

While P-QAOA converged faster (78 vs 91 iterations), it was trapped in a shallow local minimum, underperforming unstructured QAOA by **0.634226 energy units**.

## 2. Theoretical Post-Mortem: The Geometric Penalty Paradox
A mathematical analysis revealed a structural flaw in the initial data injection logic. By multiplying the matrices element-wise *classically before circuit execution*, we blindly assigned static qubit indices to specific assets (e.g., SPY to Qubit 0, XLV to Qubit 3).

In real-world market space, SPY and XLV share a massive correlation of **0.888**. However, the physical distance between Qubit 0 and Qubit 3 on our untempered logarithmic spiral landed on a high-energy structural penalty interval. This forced a fundamental mathematical contradiction directly into the Hamiltonian. 

The ansatz did not fail; it successfully obeyed its geometric translation boundary rules. The Ring-Mixer ($C_n$ cyclic group symmetry) successfully restricted sequential information flow, meaning it actively prevented the state vector from collapsing into the target market clusters because doing so would violate the spatial layout rules imposed by our blind classical assignment. We essentially hand-crafted a self-contradictory landscape.

## 3. Pivot Strategy (Mitigation)
To allow the pentatonic prior to autonomously detect and filter data correlations without classical pre-sorting (which would defeat the purpose of a quantum advantage algorithm), we must decouple the operators. 

Instead of an element-wise product, the data and the geometric prior must act as independent, competing physical fields inside a split-variational cost layer:
$$U_C(\gamma_1, \gamma_2) = e^{-i \gamma_2 H_{\text{acoustic}}} e^{-i \gamma_1 H_{\text{finance}}}$$

This allows the quantum state vector to utilize constructive quantum interference during the optimization loop to naturally shift and map the high-correlation data clusters into the low-energy acoustic resonance channels autonomously.

## 4. Next Action Steps
- [ ] Refactor `src/ansatz.py` to support decoupled dual-parameter cost layers (`gamma_1`, `gamma_2`).
- [ ] Update `src/benchmark_finance.py` to pass the independent fields into the variational loop.
- [ ] Re-test to evaluate autonomous structural alignment.
