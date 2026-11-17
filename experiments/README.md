# Experiments

- `experiment-registry.md` — every experiment, with status.
- `hypotheses/` — hypothesis records.
- `protocols/` — experiment protocols.
- `results/` — results, including negative results.
- One folder per experiment (`LO-EXP-XXX`), copied from `templates/experiment-template.md`.

## Rules

- Record the research question, hypothesis, variables, baselines, controls, metrics, random seeds, model and API versions, and cost estimate before running.
- Never invent results. Record negative and inconclusive results in full.
- Conclusions are labelled fact / hypothesis / recommendation and need human confirmation.
- Raw logs are kept in non-overwritable versions. Large data uses Git LFS or external storage; record version, checksum, and download instructions.
