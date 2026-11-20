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

# Standard labels, 2 target opponents, 5 seeds
python3 experiments/LO-EXP-001/pilot_v0.py \
  --backend openai_compat \
  --model deepseek-chat \
  --observability visible \
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

**Negative / Null Results Recorded Honestly:**
- **H2 on `G3` under `visible` + 5 seeds (`temperature = 0.3`) was NOT supported:** Although `G3` showed negative transfer in the single-seed `temperature = 0.0` probe (`1.200`), across 5 seeds at `temperature = 0.3` `G3` achieved `4.000` (5/5 adapted on Round 1) against both `tft_coop` and `always_a`.
- **Under `swap_target_labels = True`, negative transfer vanished completely for all conditions (`G0 = G1 = G3 = 4.000`, NTR = `0.00`).**

---

## Conclusions (labelled: fact / hypothesis / recommendation; human confirmation required)

- **Fact:** On `deepseek-flash` (`observability = visible`, `temperature = 0.3`, 5 seeds), raw history (`G1`) produced **100% negative transfer (5/5 seeds)** against both `tft_coop` (Full Payoff `1.280` vs `G0` `4.000`, `0/5` adapted) and `always_a` (Full Payoff `3.100` vs `G0` `4.000`, `1/5` adapted), whereas extracted rules (`G3`) showed **0% negative transfer** (`4.000`, `5/5` adapted).
- **Fact:** Swapping Game B action labels (`swap_target_labels = True`) eliminated `G1`'s negative transfer completely (`4.000`, `5/5` adapted for both opponents), while `G0` remained at `4.000` (ruling out a simple alphabetical preference for `"A"` in `G0`).
- **Interpretation / Hypothesis (to be tested further):**
  1. *Episodic Anchoring vs. Rule Abstraction:* Long raw transcripts (`G1`) appear to anchor the model strongly to the surface action symbol `"B"` from Session 1, overriding visible payoff-matrix reasoning; by contrast, distilled rules (`G3`) act as a softer prior that the model more readily overrides when the new payoff matrix is visible.
  2. *Surface Action-Label Binding:* The complete disappearance of `G1` negative transfer under label swapping suggests `G1`'s failure is driven primarily by literal symbol binding (`"B"` = safe) rather than abstract equilibrium-selection transfer (Risk-Dominance over Payoff-Dominance).
- **Recommendation (pending human team review):**
  1. Run the same 5-seed multi-opponent + label-swap protocol under `--observability hidden` to test whether `G3` also suffers negative transfer when the new payoff matrix is not directly visible.
  2. Replicate on at least one second model family (e.g., GPT / Claude / Qwen) and add a length-matched irrelevant-context control before drawing cross-model claims.
  3. Do not update `experiment-registry.md` or push experimental conclusions to `main` until the human team reviews these findings.
