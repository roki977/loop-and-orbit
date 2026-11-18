# Idea card: When Does Environment-Grounded Verification Improve Self-Generated Training Data?

- Author / date: Raised in a ChatGPT discussion with the user ("学习自我改进 Agent", 2026-11-19); recorded by Muse, 2026-11-19
- Related direction: other (self-improvement / self-generated training data — not A1 cross-game transfer, not Blank A)

## Problem

A model generates its own training data (A). Two ways to filter it can disagree: internal evaluation (B — the model judges its own output) and environment verification (C — the model executes in an environment and gets verifiable external feedback). When do they complement each other, and when do they conflict? Three cases are worth analysing: B says correct but C finds the code unrunnable; B says not good enough but C finds it passes all tests; B and C both say correct but the model still fails on a shifted task distribution.

## Why it is worth doing (gap in existing work, with sources)

The question allows conditional conclusions instead of a yes/no answer: for which tasks, for which error types, at what verification cost, when internal evaluation is already enough, and when external verification is necessary. Source: the survey *Self-Improvements in Modern Agentic Systems: A Survey* (2026, arXiv:2607.13104), Section 5 (A = Intrinsic Generative Demonstrations, B = Intrinsic Evaluative Feedback, C = Extrinsic Exploratory Experience). Whether the gap is real is not yet established — see Novelty Gate below.

## Hypothesis (to be tested)

To be refined after the Novelty Gate. Candidate: environment-grounded verification improves self-generated training data only under conditions (task type, error type, verification cost), and the B-vs-C disagreement cases identify where each method fails.

## Smallest viable experiment (can it run on Colab T4?)

To be decided after the feasibility study. Proposed testbed: a Coding Agent (code is executable, tests are automatic, no robot or expensive equipment needed). Four groups: A vs A+B vs A+C vs A+B+C, with matched generation volume, training budget, model and test set.

## Risks and confounds

- Crowded field: STaR, Self-Rewarding, LLM-as-a-Judge, execution-based verification (CodeT, LEVER) — a near-identical comparison may already exist.
- Generator-judge correlation: if B and A use the same model, the judge can share the generator's systematic bias.
- Execution verification is not absolute truth: low test coverage lets wrong code pass; hidden tests and boundary cases are needed.
- Training cost: the four-group comparison requires training a model, heavier than the Orbit-01 API-only experiments.

## Status: idea / Novelty Gate screening done — verdict MODIFY (2026-11-19)

Draft: `novelty-assessment-env-verification-draft.md`. The broad question is partly answered: OpenCodeInstruct (Ahmad et al. 2025) already compares LLM-judgment filtering against execution filtering for training data and reports the judge more effective; SSD (Zhang et al. 2026) shows raw unverified self-generated data alone lifts Qwen3-30B 42.4% → 55.3% pass@1 on LiveCodeBench v6. Still open: the controlled four-group factorial with strict equal budgets, and the B-vs-C disagreement analysis as the headline finding. Not adopted as a research direction — direction decisions belong to the human team, and this is a different direction from A1. Do not start coding; the next step would be a full read of OpenCodeInstruct Table 4.
