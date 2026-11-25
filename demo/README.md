# Interactive Math Atlas Demo

A zero-build, single-file interactive atlas of 41 mathematical ideas behind machine learning, from maximum likelihood estimation to self-play. This directory contains the demo **unchanged** from the supplied artifact (`Loop & Orbit.html`, copied here as `index.html`), plus documentation.

- **Open it:** double-click `demo/index.html`, or serve the folder locally with `python3 -m http.server 8000` and visit `http://localhost:8000/demo/`.
- **Language:** the page starts in Chinese. Use the **Language: EN** button in the header to switch to English; the choice is remembered in `localStorage`.
- **Internet required:** Tailwind CSS (Play CDN), KaTeX 0.16.11, and Google Fonts are loaded from CDNs. There is no build step, no package manager, and no local asset bundle.
- **Integrity:** `index.html` is byte-identical to the source file (648,993 bytes; SHA-256 `ca412d3cfe60af40daf1a3aac1fda486c1752f503b8c9245fd9720fcac3dd826`).

## What is in the page

| Layer | Content |
| --- | --- |
| 41 module cards | Six groups: foundations (8), models (7), training & generalisation (9), interpretability (3), vision & modern architectures (7), decision making & RL (7). Each card has a KaTeX formula, a live Retina-aware canvas, controls, prerequisite / next / related links, and at least one external reference. |
| Concept map | 41 clickable nodes and 47 "derivation bridges" (edges). Selecting a node highlights upstream/downstream dependencies; selecting an edge shows a mathematical equivalence with rendered formulas. |
| Learning paths | Five guided routes (A-E) that chain modules from basic to advanced, with jump-to-card buttons. |
| Interactions | 46 range sliders, canvas click targets, step/animate buttons, live numerical readouts, and a category filter bar. |
| Bilingual layer | A ZH/EN phrase dictionary applied to DOM text, map labels, and canvas annotations. |

Most modules compute real quantities (Beta-Binomial posterior via a Lanczos log-gamma, ridge regression via a linear solve, SVM margin optimisation, Shapley values, Bellman value iteration, Q-learning, diffusion score fields, and more). Some modules deliberately use **illustrative analytic curves** instead of training a model; see `REVIEW.md`.

## Documentation

- `REVIEW.md` - an English assessment of the demo and of its explanatory/reference apparatus, separated into verified facts, judgements, and recommendations.
- `index.html` - the demo itself. Intentionally not reformatted or refactored.

## Known limitations (summary)

1. Remote CDN dependencies (Tailwind Play CDN warns that it is not for production use) mean the page is not offline-safe.
2. The English layer is a phrase-substitution dictionary, so a few canvas annotations contain duplicated or garbled fragments (for example "80% 80% ... 20% 20%" in the Bellman card).
3. Several long display formulas overflow horizontally on narrow cards; shorter cards show large empty bands because `justify-between` stretches them to the tallest card in the row.
4. Synthetic curves are not consistently labelled as illustrative, and 16 of 41 cards have no "Why it matters" prose block.
5. References are orientation-grade: mostly Wikipedia entries plus 10 verified primary arXiv papers, without inline citation anchors, access dates, or versioning.

These are observations about the artifact, not research conclusions. They are documented so the demo can be improved without changing its content.
