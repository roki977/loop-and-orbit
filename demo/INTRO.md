# Interactive math reference platform — project introduction

**Role:** supporting reference artifact, not a research output.
**Added:** 2026-11-25.

## What this is

`demo/index.html` is a self-contained, bilingual (ZH/EN) interactive atlas of 41 mathematical ideas that recur in machine learning — from maximum likelihood estimation and Bayesian updating to diffusion models and self-play. It is a lightweight "look it up when you need it" platform: drag a slider, watch the plot change, then read the formula. Each module pairs a KaTeX equation with a live canvas, controls and numeric read-outs, a short explanation, prerequisite / next / related links, and at least one external reference. A 41-node / 47-bridge concept map and five guided learning paths connect the topics.

**Most of its content is general mathematical background, not this project's research focus.** Topics such as MLE, Bayes' theorem, KL divergence, the central limit theorem, PCA, gradient descent, bias–variance, or the Bellman equation are standard textbook material. This repository's research line remains the study of how general-purpose agents make decisions, form strategies, adapt to opponents, and fail in interactive game environments, as described in the root `README.md`. The atlas exists to make that literature and those experiments easier to read; it does not extend or represent them.

## What it is not

- **Not a research experiment, dataset, result, or publication claim.** No experiment record in `experiments/` backs any curve shown here.
- **Not a citable academic source.** References are orientation-grade (mostly Wikipedia, plus 10 primary papers whose arXiv IDs were verified). Follow the per-card link to the original source if you need to cite something.
- **Not uniformly empirical.** Several modules use closed-form illustrative curves instead of measured results; `REVIEW.md` documents which ones and why that matters.
- **Not a production web application.** It is a single 649 KB HTML file loading Tailwind, KaTeX, and Google Fonts from CDNs; there is no build step, offline fallback, or test suite.

## Who it is for

- Team members and readers who need a quick refresher on a formula or concept while reading a paper, a seminar note, or an experiment log.
- Onboarding and seminars: five learning paths run from basic to advanced, and the six group filters let a reader jump straight to a topic.
- Anyone who prefers intuition before notation.

It is a companion to `literature/` and `experiments/`, not a substitute for them.

## How to use it as a reference

1. Open `demo/index.html` in a browser (internet access required), then use **Language: EN** for English.
2. Locate a topic through the filter pills, a concept-map node, or a learning path.
3. Perturb the controls, then read the formula and the "Why it matters" note; follow the derivation bridges for the mathematical connection to neighbouring topics.
4. For anything you intend to cite, open the reference link and verify the primary source. Cite the source, not this atlas.

## Scope boundary

- **Facts (verified):** 41 cards, 47 derivation bridges, 59 external content links, zero runtime errors in a headless-browser smoke test; see `REVIEW.md` for the full method and results.
- **Judgement (assessment, not a research conclusion):** useful as a just-in-time intuition and revision aid; limited as a formal reference work.
- **Recommendation:** keep the atlas as a supporting companion. Any research claim must still trace to `experiments/` records and `literature/` sources, and pass the repository's Novelty Gate before adoption.

## Maintenance convention

`index.html` is kept byte-identical to the supplied artifact (SHA-256 recorded in `README.md`); positioning, usage, and evaluation live in separate documents: `INTRO.md` (this file), `README.md` (usage and limitations), and `REVIEW.md` (assessment). No fabricated citations, results, or benchmark numbers are introduced here.
