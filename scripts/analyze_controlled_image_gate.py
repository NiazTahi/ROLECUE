"""Score controlled-v1 image validity with paired labels and scene clusters."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np


ROLECUE_IMAGE_ID = re.compile(
    r"^(?P<prefix>(?:realv2|rolecue192)_[^_]+_s[0-9]+)_(?P<agent>red|blue)_agent_(?P<side>left|right)$"
)


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def collapse(rows: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["semantic_stimulus_id"]].append(row)
    output = []
    for stimulus_id, pair in groups.items():
        if len(pair) != 2:
            raise ValueError(f"{stimulus_id}: expected two option maps, found {len(pair)}")
        margins = []
        hard_red = []
        for row in pair:
            sign = 1.0 if row["option_a_semantics"] == "red" else -1.0
            if row.get("logit_a") is not None and row.get("logit_b") is not None:
                margins.append((row["logit_a"] - row["logit_b"]) * sign)
            if row["prediction"] == "A":
                chosen = row["option_a_semantics"]
            elif row["prediction"] == "B":
                chosen = row["option_b_semantics"]
            elif row.get("logit_a") is not None and row.get("logit_b") is not None:
                chosen = (
                    row["option_a_semantics"]
                    if row["logit_a"] >= row["logit_b"]
                    else row["option_b_semantics"]
                )
            else:
                chosen = None
            hard_red.append(chosen == "red")
        base = {key: pair[0][key] for key in (
            "candidate_id", "action", "visual_agent_color", "red_side", "image_path"
        )}
        margin = float(np.mean(margins)) if margins else None
        if margin is None:
            predicted_red = hard_red[0] if hard_red[0] == hard_red[1] else None
        else:
            predicted_red = margin > 0
        base.update({
            "semantic_stimulus_id": stimulus_id,
            "red_margin": margin,
            "predicted_agent_color": (
                "red" if predicted_red is True else "blue" if predicted_red is False else None
            ),
            "correct": (
                predicted_red == (base["visual_agent_color"] == "red")
                if predicted_red is not None
                else False
            ),
            "option_map_agreement": hard_red[0] == hard_red[1],
            "agent_side": base["red_side"] if base["visual_agent_color"] == "red" else (
                "right" if base["red_side"] == "left" else "left"
            ),
        })
        output.append(base)
    return output


def accuracy(rows: list[dict]) -> float:
    return float(np.mean([row["correct"] for row in rows]))


def cluster_ci(rows: list[dict], statistic, samples: int, seed: int) -> list[float]:
    blocks: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        blocks[row["candidate_id"]].append(row)
    ids = sorted(blocks)
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(samples):
        selected = rng.choice(ids, len(ids), replace=True)
        sample = [row for item_id in selected for row in blocks[item_id]]
        estimates.append(statistic(sample))
    return list(map(float, np.quantile(estimates, [0.025, 0.975])))


def pair_success_ci(
    pairs: dict[str, list[dict]], samples: int, seed: int
) -> list[float]:
    ids = sorted(pairs)
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(samples):
        selected = rng.choice(ids, len(ids), replace=True)
        estimates.append(
            float(
                np.mean(
                    [
                        len(pairs[item_id]) == 2
                        and all(item["correct"] for item in pairs[item_id])
                        for item_id in selected
                    ]
                )
            )
        )
    return list(map(float, np.quantile(estimates, [0.025, 0.975])))


def group_accuracy(rows: list[dict], key: str) -> dict[str, float]:
    values = sorted({row[key] for row in rows})
    return {value: accuracy([row for row in rows if row[key] == value]) for value in values}


def summarize(rows: list[dict], samples: int, seed: int) -> dict:
    paired: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        paired[role_pair_key(row)].append(row)
    reversal_success = float(np.mean([
        len(pair) == 2 and all(row["correct"] for row in pair) for pair in paired.values()
    ]))
    by_action = group_accuracy(rows, "action")
    by_color = group_accuracy(rows, "visual_agent_color")
    by_side = group_accuracy(rows, "agent_side")
    overall = accuracy(rows)
    summary = {
        "base_scenes": len(paired),
        "images": len(rows),
        "accuracy": overall,
        "accuracy_ci": cluster_ci(rows, accuracy, samples, seed),
        "role_reversal_success": reversal_success,
        "role_reversal_ci": pair_success_ci(paired, samples, seed),
        "option_map_agreement": float(np.mean([row["option_map_agreement"] for row in rows])),
        "accuracy_by_action": by_action,
        "accuracy_by_agent_color": by_color,
        "accuracy_by_agent_side": by_side,
        "color_gap": max(by_color.values()) - min(by_color.values()),
        "side_gap": max(by_side.values()) - min(by_side.values()),
    }
    summary["gate_pass"] = bool(
        overall >= 0.90
        and min(by_action.values()) >= 0.85
        and reversal_success >= 0.85
        and summary["color_gap"] < 0.05
        and summary["side_gap"] < 0.05
        and summary["option_map_agreement"] >= 0.90
    )
    return summary


def _pairs(rows: list[dict]) -> dict[str, list[dict]]:
    pairs: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        pairs[role_pair_key(row)].append(row)
    return pairs


def role_pair_key(row: dict) -> str:
    """Return the red/blue role-reversal pair key for an image-gate row.

    Older controlled manifests used `candidate_id` for the role-reversal pair.
    ROLECUE-96/192 uses unique image IDs such as
    `realv2_bandaging_s1_blue_agent_left`, so the pair key must remove only the
    visual-agent color while retaining action, seed, and side.
    """

    stimulus_id = row.get("semantic_stimulus_id", "")
    match = ROLECUE_IMAGE_ID.fullmatch(stimulus_id)
    if match:
        return f"{match.group('prefix')}__agent-side-{match.group('side')}"
    return row["candidate_id"]


def make_markdown(model: str, summary: dict) -> str:
    lo, hi = summary["accuracy_ci"]
    rlo, rhi = summary["role_reversal_ci"]
    lines = [
        f"# {model}: controlled visual gate",
        "",
        f"**Gate: {'PASS' if summary['gate_pass'] else 'FAIL'}**",
        "",
        f"- Accuracy: {summary['accuracy']:.1%} ({lo:.1%}-{hi:.1%})",
        f"- Paired role-reversal success: {summary['role_reversal_success']:.1%} ({rlo:.1%}-{rhi:.1%})",
        f"- Option-map agreement: {summary['option_map_agreement']:.1%}",
        f"- Color gap: {summary['color_gap']:.1%}",
        f"- Side gap: {summary['side_gap']:.1%}",
        "",
        "## Accuracy by action",
        "",
    ]
    lines.extend(f"- {key}: {value:.1%}" for key, value in summary["accuracy_by_action"].items())
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--bootstrap-samples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20270821)
    args = parser.parse_args()
    collapsed = collapse(read_jsonl(args.input))
    summary = summarize(collapsed, args.bootstrap_samples, args.seed)
    summary["model"] = args.model
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "collapsed.jsonl").open("w", encoding="utf-8") as handle:
        for row in collapsed:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.output_dir / "SUMMARY.md").write_text(make_markdown(args.model, summary), encoding="utf-8")


if __name__ == "__main__":
    main()
