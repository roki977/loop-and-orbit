# Contribution Guide

## Workflow

Issue → Branch → Pull Request → Review → Merge.

- `main` is protected: no direct pushes; every change goes through a Pull Request; at least one member review is required before merging; AI agents cannot merge to `main`.
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
