# Loop & Orbit — Research Hub

Research hub for studying how general-purpose agents make decisions, form strategies, adapt to opponents, and fail in interactive environments. The main instrument is games: they provide a controlled setting for observing decision-making, memory, planning, and adaptation, and a bridge toward embodied settings.

## Status

The main research line is **not yet decided**. Current candidates (see `research/research-questions.md`):

- **A1 — Cross-game strategy transfer.** Can a strategy learned in one game transfer to a structurally similar game? Under what conditions does transfer help, and when does it become negative transfer?
- **Blank A — Internal board representation drift.** Do a general LLM's internal board-state representations degrade over a game, and can that drift explain illegal moves? (probe-based)

Every candidate must pass the Novelty Gate (`research/novelty-assessment.md`) before it is adopted: check the closest prior work first, and do not claim novelty without evidence.

## Structure

```
governance/    Decision rules, roles, and publication policy
research/      Research questions, research map, novelty assessments, open problems, ideas, literature
experiments/   One folder per experiment (LO-EXP-XXX), copied from templates/
seminars/      Weekly seminar notes (week-01, week-02, ...)
publications/  Papers (workshop drafts) and WeChat articles (drafts / published)
notebooks/     Colab notebooks (T4), named after their experiment
templates/     Canonical templates (paper reading, experiment, meeting minutes)
decision-log.md  Record of decisions, with date, context, and status
```

## Working rules

1. **No fabrication.** No invented papers, citations, results, or benchmark numbers. Every citation must be verifiable; every result must trace to an experiment record.
2. **Check prior work first.** Before proposing a question, search directly related and neighbouring work and record what is established and what is still open.
3. **Label facts, hypotheses, and recommendations.** Keep them distinct in every document.
4. **Report negative and inconclusive results honestly.** A null result is a result.
5. **Humans decide.** Changes of research direction, final experimental conclusions, and any public claim require human approval.
6. **Important document changes go through a pull request.** AI contributors do not merge to `main` directly, do not change core hypotheses on their own, and do not delete raw data.
7. **Secrets stay out of the repo.** API keys live in environment variables or GitHub Secrets only — never commit them. Raw experiment logs are kept in non-overwritable versions; large data uses Git LFS or external storage, with version, checksum, and download instructions recorded here.
