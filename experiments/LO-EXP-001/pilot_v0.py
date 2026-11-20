#!/usr/bin/env python3
"""
LO-EXP-001 Pilot v0: Minimal Cross-Game Negative Transfer Runner.

Tests whether carrying prior game history (G1) or extracted strategy rules (G3)
from anonymized Game A causes negative transfer in anonymized Game B compared to
a blank-slate baseline (G0).

Zero third-party dependencies (Python 3 standard library only).
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import json
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Anonymized 2x2 Games (Actions are strictly "A" and "B"; no game names shown)
# Payoff dict maps (agent_action, opponent_action) -> (agent_payoff, opp_payoff)
# ---------------------------------------------------------------------------

GAMES: dict[str, dict[str, Any]] = {
    "pd": {
        "internal_name": "prisoners_dilemma",
        "payoffs": {
            ("A", "A"): (3, 3),
            ("A", "B"): (0, 5),
            ("B", "A"): (5, 0),
            ("B", "B"): (1, 1),
        },
    },
    "stag_hunt": {
        "internal_name": "stag_hunt",
        "payoffs": {
            ("A", "A"): (4, 4),
            ("A", "B"): (0, 3),
            ("B", "A"): (3, 0),
            ("B", "B"): (1, 1),
        },
        "target_optimal_action": "A",
    },
    "harmony": {
        "internal_name": "harmony",
        "payoffs": {
            ("A", "A"): (4, 4),
            ("A", "B"): (2, 3),
            ("B", "A"): (3, 2),
            ("B", "B"): (1, 1),
        },
        "target_optimal_action": "A",
    },
    "chicken": {
        "internal_name": "chicken",
        "payoffs": {
            ("A", "A"): (3, 3),
            ("A", "B"): (1, 4),
            ("B", "A"): (4, 1),
            ("B", "B"): (0, 0),
        },
        "target_optimal_action": "A",
    },
}


# ---------------------------------------------------------------------------
# Deterministic Opponent Policies
# ---------------------------------------------------------------------------

def opp_always_b(history: list[dict[str, Any]]) -> str:
    return "B"


def opp_always_a(history: list[dict[str, Any]]) -> str:
    return "A"


def opp_tft_coop(history: list[dict[str, Any]]) -> str:
    if not history:
        return "A"
    return history[-1]["agent_action"]


def opp_tft_defect(history: list[dict[str, Any]]) -> str:
    if not history:
        return "B"
    return history[-1]["agent_action"]


def opp_grim_trigger(history: list[dict[str, Any]]) -> str:
    if any(h["agent_action"] == "B" for h in history):
        return "B"
    return "A"


OPPONENTS: dict[str, Callable[[list[dict[str, Any]]], str]] = {
    "always_b": opp_always_b,
    "always_a": opp_always_a,
    "tft_coop": opp_tft_coop,
    "tft_defect": opp_tft_defect,
    "grim_trigger": opp_grim_trigger,
}


# ---------------------------------------------------------------------------
# LLM Backends
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class LLMResponse:
    content: str
    prompt_tokens: int
    completion_tokens: int
    response_model: str
    latency_s: float


class OpenAICompatClient:
    """Minimal OpenAI-compatible /chat/completions client using urllib."""

    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str,
        temperature: float = 0.0,
        max_tokens: int = 128,
        timeout_s: int = 60,
        max_retries: int = 3,
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        cafile = ssl.get_default_verify_paths().cafile
        if not cafile and Path("/etc/ssl/cert.pem").is_file():
            self.ssl_context = ssl.create_default_context(cafile="/etc/ssl/cert.pem")
        else:
            self.ssl_context = ssl.create_default_context()

    def chat(self, system_prompt: str, user_prompt: str, seed: int | None = None) -> LLMResponse:
        url = f"{self.base_url}/chat/completions"
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if seed is not None:
            payload["seed"] = seed

        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        last_err: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            t0 = time.time()
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=self.timeout_s, context=self.ssl_context) as resp:
                    raw = json.loads(resp.read().decode("utf-8"))
                latency = time.time() - t0
                content = raw["choices"][0]["message"]["content"]
                usage = raw.get("usage", {})
                return LLMResponse(
                    content=content,
                    prompt_tokens=int(usage.get("prompt_tokens", 0)),
                    completion_tokens=int(usage.get("completion_tokens", 0)),
                    response_model=str(raw.get("model", self.model)),
                    latency_s=round(latency, 4),
                )
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, KeyError) as exc:
                last_err = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * attempt)
        raise RuntimeError(f"API call failed after {self.max_retries} attempts: {last_err}")


class MockClient:
    """
    Deterministic mock backend ONLY for verifying pipeline, logging, and metrics.
    Simulates a sticky rule-follower under G3 vs a faster explorer under G0.
    """

    def __init__(self, model: str = "mock-v0") -> None:
        self.model = model

    def chat(self, system_prompt: str, user_prompt: str, seed: int | None = None) -> LLMResponse:
        # Rule extraction step
        if "EXTRACT_RULES_TASK" in system_prompt:
            return LLMResponse(
                content=(
                    "- Rule 1: The other player consistently selects B.\n"
                    "- Rule 2: Choosing A yields 0 payoff; always choose B to avoid exploitation."
                ),
                prompt_tokens=len(user_prompt) // 4,
                completion_tokens=28,
                response_model=self.model,
                latency_s=0.001,
            )

        # Parse current round number in the active game from prompt
        m_round = re.search(r"Current round:\s*(\d+)", user_prompt)
        curr_round = int(m_round.group(1)) if m_round else 1
        has_rules = "Extracted strategy rules from a previous session" in user_prompt
        has_prev_history = "Full transcript from a previous session" in user_prompt

        # Look for current-game observations
        seen_opp_a = "Opponent chose A" in user_prompt.split("Current session history:")[-1]

        if "Session 1" in user_prompt:
            # In Game A (vs always_b), switch to B after round 1
            action = "A" if curr_round == 1 else "B"
        else:
            # In Game B: G3 clings to Rule 2 longer than G0; G1 clings moderately
            if has_rules:
                action = "B" if curr_round <= 4 else "A"
            elif has_prev_history:
                action = "B" if curr_round <= 2 else "A"
            else:
                action = "A" if (curr_round == 1 or seen_opp_a) else "A"

        content = json.dumps({"reason": f"mock decision round {curr_round}", "action": action})
        return LLMResponse(
            content=content,
            prompt_tokens=len(user_prompt) // 4,
            completion_tokens=len(content) // 4,
            response_model=self.model,
            latency_s=0.001,
        )


# ---------------------------------------------------------------------------
# Prompt Formatting & Parsing
# ---------------------------------------------------------------------------

DECISION_SYSTEM_PROMPT = (
    "You are an autonomous decision-making agent playing a repeated two-player "
    "interactive task. Your sole objective is to maximize your own cumulative payoff "
    "in the current session. Respond ONLY with a valid JSON object of the form: "
    '{"reason": "<brief 1-sentence rationale>", "action": "A"} or '
    '{"reason": "<brief 1-sentence rationale>", "action": "B"}.'
)

RULE_EXTRACTION_SYSTEM_PROMPT = (
    "EXTRACT_RULES_TASK: Summarize the strategic lessons you learned from the "
    "completed session into 2-4 concise, actionable bullet-point rules for future "
    "interactive sessions. Keep it under 80 words."
)


def flip_action(action: str) -> str:
    return "B" if action == "A" else "A"


def get_payoffs(game_key: str, swap_labels: bool = False) -> dict[tuple[str, str], tuple[int, int]]:
    base = GAMES[game_key]["payoffs"]
    if not swap_labels:
        return base
    return {
        (a, o): base[(flip_action(a), flip_action(o))]
        for a in ("A", "B")
        for o in ("A", "B")
    }


def format_payoff_matrix(game_key: str, swap_labels: bool = False) -> str:
    p = get_payoffs(game_key, swap_labels=swap_labels)
    return (
        "Payoff matrix (Your payoff, Opponent payoff):\n"
        f"- You choose A, Opponent chooses A -> ({p[('A', 'A')][0]}, {p[('A', 'A')][1]})\n"
        f"- You choose A, Opponent chooses B -> ({p[('A', 'B')][0]}, {p[('A', 'B')][1]})\n"
        f"- You choose B, Opponent chooses A -> ({p[('B', 'A')][0]}, {p[('B', 'A')][1]})\n"
        f"- You choose B, Opponent chooses B -> ({p[('B', 'B')][0]}, {p[('B', 'B')][1]})"
    )


def format_history(
    history: list[dict[str, Any]],
    label_map: dict[str, str] | None = None,
    include_payoff: bool = True,
) -> str:
    if not history:
        return "(none yet)"
    lines = []
    for h in history:
        a_act = label_map.get(h["agent_action"], h["agent_action"]) if label_map else h["agent_action"]
        o_act = label_map.get(h["opp_action"], h["opp_action"]) if label_map else h["opp_action"]
        if include_payoff:
            lines.append(
                f"Round {h['round']}: You chose {a_act}, "
                f"Opponent chose {o_act}, Your payoff = {h['agent_payoff']}"
            )
        else:
            lines.append(f"Round {h['round']}: You chose {a_act}, Opponent chose {o_act}")
    return "\n".join(lines)


def build_irrelevant_pad(n_rounds: int) -> str:
    """Length-matched neutral log with no A/B tokens or strategic content."""
    lines = [
        f"Entry {r}: Station North logged code M, Station South logged code N, Index value = {r % 4}"
        for r in range(1, n_rounds + 1)
    ]
    return (
        "Unrelated archival log from another system (note: this log is irrelevant "
        "to the current session and its payoff structure):\n"
        + "\n".join(lines)
    )


def build_decision_prompt(
    session_label: str,
    game_key: str,
    round_idx: int,
    total_rounds: int,
    observability: str,
    current_history: list[dict[str, Any]],
    prior_context_block: str = "",
    swap_labels: bool = False,
) -> str:
    parts = [f"=== {session_label} ==="]
    if prior_context_block:
        parts.append(prior_context_block)
    if observability == "visible":
        parts.append(format_payoff_matrix(game_key, swap_labels=swap_labels))
    else:
        parts.append(
            "The exact payoff table is hidden; you learn payoffs from round-by-round "
            "feedback below. Available actions: A or B."
        )
    parts.append(f"Current round: {round_idx} of {total_rounds}")
    parts.append("Current session history:\n" + format_history(current_history))
    parts.append('Choose your action ("A" or "B") and reply in JSON.')
    return "\n\n".join(parts)


def parse_action(raw_text: str) -> tuple[str, bool]:
    """
    Returns (action, parse_ok). Defaults to 'A' only on unrecoverable parse failure
    while explicitly flagging parse_ok=False so error rates are never hidden.
    """
    text = raw_text.strip()
    # Try direct JSON or embedded JSON block
    candidates = [text]
    m_obj = re.search(r"\{.*?\}", text, flags=re.DOTALL)
    if m_obj:
        candidates.append(m_obj.group(0))
    for cand in candidates:
        try:
            obj = json.loads(cand)
            act = str(obj.get("action", "")).strip().upper()
            if act in ("A", "B"):
                return act, True
        except (json.JSONDecodeError, AttributeError):
            continue
    # Fallback regex for explicit action token
    m_act = re.search(r'"action"\s*:\s*"([AB])"', text, flags=re.IGNORECASE)
    if m_act:
        return m_act.group(1).upper(), True
    m_bare = re.fullmatch(r"([AB])\.?", text, flags=re.IGNORECASE)
    if m_bare:
        return m_bare.group(1).upper(), True
    return "A", False


# ---------------------------------------------------------------------------
# Episode & Experiment Execution
# ---------------------------------------------------------------------------

def run_session(
    client: OpenAICompatClient | MockClient,
    session_label: str,
    game_key: str,
    opp_key: str,
    rounds: int,
    observability: str,
    seed: int,
    condition: str,
    prior_context_block: str,
    event_sink: Callable[[dict[str, Any]], None],
    swap_labels: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    payoffs = get_payoffs(game_key, swap_labels=swap_labels)
    opp_fn = OPPONENTS[opp_key]
    history: list[dict[str, Any]] = []
    canonical_history: list[dict[str, Any]] = []
    stats = {"prompt_tokens": 0, "completion_tokens": 0, "parse_errors": 0}

    for r in range(1, rounds + 1):
        prompt = build_decision_prompt(
            session_label=session_label,
            game_key=game_key,
            round_idx=r,
            total_rounds=rounds,
            observability=observability,
            current_history=history,
            prior_context_block=prior_context_block,
            swap_labels=swap_labels,
        )
        resp = client.chat(DECISION_SYSTEM_PROMPT, prompt, seed=seed * 1000 + r)
        agent_action, parse_ok = parse_action(resp.content)
        canonical_opp = opp_fn(canonical_history)
        opp_action = flip_action(canonical_opp) if swap_labels else canonical_opp
        agent_payoff, opp_payoff = payoffs[(agent_action, opp_action)]

        if not parse_ok:
            stats["parse_errors"] += 1
        stats["prompt_tokens"] += resp.prompt_tokens
        stats["completion_tokens"] += resp.completion_tokens

        record = {
            "event_type": "round",
            "condition": condition,
            "seed": seed,
            "session": session_label,
            "game_key": game_key,
            "opp_key": opp_key,
            "swap_labels": swap_labels,
            "round": r,
            "agent_action": agent_action,
            "opp_action": opp_action,
            "agent_payoff": agent_payoff,
            "opp_payoff": opp_payoff,
            "parse_ok": parse_ok,
            "raw_response": resp.content,
            "prompt_tokens": resp.prompt_tokens,
            "completion_tokens": resp.completion_tokens,
            "response_model": resp.response_model,
            "latency_s": resp.latency_s,
        }
        event_sink(record)
        history.append(record)
        canonical_history.append({
            "round": r,
            "agent_action": flip_action(agent_action) if swap_labels else agent_action,
            "opp_action": canonical_opp,
        })

    return history, stats


def compute_adaptation_speed(history_b: list[dict[str, Any]], optimal_action: str) -> int | None:
    """First round t (1-indexed) where optimal_action is played for 2 consecutive rounds."""
    for i in range(len(history_b) - 1):
        if (
            history_b[i]["agent_action"] == optimal_action
            and history_b[i + 1]["agent_action"] == optimal_action
        ):
            return int(history_b[i]["round"])
    return None


def get_git_commit() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=Path(__file__).resolve().parent,
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8").strip()
    except Exception:
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description="LO-EXP-001 Pilot v0 Runner")
    parser.add_argument("--backend", choices=["mock", "openai_compat"], default="mock")
    parser.add_argument("--model", default="mock-v0", help="Model name for API backend")
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    parser.add_argument("--source-game", choices=list(GAMES.keys()), default="pd")
    parser.add_argument("--source-opp", choices=list(OPPONENTS.keys()), default="always_b")
    parser.add_argument("--target-game", choices=list(GAMES.keys()), default="stag_hunt")
    parser.add_argument("--target-opp", choices=list(OPPONENTS.keys()), default="tft_coop")
    parser.add_argument(
        "--target-opps",
        nargs="+",
        choices=list(OPPONENTS.keys()),
        default=None,
        help="Evaluate multiple target opponents in one run (overrides --target-opp), e.g. --target-opps tft_coop always_a",
    )
    parser.add_argument(
        "--swap-target-labels",
        action="store_true",
        help="Swap action labels A and B in Game B (payoff matrix + opponent actions) to test label vs structural transfer",
    )
    parser.add_argument(
        "--conditions",
        nargs="+",
        choices=["G0", "G0_PAD", "G1_NO_PAYOFF", "G1_XY", "G1", "G3"],
        default=["G0", "G1", "G3"],
        help="Conditions to evaluate (G0 must be included as baseline). E.g.: --conditions G0 G0_PAD G1_NO_PAYOFF G1_XY G1 G3",
    )
    parser.add_argument("--observability", choices=["hidden", "visible"], default="hidden")
    parser.add_argument("--rounds-a", type=int, default=10)
    parser.add_argument("--rounds-b", type=int, default=10)
    parser.add_argument("--early-window", type=int, default=5)
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--run-id", default=None, help="Optional custom run_id (must not already exist)")
    args = parser.parse_args()

    if args.backend == "openai_compat":
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            print("ERROR: OPENAI_API_KEY environment variable is required for openai_compat backend.", file=sys.stderr)
            return 2
        if args.model == "mock-v0":
            print("ERROR: Please specify --model for openai_compat backend.", file=sys.stderr)
            return 2
        client: OpenAICompatClient | MockClient = OpenAICompatClient(
            model=args.model,
            api_key=api_key,
            base_url=args.base_url,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    else:
        client = MockClient(model=args.model)

    # Create non-overwritable run directory
    exp_dir = Path(__file__).resolve().parent
    runs_dir = exp_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    target_opps = args.target_opps if args.target_opps else [args.target_opp]
    conditions = list(dict.fromkeys(args.conditions))
    if "G0" not in conditions:
        conditions = ["G0"] + conditions

    safe_model = re.sub(r"[^A-Za-z0-9._-]+", "_", args.model)
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    swap_tag = "_swapped" if args.swap_target_labels else ""
    run_id = args.run_id or f"{ts}_{args.backend}_{safe_model}_{args.observability}{swap_tag}"
    run_dir = runs_dir / run_id
    if run_dir.exists():
        print(f"ERROR: Run directory already exists (non-overwritable): {run_dir}", file=sys.stderr)
        return 2
    run_dir.mkdir(parents=True, exist_ok=False)

    config = {
        "experiment_id": "LO-EXP-001-pilot-v0",
        "run_id": run_id,
        "created_utc": ts,
        "git_commit": get_git_commit(),
        "backend": args.backend,
        "model": args.model,
        "base_url": args.base_url if args.backend == "openai_compat" else None,
        "source_game": args.source_game,
        "source_opp": args.source_opp,
        "target_game": args.target_game,
        "target_opps": target_opps,
        "swap_target_labels": args.swap_target_labels,
        "observability": args.observability,
        "rounds_a": args.rounds_a,
        "rounds_b": args.rounds_b,
        "early_window": min(args.early_window, args.rounds_b),
        "seeds": list(range(args.seeds)),
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "conditions": conditions,
    }
    (run_dir / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    raw_log_path = run_dir / "raw_events.jsonl"
    base_target_opt = GAMES[args.target_game].get("target_optimal_action", "A")
    target_opt = flip_action(base_target_opt) if args.swap_target_labels else base_target_opt
    early_n = config["early_window"]

    per_seed_results: dict[str, dict[str, list[dict[str, Any]]]] = {
        opp: {c: [] for c in conditions} for opp in target_opps
    }

    with raw_log_path.open("w", encoding="utf-8") as log_f:
        def write_event(ev: dict[str, Any]) -> None:
            log_f.write(json.dumps(ev, ensure_ascii=False) + "\n")
            log_f.flush()

        for seed in config["seeds"]:
            # 1) Run Game A once per seed to produce shared source experience
            hist_a, stats_a = run_session(
                client=client,
                session_label="Session 1",
                game_key=args.source_game,
                opp_key=args.source_opp,
                rounds=args.rounds_a,
                observability=args.observability,
                seed=seed,
                condition="SOURCE_A",
                prior_context_block="",
                event_sink=write_event,
                swap_labels=False,
            )

            # 2) Extract G3 rules from Game A (only if G3 is requested)
            rule_resp: LLMResponse | None = None
            if "G3" in conditions:
                extract_prompt = (
                    "You just completed Session 1 with the following history:\n"
                    + format_history(hist_a)
                    + "\n\nWrite 2-4 concise strategic rules based on this experience."
                )
                rule_resp = client.chat(RULE_EXTRACTION_SYSTEM_PROMPT, extract_prompt, seed=seed * 1000 + 999)
                write_event({
                    "event_type": "rule_extraction",
                    "condition": "G3",
                    "seed": seed,
                    "rules_text": rule_resp.content,
                    "prompt_tokens": rule_resp.prompt_tokens,
                    "completion_tokens": rule_resp.completion_tokens,
                    "response_model": rule_resp.response_model,
                    "latency_s": rule_resp.latency_s,
                })

            prior_blocks = {
                "G0": "",
                "G0_PAD": build_irrelevant_pad(len(hist_a)),
                "G1_NO_PAYOFF": (
                    "Action sequence from a previous session (payoffs omitted; note: the new "
                    "session may have a different payoff structure or opponent):\n"
                    + format_history(hist_a, include_payoff=False)
                ),
                "G1": (
                    "Full transcript from a previous session (note: the new session may "
                    "have a different payoff structure or opponent):\n"
                    + format_history(hist_a)
                ),
                "G1_XY": (
                    "Full transcript from a previous session (actions were labelled X and Y; "
                    "note: the new session may have a different payoff structure or opponent):\n"
                    + format_history(hist_a, label_map={"A": "X", "B": "Y"})
                ),
                "G3": (
                    "Extracted strategy rules from a previous session (note: the new session "
                    "may have a different payoff structure or opponent):\n"
                    + (rule_resp.content.strip() if rule_resp else "")
                ),
            }

            # 3) Run Game B under requested conditions for each target opponent
            for target_opp in target_opps:
                for cond in conditions:
                    hist_b, stats_b = run_session(
                        client=client,
                        session_label="Session 2",
                        game_key=args.target_game,
                        opp_key=target_opp,
                        rounds=args.rounds_b,
                        observability=args.observability,
                        seed=seed,
                        condition=cond,
                        prior_context_block=prior_blocks[cond],
                        event_sink=write_event,
                        swap_labels=args.swap_target_labels,
                    )
                    payoffs_b = [h["agent_payoff"] for h in hist_b]
                    early_payoff = sum(payoffs_b[:early_n]) / early_n
                    full_payoff = sum(payoffs_b) / len(payoffs_b)
                    adapt_round = compute_adaptation_speed(hist_b, target_opt)
                    extra_p = rule_resp.prompt_tokens if (cond == "G3" and rule_resp) else 0
                    extra_c = rule_resp.completion_tokens if (cond == "G3" and rule_resp) else 0

                    per_seed_results[target_opp][cond].append({
                        "seed": seed,
                        "target_opp": target_opp,
                        "early_payoff_b": early_payoff,
                        "mean_payoff_b": full_payoff,
                        "adaptation_round": adapt_round,
                        "parse_errors_b": stats_b["parse_errors"],
                        "prompt_tokens_b": stats_b["prompt_tokens"] + extra_p,
                        "completion_tokens_b": stats_b["completion_tokens"] + extra_c,
                        "source_a_mean_payoff": sum(h["agent_payoff"] for h in hist_a) / len(hist_a),
                        "source_a_parse_errors": stats_a["parse_errors"],
                    })

    # Aggregate summary metrics vs G0 baseline per target opponent
    summary_rows: list[dict[str, Any]] = []
    for target_opp in target_opps:
        g0_rows = per_seed_results[target_opp]["G0"]
        for cond in conditions:
            rows = per_seed_results[target_opp][cond]
            n = len(rows)
            mean_early = sum(r["early_payoff_b"] for r in rows) / n
            mean_full = sum(r["mean_payoff_b"] for r in rows) / n

            early_gains = [r["early_payoff_b"] - g0["early_payoff_b"] for r, g0 in zip(rows, g0_rows)]
            full_gains = [r["mean_payoff_b"] - g0["mean_payoff_b"] for r, g0 in zip(rows, g0_rows)]

            early_ntr = sum(1 for g in early_gains if g < -1e-9) / n if cond != "G0" else 0.0
            full_ntr = sum(1 for g in full_gains if g < -1e-9) / n if cond != "G0" else 0.0

            adapt_vals = [
                r["adaptation_round"] if r["adaptation_round"] is not None else (args.rounds_b + 1)
                for r in rows
            ]
            adapted_count = sum(1 for r in rows if r["adaptation_round"] is not None)

            summary_rows.append({
                "target_opp": target_opp,
                "condition": cond,
                "swap_target_labels": args.swap_target_labels,
                "seeds": n,
                "early_payoff_B": round(mean_early, 4),
                "early_transfer_gain": round(sum(early_gains) / n, 4),
                "early_negative_transfer_rate": round(early_ntr, 4),
                "mean_payoff_B": round(mean_full, 4),
                "full_transfer_gain": round(sum(full_gains) / n, 4),
                "full_negative_transfer_rate": round(full_ntr, 4),
                "mean_adaptation_round": round(sum(adapt_vals) / n, 4),
                "adapted_seeds": f"{adapted_count}/{n}",
                "total_prompt_tokens_B": sum(r["prompt_tokens_b"] for r in rows),
                "total_completion_tokens_B": sum(r["completion_tokens_b"] for r in rows),
                "parse_errors_B": sum(r["parse_errors_b"] for r in rows),
            })

    summary_payload = {
        "config": config,
        "summary": summary_rows,
        "per_seed": per_seed_results,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    with (run_dir / "summary.csv").open("w", newline="", encoding="utf-8") as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    # Print crisp Markdown table
    print(f"\nRun complete: {run_dir}")
    print(
        f"Backend: {args.backend} | Model: {args.model} | "
        f"Observability: {args.observability} | Swap Target Labels: {args.swap_target_labels}"
    )
    print(
        f"Pair: {args.source_game} (vs {args.source_opp}) -> "
        f"{args.target_game} (vs {', '.join(target_opps)})\n"
    )
    headers = [
        "Target Opp",
        "Cond",
        f"Early({early_n}) Payoff",
        "Early Gain",
        "Early NTR",
        "Full Payoff",
        "Adapt Round",
        "Parse Err",
    ]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---"] * len(headers)) + "|")
    for r in summary_rows:
        print(
            f"| {r['target_opp']} | {r['condition']} | {r['early_payoff_B']:.3f} "
            f"| {r['early_transfer_gain']:+.3f} | {r['early_negative_transfer_rate']:.2f} "
            f"| {r['mean_payoff_B']:.3f} | {r['mean_adaptation_round']:.2f} ({r['adapted_seeds']}) "
            f"| {r['parse_errors_B']} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
