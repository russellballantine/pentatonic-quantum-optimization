# Research Note 02: The Spatial Embedding Bottleneck and Causal Pivot
**Status:** Concluded / Pivoting to Directed Acyclic Graphs (DAGs)  
**Component:** `src/benchmark_finance.py`  
**Date:** October 2026

## 1. High-Depth Scaling Performance Log
Following the variational decoupling refactor, circuit depth was scaled to evaluate asymptotic convergence properties across the dense 5-ETF statistical landscape:

* **Depth $p=1$:** Pentatonic Energy = `-0.161194` (172 iterations)
* **Depth $p=2$:** Pentatonic Energy = `-0.495105` (1192 iterations) [+$207\%$ Optimization]
* **Depth $p=4$:** Pentatonic Energy = `-0.549964` (1349 iterations)

## 2. Empirical Diagnosis: The Dimensionality Wall
While scaling depth from $p=1$ to $p=2$ yielded a massive structural jump, further expansion to $p=4$ flatlined, with the model settling at an asymptotic floor of `-0.549964`. Standard Unstructured QAOA maintained a superior ground-state capture at `-0.903410`.

This establishes a definitive boundary constraint: **Statistical finance data is globally dense.** A fully connected 5-node graph requires a 4-dimensional geometric embedding manifold to be expressed without spatial distortion. 

By forcing this 4D cloud into a 1D physical Qubit Ring ($C_n$ cyclic group translation symmetry), we engineered a permanent **spatial embedding bottleneck**. Adding layers merely increases the duration of the quantum walk along the restricted 1D track but cannot break the track itself.

## 3. Causal Framework Pivot (Directed Acyclic Graphs)
To achieve a geometric quantum advantage, the data topology must natively align with the underlying physics of the ansatz. 

We identify that the untempered generation rule of the Spiral of Fifths ($f_{k+1} = f_k \times 1.5$) is inherently a **one-way, asymmetric, acyclic progression**. It is a hierarchical ladder, not a closed circle.

By unrolling our periodic qubit ring into an open **Linear Ladder Mixer**, we can map the directional, non-reversible edges of a **DAG** directly to the untempered physical generations of the perfect fifth steps, eliminating the embedding distortion completely.
