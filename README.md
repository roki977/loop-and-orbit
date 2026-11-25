# Loop & Orbit — Research Hub

Research hub for studying how general-purpose agents make decisions, form strategies, adapt to opponents, and fail in interactive environments. The main instrument is games: they provide a controlled setting for observing decision-making, memory, planning, and adaptation, and a bridge toward embodied settings.

A supporting interactive math reference platform lives in `demo/`: it is a just-in-time companion for looking up general mathematical background behind the literature, and is not part of the research line described below.

## Status

The main research line is **not yet decided**. Current candidates (see `research/research-questions.md`, from the planning conversation, 2026-11-17):

- **A — Strategy formation and opponent adaptation.** How does a general LLM agent form a strategy from an opponent's history, and can it adapt in time when the opponent changes strategy?
- **B — Reward vs. true goals.** Does a high reward mean the agent actually completed the task? (Reward hacking, specification gaming.)
- **C — General strategy transfer.** Can decision experience learned in one game help in an unfamiliar game?
- **D — What are agent scaffolds for?** When do planning, memory, reflection, and opponent modelling help?
- **E — Multi-agent games and cooperation.** What cooperation, competition, coordination, and group behaviour emerge when several general agents interact?

Preferred main-line candidate: **A1 — conditions and boundaries of cross-game strategy transfer**, with A2 (cost of adaptation) as an evaluation dimension and A3 (memory helps or hurts) as a mechanism variable. Every candidate must pass the Novelty Gate (`research/novelty-assessment.md`) before it is adopted.

## Structure

```
governance/    Decision rules, AI agent charter, contribution guide, decision log
research/      Research questions, research map, novelty assessments, open problems, ideas
literature/    Bibliography, literature matrix, reading notes, related work
experiments/   Registry, hypotheses, protocols, results (one folder per experiment)
seminars/      Weekly seminar notes (week-01, week-02, ...)
publications/  Papers, technical reports, WeChat articles (drafts / published / archive)
notebooks/     Colab notebooks (T4), named after their experiment
templates/     Canonical templates (paper reading, experiment, meeting minutes, research idea)
demo/          Supporting interactive math reference platform (standalone HTML + docs)
```

## Interactive math atlas demo (supporting reference platform)

**Positioning:** this directory is a companion for looking up and building intuition about mathematical background, not part of the research line described above. Most of its 41 modules cover general, textbook-level principles (maximum likelihood, Bayes, KL divergence, PCA, gradient descent, Bellman equations, and so on); they are included so that papers, seminar notes, and experiment logs are easier to read. Nothing here is a research result, a dataset, or a publication claim, and the atlas is not a citable source for research conclusions.

`demo/index.html` is a standalone, bilingual interactive atlas of 41 mathematical ideas behind machine learning, from maximum likelihood estimation to self-play. It contains 41 live canvas modules, a 41-node / 47-bridge concept map with derivation formulas, five guided learning paths, and per-card references. Open the file directly in a browser (CDN access required) or serve the folder locally; use the **Language: EN** button for English.

Documentation: `demo/INTRO.md` explains the project's role and scope boundary; `demo/README.md` covers how to run it and its known limitations; `demo/REVIEW.md` is an assessment of the demo and its explanatory/reference apparatus, with verified facts, judgements, and recommendations kept separate. The demo file is kept byte-identical to the supplied artifact; no research claims are made from it.

## Working rules

1. **No fabrication.** No invented papers, citations, results, or benchmark numbers. Every citation must be verifiable; every result must trace to an experiment record.
2. **Check prior work first.** Before proposing a question, search directly related and neighbouring work and record what is established and what is still open.
3. **Label facts, hypotheses, and recommendations.** Keep them distinct in every document.
4. **Report negative and inconclusive results honestly.** A null result is a result.
5. **Humans decide.** Changes of research direction, final experimental conclusions, and any public claim require human approval.
6. **Routine changes may be pushed directly to `main` by Muse with team approval (SD-006).** Research-direction changes, core-hypothesis changes, and publication claims still require human approval first. AI contributors do not change core hypotheses on their own and do not delete raw data.
7. **Secrets stay out of the repo.** API keys live in environment variables or GitHub Secrets only — never commit them. Raw experiment logs are kept in non-overwritable versions; large data uses Git LFS or external storage, with version, checksum, and download instructions recorded here.
