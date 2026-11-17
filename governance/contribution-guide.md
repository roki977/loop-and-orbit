# Contribution Guide

## Workflow

Issue → Branch → Pull Request → Review → Merge — or, for routine changes, a direct push to `main` by Muse with team approval (SD-006, 2026-11-17).

- Significant changes (research direction, core hypotheses, publication claims) go through a Pull Request with member review.
- Experiment results and data files are not pushed directly to `main`.
- Every merge has a clear commit message.

## Task board

Loop & Orbit Research Board: Backlog → Literature Review → Research Design → AI Execution → Human Review → Completed.

## Division of labour

Shared, not fixed: everyone understands the whole project; no one works only on what they are already good at; tasks rotate, but every task has an owner responsible for its result. Research judgement cannot be outsourced to AI.

## Secrets and data

- API keys live in environment variables or GitHub Secrets only. Never commit them.
- Raw experiment logs are kept in non-overwritable versions.
- Large data uses Git LFS or external storage; record version, checksum, and download instructions.
