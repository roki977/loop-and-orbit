# Research Questions

Status: candidates. The main line is **not decided**. A candidate is adopted only after it passes the Novelty Gate (`novelty-assessment.md`) and a human decision is recorded in `governance/decision-log.md`.

## Five candidate directions (2026-11-17)

### A — Strategy formation and opponent adaptation (first choice)

- **Question:** How does a general LLM agent form a strategy from an opponent's history, and can it adapt in time when the opponent changes strategy?
- **Topics:** Cooperation vs. defection; opponent modelling; strategy adaptation; memory and history.

### B — Reward vs. true goals (second choice)

- **Question:** Does a high reward mean the agent actually completed the task?
- **Topics:** Reward hacking; specification gaming; reward robustness; verifiable vs. non-verifiable feedback.

### C — General strategy transfer

- **Question:** Can decision experience learned in one game help in an unfamiliar game?
- **Topics:** Cross-game transfer; strategy reuse; generalization; zero-shot vs. few-shot adaptation.

### D — What are agent scaffolds for?

- **Question:** When do planning, memory, reflection, and opponent modelling help?
- **Topics:** Ablation studies; planning vs. direct response; memory quality; reflection cost-effectiveness.

### E — Multi-agent games and cooperation

- **Question:** What cooperation, competition, coordination, and group behaviour emerge when several general agents interact?
- **Topics:** Emergent cooperation; coordination; multi-agent dynamics; communication protocols.

## Preferred focus: A1 / A2 / A3

- **A1 — Conditions and boundaries of strategy transfer (main-line candidate).** *When Does Strategic Knowledge Transfer Across Games?* Not whether an agent can learn to cooperate in one game, but when experience formed in game X helps it decide better in game Y: games sharing similar strategy structure but different surface rules; opponent behaviour distributions changing; reward structures changing; memory helping or causing negative transfer.
- **A2 — The cost of adaptation (evaluation dimension).** *The Cost of Strategic Adaptation.* What does adaptation cost in extra reasoning, calls, memory, and interaction? Adaptation speed, API token cost, strategy stability, forgetting old opponents, overreacting to new ones.
- **A3 — Memory helps or hurts (mechanism variable).** *When Does Memory Help or Hurt Agent Decisions?* Compare no memory, full history, summarized memory, strategic memory, stale memory. The point is not to prove memory useful again, but to find the conditions under which it hurts.

## Pilot: LO-EXP-001

- **Question:** Can agents transfer strategic knowledge across games?
- **H1:** Experience accumulated in game A helps an LLM agent form an effective strategy faster in a structurally similar but different game B.
- **H2 (competing):** Past experience causes negative transfer — the agent over-relies on old strategies and performs worse in the new environment.
- **Games:** Prisoner's Dilemma, Stag Hunt, Chicken, Battle of the Sexes.
- **Experience conditions:** G0 no history; G1 full history; G2 text summary of past experience; G3 strategy rules extracted from past experience; G4 past experience + current opponent information.
- **Metrics:** Average Payoff, Transfer Gain, Negative Transfer Rate, Adaptation Speed, Strategy Consistency, API Cost. Watch Adaptation Speed and Negative Transfer Rate most closely.
- **Controls:** fixed model version, prompt, token budget, opponent strategy, payoff matrix, number of rounds; multiple random seeds; paired opponents and environments across groups; equal-budget comparisons (extra reasoning tokens must not masquerade as a memory advantage).

## Cautions

- Models have seen these four games many times in training. A gain in game B may mean the model recognized the game, not that experience transferred. Mitigations: hide game names, use neutral action labels, parametrize payoff matrices (Robinson & Goforth's topology of 2×2 games) so structural similarity becomes a continuous variable. Start small: 2 games, 3 groups, 2 opponents.
- Do not treat "general beats specialized" as an established hypothesis. Break it into falsifiable questions.
- Every question must state what is established, what is uncertain, and what would count as evidence against it.
