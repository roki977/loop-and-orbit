# Idea card: Which part to modify — meta-judgment in self-improving systems

- Author / date: Yuzhe Ma / 2026-11-19
- Related direction: other (paper extension of the Self-Improvements survey; adjacent to the env-verification candidate)

## Problem
A self-improving system needs two capabilities, not one: (1) the ability to modify itself, and (2) the ability to correctly judge *which part of itself* should be modified. The survey's framework (Ren et al. 2026, arXiv:2607.13104) separates Foundation Model Improvement (θ) from Scaffolding Improvement (Σ) — it says *where* improvement can happen, but not *how* the system decides which part to change. This idea is an extension of the paper: the meta-judgment of the modification target is itself a capability that needs explaining.

## Why it is worth doing (gap in existing work, with sources)
- The survey (Ren et al. 2026) covers improvement mechanisms at both levels but does not treat target selection — deciding between θ and Σ, or between components within each — as a research problem in its own right.
- The judgment depends on verification: without a reliable signal, the system cannot tell which part is the bottleneck, so modifications are misdirected. This connects directly to the verification-bottleneck consensus (independent verifiers as the limiting factor) and to the Gödel Machine's proof searcher, which decides whether a self-modification is provably beneficial — and whose proof cost is its bottleneck.
- It is also a credit-assignment problem: attributing a failure to the right component (model weights, prompt/scaffold, data, verifier) before changing it.

## Hypothesis (to be tested)
Meta-judgment is the binding constraint on self-improvement: a system that can modify itself but cannot correctly target the modification will not reliably improve, and may regress. Given a reliable independent verifier, targeted modification beats blind or fixed-target modification; without one, targeting fails and improvement stalls.

## Smallest viable experiment (can it run on Colab T4?)
Small pilot, one coding/PCB task, one small model: compare (a) a system that chooses which part to modify using independent verification feedback (e.g. DRC/SPICE results point at the failing component) against (b) the same system modifying a fixed part or a randomly chosen part. Measure success rate and reliable-solvable-set change. No full training run; data-quality / decision-quality measurement only.

## Risks and confounds
- The "which part" judgment itself needs verification — circularity if the system judges itself with its own (possibly flawed) evaluator.
- Hard to isolate targeting quality from modification quality: a good target with a bad modification looks like a bad target.
- The distinction between θ and Σ may blur in practice (e.g. prompt changes that mimic weight changes).

## Status: idea
