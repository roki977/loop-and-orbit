# Novelty Assessment (Novelty Gate)

No question is adopted before it passes this gate. Record one assessment per question.

## Checklist

1. **Closest prior work.** Name the closest published studies (directly related and neighbouring fields). Compare questions, methods, environments, and findings.
2. **What is established.** What do those studies already answer?
3. **What is still open.** What gap remains, and why does it matter?
4. **What would be new here.** State the difference precisely — a new question, a new condition, a new measurement, or a new explanation.
5. **What would falsify it.** State what result would count against the hypothesis.

## Template

| Field | Content |
|---|---|
| Question | |
| Closest prior work (with links) | |
| What is established | |
| What is still open | |
| What would be new here | |
| What would falsify it | |
| Verdict | new / partly new / already answered |
| Assessed by / date | |

## Nearest neighbours (from the 2026-11-17 planning reply)

| Study | What it already did | What it means for us |
|---|---|---|
| Akata et al. (2025), Playing Repeated Games with LLMs, Nature Human Behaviour | LLM cooperation, coordination, and opponent information in repeated games | Do not treat a simple cooperation-rate comparison as novel |
| Scaling Inference-Time Computation via Opponent Simulation (ICML 2026) | Opponent simulation and Smooth Fictitious Play for online adaptation | Opponent modelling + adaptation alone is not new |
| Solving Repeated Games with Large Language Model (AAMAS 2026) | Reflective Hypothetical Mind, joint opponent modelling and adaptation | Do not propose a plain Reflection + Opponent Modelling architecture |
| CoopEval (2026) | Compares cooperation mechanisms: repeated games, reputation, mediation, contracts | Do not only compare which mechanism produces cooperation more easily |
| Generalizability of LLM-based Agents (2026) | Systematic survey of agent generalization and evaluation | Generalization itself is an established topic; the question must be more precise |
| Reward Hacking Benchmark (ICML 2026) | Systematic evaluation of reward exploitation by tool-using agents | Do not only design a few reward loopholes and count exploitation |

Note: this is a preliminary nearest-neighbour screen, not a complete systematic review, and it cannot by itself establish that a question is unstudied.

## Independent pre-screen (2026-11-17)

An independent Novelty Gate pre-screen of A1 returned **MODIFY**: the broad version of A1 is partly covered (fine-tuned cross-game transfer modelling; training-free reflection playbooks across social games; in-context negative transfer across game sequences), but no one has done the LO-EXP-001 cut — in-context G0–G4 memory conditions in repeated 2×2 games, with structural similarity as a continuous variable and Negative Transfer Rate / Adaptation Speed as the main metrics. The narrowed scope is recorded in the draft assessment shared with the team on 2026-11-17. This is a pre-screen, not a systematic review; residual risks are listed in that draft.
