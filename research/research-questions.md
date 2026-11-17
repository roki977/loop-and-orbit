# Research Questions

Status: candidates. The main line is **not decided**. A candidate is adopted only after it passes the Novelty Gate (`novelty-assessment.md`) and a human decision is recorded in `decision-log.md`.

## A1 — Cross-game strategy transfer (main-line candidate)

- **Question:** Under what conditions does a strategy learned in one game transfer to a structurally similar game, and when does transfer become negative transfer?
- **Sub-questions:**
  - A2 — What does adaptation cost, as an evaluation dimension?
  - A3 — Does memory help or limit transfer? (memory as a mechanism variable)
- **Pilot:** LO-EXP-001. H1: transfer helps. H2: negative transfer occurs. 4 games (Prisoner's Dilemma, Stag Hunt, Chicken, Battle of the Sexes); 5 experience conditions (G0–G4). Metrics: Adaptation Speed, Negative Transfer Rate.
- **Caution:** Models have seen these four games many times in training. A gain in game B may mean the model recognized the game, not that experience transferred. Mitigations: hide game names, use neutral action labels, parametrize payoff matrices (Robinson & Goforth's topology of 2×2 games) so structural similarity becomes a continuous variable. Start small: 2 games, 3 groups, 2 opponents.
- **Status:** candidate — pending Novelty Gate and human decision.

## Blank A — Internal board representation drift

- **Question:** Do a general LLM's internal board-state representations degrade as a game progresses, and can that drift explain illegal moves?
- **Method:** Probes on internal representations.
- **Status:** candidate — pending Novelty Gate and human decision.

## Notes

- Do not treat "general beats specialized" as an established hypothesis. Break it into falsifiable questions.
- Every question must state what is established, what is uncertain, and what would count as evidence against it.
