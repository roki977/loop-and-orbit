# Loop & Orbit — Research Hub

Research hub for studying how general-purpose agents make decisions, form strategies, adapt to opponents, and fail in interactive environments. The main instrument is games: they provide a controlled setting for observing decision-making, memory, planning, and adaptation, and a bridge toward embodied settings.

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
```

## Working rules

1. **No fabrication.** No invented papers, citations, results, or benchmark numbers. Every citation must be verifiable; every result must trace to an experiment record.
2. **Check prior work first.** Before proposing a question, search directly related and neighbouring work and record what is established and what is still open.
3. **Label facts, hypotheses, and recommendations.** Keep them distinct in every document.
4. **Report negative and inconclusive results honestly.** A null result is a result.
5. **Humans decide.** Changes of research direction, final experimental conclusions, and any public claim require human approval.
6. **Important document changes go through a pull request.** AI contributors do not merge to `main` directly, do not change core hypotheses on their own, and do not delete raw data.
7. **Secrets stay out of the repo.** API keys live in environment variables or GitHub Secrets only — never commit them. Raw experiment logs are kept in non-overwritable versions; large data uses Git LFS or external storage, with version, checksum, and download instructions recorded here.
