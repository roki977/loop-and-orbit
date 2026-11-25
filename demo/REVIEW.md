# Review: Interactive Math Atlas Demo and Its Explanatory Apparatus

**Reviewed:** 2026-11-25
**Scope:** `demo/index.html` (single-file demo, 648,993 bytes, ~6,370 lines) - the teaching design, the explanations, the reference apparatus, and the implementation as it affects both.
**Method:** static source inspection; headless Chrome (Playwright) load, language toggle, slider/filter/node/edge interaction, and per-card DOM audit; HTTP status check of every unique external content link; arXiv metadata cross-check of all 10 cited papers.

This document follows the repository convention of separating **facts** (verified), **assessment** (judgement), and **recommendations** (not yet implemented). It evaluates a demo artifact; it is not a research result or a publication claim. Most of the mathematics covered here is general textbook background, not this repository's research focus; see `INTRO.md` for the scope boundary.

---

## 1. Facts (verified)

**Content and structure**

- 41 module cards in 6 groups, 41 canvases, 46 range sliders, 50 display-equation blocks, 59 external content links.
- Every card has a canvas, prerequisite / next / related navigation, and at least one reference link. 40 cards contain a rendered display formula; 25 contain a "Why it matters" prose block.
- Concept map: 41 nodes, 47 derivation bridges with KaTeX-formatted mathematical derivations. Five guided learning paths (A-E).
- Six category filter pills; a ZH/EN language toggle persisted in `localStorage`.

**Runtime behaviour (headless Chrome, 1440x900)**

- Zero page errors, zero uncaught exceptions. All 41 canvases were sized and drawn; 140 KaTeX elements rendered; filter G6 correctly showed 7 cards; node and edge selection produced bridge text with rendered math.
- EN toggle: document language switched to `en`, title changed, map labels translated, and **0 Chinese characters** remained in DOM `innerText`. Switching back restored Chinese.
- One console warning only: Tailwind Play CDN "should not be used in production".

**Reference apparatus**

- 59 unique external content links: 40 Wikipedia, 10 arXiv, 4 scikit-learn, 2 christophm.github.io (Interpretable ML book), plus numpy.org, XGBoost docs, and incompleteideas.net (Sutton & Barto).
- 58/59 returned HTTP 200 in this environment; `http://incompleteideas.net/book/the-book-2nd.html` timed out. This is a reachability observation, not proof the source is gone.
- All 10 arXiv IDs resolve to the exact papers named in the anchor text (e.g. 1706.03762 = *Attention Is All You Need*, 2006.11239 = *Denoising Diffusion Probabilistic Models*, 1707.06347 = *Proximal Policy Optimization Algorithms*). No fabricated citations were found.

**Implementation details that affect the explanation**

- No framework and no build step: vanilla JS, `<canvas>` with device-pixel-ratio scaling, KaTeX auto-render, Tailwind utility classes.
- Bilingual support is implemented as large ZH/EN phrase dictionaries plus substring replacement over DOM text nodes and canvas label strings, not as structured i18n message keys.
- Several curves are closed-form scripts rather than experiments: `agNoAug`, `agWithAug`, `trAcc`, `kfFoldScore`, `kfLeakScore`, `bgOOBErr`, `esCurves`, `spVsRandom`. The word 示意 ("schematic/illustrative") appears in 9 source lines.
- At 1440px, 6 cards in ZH mode and 3 in EN mode have display formulas wider than their container (SHAP, ReLU, Boosting among the EN cases). Card heights range 586-894 px.

---

## 2. Assessment

### What works well

**The pedagogy is genuinely well designed.** The stated rule - "drag the slider first, then read the formula" - is respected by the card layout: formula on top, live plot in the middle, controls and numeric readouts below, prose at the bottom. That ordering turns an abstract identity into something the reader can perturb, which is exactly the right sequence for building intuition. The live readouts tie the plot back to the symbols in the equation.

**The cross-topic scaffolding is unusual and valuable.** Most "41 concepts" explainers are flat lists. Here, 47 derivation bridges connect topics mathematically (MLE <-> KL, Gaussian prior <-> L2 ridge, KL non-negativity <-> ELBO, hinge loss + L2 <-> SVM), every card carries prerequisite/next/related links, and five learning paths give a reader a way in. This makes the artifact usable both as a reference to dip into and as a curriculum to work through.

**The explanations are concise and honest about caveats where they exist.** The "Why it matters" notes include genuinely useful warnings - log1p for zeros, target-encoding leakage, boosting reduces bias while bagging reduces variance, theoretical vs effective receptive field, "correlation is not causation" for mutual information. These are the mistakes learners actually make, so the notes earn their space.

**References are real and correctly matched.** Primary papers for the modern topics, canonical docs for the tooling ones, and a textbook for RL. Cross-checking arXiv IDs against titles found no mismatches. As an orientation aid, this is above average.

**It runs.** Zero runtime errors, all canvases drawn, both languages functional, interaction paths working. For a 650 KB hand-written single file, that is a solid engineering result.

### What holds it back as a teaching reference

**1. Mixed fidelity is under-disclosed (most important).** Roughly a third of the modules simulate behaviour with hand-written curves rather than computing it from data. That is a legitimate teaching simplification, but a reader cannot tell which plots are computed and which are scripted: "validation accuracy" curves are deterministic functions, yet they are presented in the same visual language as the real value-iteration grid or the posterior density. For a reference artifact, that distinction should be explicit on the card, not buried in the source.

**2. Explanatory depth is uneven.** Only 25 of 41 cards get a "Why it matters" paragraph. The remaining 16 rely on canvas annotations, which are fragments rather than connected prose. A reader following a learning path gets an inconsistent amount of context.

**3. The reference tier is orientation-grade, not citation-grade.** 40 of 59 links are Wikipedia; there are no inline citation anchors connecting a specific claim to a specific source, no access dates, no version or section references, and no "further reading" tier. The one textbook link uses plain HTTP and timed out here. Adequate for a first pass; not something to cite in a paper or a seminar reading list.

**4. The bilingual layer is brittle.** EN DOM text is fully translated, but canvas annotations are patched by phrase substitution, producing visible artifacts: "Random transitions: 80% 80% along the policy direction, 20% 20% sideways" (Bellman card), a stray "Â" in one dictionary entry, and "Why it matters:The" with no space. Any edit to a Chinese label can silently break its English counterpart. The translation mechanism, not the translation coverage, is the problem.

**5. Layout and responsive details.** `justify-between` inside equal-height grid rows leaves large blank bands in shorter cards (clearly visible on Attention and Bellman). Long formulas scroll horizontally within their box in 3-6 cards. The filter bar hides its scrollbar with no visual affordance, so the last group pill appears clipped. None of these break the demo, but they make a dense page feel less deliberate than its content deserves.

**6. Offline and maintenance risk.** Three remote CDNs must load; Tailwind Play CDN explicitly warns against production use. A 650 KB single file with all 41 modules in one script has no module boundaries and no automated test, so a small change to a shared helper (for example `setupCanvas` or the phrase dictionary) can affect every card without detection.

**7. Accessibility.** Plot content exists only as canvas pixels; there is no textual alternative, data table, or description for the visual explanation, so a screen reader gets the formula and controls but not the demonstration.

### Overall verdict

As an **intuition-building and revision tool** for a machine-learning course, a reading group, or self-study, this is excellent: broad, mathematically connected, interactive, and polished enough to use immediately. As a **reference work**, it is good for orientation and for finding the right primary source, but the mixed simulation fidelity, uneven prose, and missing citation discipline keep it below citable-article quality. As **production web code**, it is a prototype: replace the CDN dependencies before deploying it anywhere that matters.

The single highest-value improvement is not another module - it is a small label on each card saying whether the plot is computed or illustrative.

---

## 3. Recommendations (not implemented; the demo was kept byte-identical)

1. Add a per-card badge: "computed from data" vs "illustrative simulation", and name the seeded generator or analytic function used.
2. Write "Why it matters" notes for the remaining 16 cards; keep the existing caveat-first style.
3. Replace phrase-substitution i18n with structured message keys shared by DOM and canvas; add a smoke assertion that EN mode leaves no Chinese characters in either DOM text or canvas labels.
4. Fix the duplicated "80% 80%" / "20% 20%" annotation, the "Â" typo, and the missing space after "Why it matters:".
5. Wrap long display formulas or allow a full-width expandable view; remove `justify-between` on stretched cards; make the filter bar's horizontal scroll discoverable.
6. Add inline citation anchors (claim -> source), access dates, and one primary source per group; switch the textbook link to HTTPS or a stable archival URL.
7. Vendor or pin Tailwind/KaTeX/fonts with a local fallback so the atlas works offline; add a lightweight Playwright smoke test to CI.
8. Provide text alternatives (a short description or data table) for each canvas.

## 4. Open questions for the next iteration

- If a learner can freely distort an illustrative curve, does that build a correct mental model or a false sense of empirical evidence?
- Which of the 41 modules would actually benefit from real data rather than a closed-form simulation, and what would that cost in complexity?
- Should the concept map be derived from the card metadata instead of maintained as a separate 47-edge list, so the two cannot drift apart?
