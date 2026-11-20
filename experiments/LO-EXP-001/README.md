# Experiment LO-EXP-001 (Pilot v0): Negative Transfer in Anonymized Repeated 2×2 Games

> **Status:** Pilot v0 initial runs completed on `deepseek-chat` (API response model: `deepseek-flash`), 2026-11-20. Pending human review before updating `experiment-registry.md` or merging to `main`.
> **Labels:** Statements below distinguish **Fact**, **Hypothesis**, **Interpretation**, and **Recommendation**.

| Field | Content |
|---|---|
| Research question (RQ) | **A1 / A3 (narrowed cut):** In anonymized repeated 2×2 games, when an LLM agent transitions from Game A to Game B, does carrying extracted strategic rules (`G3`) or raw history (`G1`) cause **negative transfer** (lower payoff / slower adaptation) relative to a blank-slate agent (`G0`) during the first $N$ rounds of Game B? |
| Hypothesis | **H1 (Positive Transfer):** Experience from Game A helps the agent adapt faster in Game B.<br>**H2 (Negative Transfer — primary target of Pilot v0):** When Game A induces a defensive rule that is suboptimal in Game B, `G3` (extracted rules) underperforms `G0` (no memory) in the early rounds of Game B and exhibits slower `adaptation_speed`. |
| Independent / dependent variables | **IVs:** Experience condition (`G0` no memory, `G1` full Game A transcript, `G3` model-extracted rules from Game A); Observability (`hidden` payoff matrix via feedback only vs. `visible` anonymized matrix).<br>**DVs:** Early-window mean payoff (first $N=5$ rounds of Game B), full-Game-B mean payoff, Transfer Gain ($\text{Payoff}_B(G_k) - \text{Payoff}_B(G_0)$), Negative Transfer Rate (fraction of seeds with $\text{Payoff}_B(G_k) < \text{Payoff}_B(G_0)$), Adaptation Speed (first round $t$ in Game B with 2 consecutive optimal actions), Token Usage, Parse Error Rate. |
| Baselines | `G0` (blank-slate agent entering Game B with zero history from Game A). |
| Controls | Anonymized labels (no game names; actions labelled `A` / `B`); fixed prompt template; fixed `max_tokens` per turn (`128`); fixed `temperature` (`0.0` default, or matched across groups when using `>0`); paired seeds and deterministic opponents across `G0 / G1 / G3`; immutable per-run raw logs. |
| Random seeds | Pilot v0 default: 5 seeds (`0, 1, 2, 3, 4`); expand to $\ge 10$ if a real signal appears. |
| Model and API versions | Any OpenAI-compatible chat model via `OPENAI_API_KEY` + `OPENAI_BASE_URL` (e.g., DeepSeek, OpenAI, OpenRouter, Gemini OpenAI-compat). Exact `model` string and API response `model` field are logged in `config.json` and `raw_events.jsonl`. |
| Estimated compute / cost | 3 groups × 5 seeds × (10 rounds A + 10 rounds B + 1 rule extraction for `G3`) ≈ 255 short API calls (~128 output tokens each) — typically < \$0.50 on standard API models. |
| How to reproduce | See Quick Start below. |

---

## Design Rationale (Recommendation)

1. **Why `PD (vs Always-B)` → `Stag Hunt (vs Tit-for-Tat)` by default?**
   - **Fact:** In iterated Prisoner's Dilemma against Tit-for-Tat, cooperation is often optimal — the same optimal action as in Stag Hunt or Harmony, which would confound tests of negative transfer.
   - **Recommendation:** In Pilot v0, Game A uses an anonymized Prisoner's Dilemma matrix against a stubborn `always_B` opponent (making `B` strictly optimal), and Game B switches to an anonymized Stag Hunt matrix (or Harmony via `--target-game harmony`) against a cooperative `tft_coop` opponent (making mutual `A` optimal, payoff `4` vs `1`). This cleanly separates whether `G3` over-commits to its extracted defensive rule.
2. **Why include `--observability hidden` vs `visible`?**
   - **Hypothesis:** Strong LLMs shown a full 2×2 payoff matrix may algebraically solve Game B on round 1 regardless of prior memory. Comparing `hidden` (bandit-like round feedback only) against `visible` tests whether negative transfer is driven by partial observability / opponent uncertainty or persists even with full matrix visibility.

---

## Quick Start

### 1. Pipeline smoke test (no API key, mock backend)
```bash
python3 experiments/LO-EXP-001/pilot_v0.py --backend mock --seeds 3 --rounds-a 6 --rounds-b 8
```
> Mock outputs are explicitly tagged `"backend": "mock"` and must **never** be cited as experimental results.

### 2. Real API run (OpenAI-compatible endpoint)
```bash
export OPENAI_API_KEY="your-key-here"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"   # or OpenAI / OpenRouter / Gemini compat URL

# Full 6-condition 2x2 mechanism decomposition (visible or hidden)
python3 experiments/LO-EXP-001/pilot_v0.py \
  --backend openai_compat \
  --model deepseek-chat \
  --observability visible \
  --conditions G0 G0_PAD G1_NO_PAYOFF G1_XY G1 G3 \
  --target-opps tft_coop always_a \
  --seeds 5 --temperature 0.3 \
  --rounds-a 10 --rounds-b 10 --early-window 5

# Label-swap ablation (add --swap-target-labels)
python3 experiments/LO-EXP-001/pilot_v0.py \
  --backend openai_compat \
  --model deepseek-chat \
  --observability visible \
  --target-opps tft_coop always_a \
  --swap-target-labels \
  --seeds 5 --temperature 0.3 \
  --rounds-a 10 --rounds-b 10 --early-window 5
```

### Output Layout (Non-Overwritable)
Each run creates a new timestamped directory under `experiments/LO-EXP-001/runs/<run_id>/` (refuses to overwrite existing runs):
- `config.json` — full hyperparameters, game matrices, opponent policies, git commit hash
- `raw_events.jsonl` — every prompt, raw LLM response, parsed action, payoff, and token count
- `summary.json` & `summary.csv` — per-condition metrics (`early_payoff_B`, `mean_payoff_B`, `transfer_gain`, `negative_transfer_rate`, `adaptation_speed`, token usage, parse errors)

---

## Results (including negative results)

All runs below used `source_game = pd (vs always_b)` → `target_game = stag_hunt`, `rounds_a = 10`, `rounds_b = 10`, `early_window = 5`, `max_tokens = 128`, requested model `deepseek-chat` (API `response_model = deepseek-flash`), and recorded **0 parse errors** across all conditions. Raw logs are stored locally under `experiments/LO-EXP-001/runs/` (not pushed to `main` per SD-006).

### Run Set A — Initial Single-Seed Exploratory Probes (`temperature = 0.0`, `seeds = 1`, `target_opp = tft_coop`)

- `20261120T070127Z_openai_compat_deepseek-chat_hidden` (`observability = hidden`, `swap = False`):
  - `G0`: Early(5) = `4.000`, Full = `4.000`, Adapt Round = `1.00 (1/1)`
  - `G1`: Early(5) = `1.400` (`-2.600`), Full = `1.200`, Adapt Round = `11.00 (0/1)`
  - `G3`: Early(5) = `1.600` (`-2.400`), Full = `1.300`, Adapt Round = `11.00 (0/1)`
- `20261120T070342Z_openai_compat_deepseek-chat_visible` (`observability = visible`, `swap = False`):
  - `G0`: Early(5) = `4.000`, Full = `4.000`, Adapt Round = `1.00 (1/1)`
  - `G1`: Early(5) = `1.400` (`-2.600`), Full = `1.200`, Adapt Round = `11.00 (0/1)`
  - `G3`: Early(5) = `1.400` (`-2.600`), Full = `1.200`, Adapt Round = `11.00 (0/1)`

### Run Set B — 5-Seed Multi-Opponent & Label-Swap Ablation (`observability = visible`, `temperature = 0.3`, `seeds = 5`)

- **Standard labels (`swap_target_labels = False`)** — `run_id: 20261120T071731Z_openai_compat_deepseek-chat_visible`
- **Swapped labels (`swap_target_labels = True`)** — `run_id: 20261120T072449Z_openai_compat_deepseek-chat_visible_swapped`

| Label Setting | Target Opp | Cond | Early(5) Payoff | Early Gain | Early NTR | Full Payoff | Full Gain | Adapt Round | Parse Err |
|---|---|---|---|---|---|---|---|---|---|
| Standard (`swap=False`) | `tft_coop` | `G0` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Standard (`swap=False`) | `tft_coop` | `G1` | **1.560** | **-2.440** | **1.00** | **1.280** | **-2.720** | **11.00 (0/5)** | 0 |
| Standard (`swap=False`) | `tft_coop` | `G3` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Standard (`swap=False`) | `always_a` | `G0` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Standard (`swap=False`) | `always_a` | `G1` | **3.000** | **-1.000** | **1.00** | **3.100** | **-0.900** | **10.00 (1/5)** | 0 |
| Standard (`swap=False`) | `always_a` | `G3` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Swapped (`swap=True`) | `tft_coop` | `G0` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Swapped (`swap=True`) | `tft_coop` | `G1` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Swapped (`swap=True`) | `tft_coop` | `G3` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Swapped (`swap=True`) | `always_a` | `G0` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Swapped (`swap=True`) | `always_a` | `G1` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| Swapped (`swap=True`) | `always_a` | `G3` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |

### Run Set C — 6-Condition $2 \times 2$ Mechanism Decomposition: `visible` vs `hidden` (`temperature = 0.3`, `seeds = 5`)

Conditions decompose **context length**, **surface action-label overlap (`A/B`)**, and **payoff/experience content**:
- `G0`: No memory baseline
- `G0_PAD`: Length-matched unrelated archival log (controls for prompt length without `A/B` or payoff content)
- `G1_NO_PAYOFF`: Action sequence from Game A with payoffs stripped (surface `A/B` symbols only)
- `G1_XY`: Full Game A transcript with actions renamed `A → X, B → Y` (payoff experience without `A/B` symbol overlap)
- `G1`: Full Game A transcript (`A/B` symbols + payoffs)
- `G3`: Model-extracted strategic rules from Game A

- **`visible` run** — `run_id: 20261120T122742Z_openai_compat_deepseek-chat_visible`
- **`hidden` run** — `run_id: 20261120T124220Z_openai_compat_deepseek-chat_hidden`

| Observability | Target Opp | Cond | Early(5) Payoff | Early Gain | Early NTR | Full Payoff | Full Gain | Adapt Round | Parse Err |
|---|---|---|---|---|---|---|---|---|---|
| `visible` | `tft_coop` | `G0` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `visible` | `tft_coop` | `G0_PAD` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `visible` | `tft_coop` | `G1_NO_PAYOFF` | **1.440** | **-2.560** | **1.00** | **1.260** | **-2.740** | **11.00 (0/5)** | 0 |
| `visible` | `tft_coop` | `G1_XY` | 3.800 | -0.200 | 0.20 | 3.900 | -0.100 | 1.20 (5/5) | 0 |
| `visible` | `tft_coop` | `G1` | **1.640** | **-2.360** | **1.00** | **1.620** | **-2.380** | **9.40 (1/5)** | 0 |
| `visible` | `tft_coop` | `G3` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `visible` | `always_a` | `G0` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `visible` | `always_a` | `G0_PAD` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `visible` | `always_a` | `G1_NO_PAYOFF` | **3.000** | **-1.000** | **1.00** | **3.000** | **-1.000** | **11.00 (0/5)** | 0 |
| `visible` | `always_a` | `G1_XY` | 3.960 | -0.040 | 0.20 | 3.980 | -0.020 | 1.20 (5/5) | 0 |
| `visible` | `always_a` | `G1` | **3.000** | **-1.000** | **1.00** | **3.000** | **-1.000** | **11.00 (0/5)** | 0 |
| `visible` | `always_a` | `G3` | 3.760 | -0.240 | 0.40 | 3.780 | -0.220 | 3.20 (4/5) | 0 |
| `hidden` | `tft_coop` | `G0` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `hidden` | `tft_coop` | `G0_PAD` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `hidden` | `tft_coop` | `G1_NO_PAYOFF` | **1.520** | **-2.480** | **1.00** | **1.300** | **-2.700** | **11.00 (0/5)** | 0 |
| `hidden` | `tft_coop` | `G1_XY` | **2.000** | **-2.000** | **0.80** | **1.800** | **-2.200** | **9.00 (1/5)** | 0 |
| `hidden` | `tft_coop` | `G1` | **1.440** | **-2.560** | **1.00** | **1.220** | **-2.780** | **11.00 (0/5)** | 0 |
| `hidden` | `tft_coop` | `G3` | **1.600** | **-2.400** | **1.00** | **1.300** | **-2.700** | **11.00 (0/5)** | 0 |
| `hidden` | `always_a` | `G0` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `hidden` | `always_a` | `G0_PAD` | 4.000 | +0.000 | 0.00 | 4.000 | +0.000 | 1.00 (5/5) | 0 |
| `hidden` | `always_a` | `G1_NO_PAYOFF` | **3.240** | **-0.760** | **1.00** | **3.320** | **-0.680** | **7.80 (2/5)** | 0 |
| `hidden` | `always_a` | `G1_XY` | 3.760 | -0.240 | 0.40 | 3.780 | -0.220 | 3.20 (4/5) | 0 |
| `hidden` | `always_a` | `G1` | **3.000** | **-1.000** | **1.00** | **3.000** | **-1.000** | **11.00 (0/5)** | 0 |
| `hidden` | `always_a` | `G3` | 3.560 | -0.440 | 1.00 | 3.780 | -0.220 | 3.20 (5/5) | 0 |

**Negative / Null Results Recorded Honestly:**
- **Prompt length alone had zero effect:** `G0_PAD` achieved `4.000` (5/5 adapted on Round 1) across all 4 `(observability, opponent)` cells.
- **Under `visible` + 5 seeds (`temperature = 0.3`), `G3` largely avoided negative transfer** (`4.000`, 5/5 on `tft_coop`; `3.780`, 4/5 on `always_a`), contrasting with the single-seed `temperature = 0.0` probe (`1.200`) and demonstrating why fixed temperature and multi-seed evaluation are mandatory.
- **Under `swap_target_labels = True` (`visible`), negative transfer vanished completely for all conditions (`G0 = G1 = G3 = 4.000`, NTR = `0.00`).**

---

## Conclusions (labelled: fact / hypothesis / recommendation; human confirmation required)

- **Fact:** Across both `visible` and `hidden` modes on `deepseek-flash` (`temperature = 0.3`, 5 seeds), length-matched irrelevant padding (`G0_PAD`) produced **0% negative transfer** (`4.000`, 5/5), ruling out pure context-length distraction.
- **Fact (Double Dissociation across Observability):**
  1. **When the payoff matrix is `visible`:** Raw action history (`G1`: `1.620`, 1/5 on `tft_coop`; `3.000`, 0/5 on `always_a`) and payoff-stripped action sequences (`G1_NO_PAYOFF`: `1.260`, 0/5 on `tft_coop`; `3.000`, 0/5 on `always_a`) both induced severe negative transfer, whereas renaming prior actions to `X/Y` (`G1_XY`: `3.900`, 5/5; `3.980`, 5/5) and rule abstraction (`G3`: `4.000`, 5/5; `3.780`, 4/5) nearly eliminated it.
  2. **When the payoff matrix is `hidden`:** Both `G1_XY` (`1.800`, 1/5 on `tft_coop`) and `G3` (`1.300`, 0/5 on `tft_coop`) also suffered severe negative transfer against `tft_coop`, and exhibited delayed adaptation (`3.20` rounds) against `always_a` (while `G1` remained completely locked at `3.000`, 0/5 even against `always_a`).
- **Interpretation / Hypothesis (to be tested across models and games):**
  1. *Surface Action-Label Anchoring (`visible`):* Under transparent payoffs, `G1`'s negative transfer is driven primarily by literal symbol co-occurrence (`"B"`), not payoff-derived strategy — proved by `G1_NO_PAYOFF` matching `G1`'s failure and `G1_XY` almost fully rescuing performance.
  2. *Analogical / Rule-Level Negative Transfer (`hidden`):* When the target payoff table is hidden, raw logs show `G1_XY` explicitly mapping the second symbol (`Y`) analogically to the second action (`B`) in Session 2, and `G3` following its extracted rule — producing beyond-surface negative transfer when coordination with `tft_coop` is required.
- **Scope Limitations (Fact):** All results so far come from **one model (`deepseek-flash`)**, **one game pair (`PD → Stag Hunt`)**, and **5 seeds per cell**. No cross-model or general claim is justified yet.
- **Recommendation (pending human team review):**
  1. Replicate Run Set C (`visible` + `hidden`, 6 conditions) on at least **one second model family** (e.g., GPT / Claude / Qwen) and expand to $\ge 10$ seeds.
  2. Expand game pairs (e.g., Harmony, Chicken, reverse direction cooperative → adversarial) and add a mid-session regime-switching opponent for A2 adaptation cost.
  3. Complete nearest-neighbour entries in `literature/literature-matrix.csv` before updating `experiment-registry.md` or merging to `main`.
