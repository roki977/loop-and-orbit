# Governance (working draft)

> Working draft. The full Governance Charter v1.0 is being finalized; this file records the decisions already confirmed. Do not treat this file as the Charter itself.

## Organization

- **Type:** Independent research organization.
- **Repositories:** Mixed openness — the knowledge base is public; unpublished research and sensitive experiments stay private for now.
- **Publishing:** Selective — WeChat articles are curated, not automatic.

## Decision authority

- Final research decisions are made by human members.
- The AI research commander handles research planning, literature surveys, critical review, and experiment-design suggestions. It holds no legal identity, no voting rights, and no asset ownership.

## Change control

- Important document changes go through a pull request with human review.
- AI contributors do not merge to `main` directly, do not change core hypotheses on their own, and do not delete raw data.
- Research-direction changes, final experimental conclusions, and publication claims require human approval.

## Secrets and data

- API keys live in environment variables or GitHub Secrets only. Never commit them.
- Raw experiment logs are kept in non-overwritable versions.
- Large data uses Git LFS or external storage; record version, checksum, and download instructions in the repo.

## Academic integrity

The following are not acceptable: selective reporting (reporting only favourable results while hiding important counterexamples), citation fabrication, and misleading visualization.
