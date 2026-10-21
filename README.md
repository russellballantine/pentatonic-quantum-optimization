# Pentatonic Quantum Approximate Optimization Algorithm (P-QAOA)

An interdisciplinary research framework exploring the intersection of **Quantum Information Theory, Parametric Unitaries, and Pure Acoustic Physics**. 

This repository implements a novel variant of the Quantum Approximate Optimization Algorithm (QAOA) in **PennyLane**. Rather than utilizing man-made discrete scales (such as 12-tone equal temperament), this framework projects the infinite, untempered **Spiral of Fifths** directly onto a qubit-based quantum architecture. By leveraging the rational geometric approximations of this continuous spiral, we construct a natural **Symmetry-Protected Subspace** to smooth non-convex optimization error landscapes.

---

## 💻 Core Concept & Mathematical Architecture

### 1. The Untempered Spiral of Fifths
Equal temperament forces twelve 3:2 perfect fifths to equal seven 2:1 octaves (2⁷ = 128 vs. (3/2)¹² ≈ 129.74). This artificial loop introduces the **Pythagorean Comma**. 

This project bypasses this compromise by mapping couplings to the true physical distance along the infinite logarithmic spiral:
\[D_{ij} = \left\vert \log_2(f_i) - \log_2(f_j) \right\vert \pmod 1\]

### 2. The Pentatonic Subspace Prior
Using continued fractions, the rational fraction 3/5 emerges as the first deeply stable, highly accurate structural closure of the spiral. The **Pentatonic Scale** is therefore treated as a fundamental, naturally occurring gauge symmetry. 

By penalizing acoustic dissonance (e.g., minor seconds and tritones) and encouraging natural resonance (perfect fifths), our cost Hamiltonian acts as a spectral filter that guides the quantum walk away from trapping local minima.

---

## 🛠️ Repository Layout
*📂 Repository structure to be populated as the framework scales:*
* `src/hamiltonian.py` — Logarithmic physical distance matrices and untempered mapping logic.
* `src/ansatz.py` — Symmetry-preserving parametric unitaries and P-QAOA circuit layers.
* `src/benchmarks.py` — Optimization loops evaluating performance against standard QAOA and Simulated Annealing.
* `data/` — Local asset allocation, genomic sequences, and network graph datasets.

---

## 🚀 Quick Start & Installation

Ensure you are operating inside an isolated virtual environment (`.venv`), then install the core scientific dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔬 Benchmarking Target Objectives
We evaluate the convergence rate and error landscape characteristics of P-QAOA across three primary relational domains:
1. **Financial Asset Allocation:** Mapping highly anti-correlated asset structures to resonant intervals.
2. **Bio-Informatics Sequence Clustering:** Mapping evolutionary distances using base-pair genomic metrics.
3. **Structural Community Detection:** Grouping complex graphs (e.g., Zachary’s Karate Club) via consonant relational weights.
