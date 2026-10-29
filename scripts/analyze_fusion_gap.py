#!/usr/bin/env python3
"""Estimate direct-to-modular ROLECUE fusion gaps with candidate bootstrap intervals."""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def bootstrap_candidate_gap(
    candidate_values: dict[str, list[float]], *, samples: int, seed: int
) -> tuple[float, float]:
    candidate_means = {
        candidate: sum(values) / len(values) for candidate, values in candidate_values.items()
    }
    candidates = sorted(candidate_means)
    if not candidates:
        raise ValueError("Cannot bootstrap an empty candidate set")
    rng = random.Random(seed)
    draws = []
    for _ in range(samples):
        resampled = [rng.choice(candidates) for _ in candidates]
        draws.append(sum(candidate_means[candidate] for candidate in resampled) / len(resampled))
    return percentile(draws, 0.025), percentile(draws, 0.975)


def join_trials(direct: list[dict[str, Any]], modular: list[dict[str, Any]]) -> list[dict[str, Any]]:
    modular_index = {
        (
            row["model"],
            row["candidate_id"],
            row["language"],
            row["order"],
            row["true_match"],
        ): row
        for row in modular
    }
    output = []
    for row in direct:
        if row["task"] != "joint_match":
            continue
        key = (
            row["model"],
            row["candidate_id"],
            row["language"],
            row["order"],
            row["is_match"],
        )
        if key not in modular_index:
            raise KeyError(f"No modular trial for {key}")
        modular_row = modular_index[key]
        output.append(
            {
                "model": row["model"],
                "candidate_id": row["candidate_id"],
                "language": row["language"],
                "order": row["order"],
                "action": row["action"],
                "direct_correct": bool(row["case_correct"]),
                "modular_correct": bool(modular_row["modular_correct"]),
                "gap": int(modular_row["modular_correct"]) - int(row["case_correct"]),
            }
        )
    if len(output) != len(modular):
        raise ValueError(f"Joined {len(output)} direct trials to {len(modular)} modular trials")
    return output


def aggregate(rows: list[dict[str, Any]], samples: int, seed: int) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["model"], row["language"], row["order"])].append(row)
    output = []
    for index, (keys, group) in enumerate(sorted(groups.items())):
        candidate_values: dict[str, list[float]] = defaultdict(list)
        for row in group:
            candidate_values[row["candidate_id"]].append(float(row["gap"]))
        low, high = bootstrap_candidate_gap(
            candidate_values, samples=samples, seed=seed + index
        )
        n = len(group)
        output.append(
            {
                **dict(zip(("model", "language", "order"), keys, strict=True)),
                "n_trials": n,
                "n_candidates": len(candidate_values),
                "direct_accuracy": sum(row["direct_correct"] for row in group) / n,
                "modular_accuracy": sum(row["modular_correct"] for row in group) / n,
                "fusion_gap": sum(row["gap"] for row in group) / n,
                "fusion_gap_ci_low": low,
                "fusion_gap_ci_high": high,
            }
        )
    return output


def sensitivity(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    base_groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["model"], row["language"], row["order"], row["action"])].append(row)
        base_groups[(row["model"], row["language"], row["order"])].append(row)

    by_action = []
    for keys, group in sorted(groups.items()):
        n = len(group)
        by_action.append(
            {
                **dict(zip(("model", "language", "order", "action"), keys, strict=True)),
                "n": n,
                "direct_accuracy": sum(row["direct_correct"] for row in group) / n,
                "modular_accuracy": sum(row["modular_correct"] for row in group) / n,
                "fusion_gap": sum(row["gap"] for row in group) / n,
            }
        )

    leave_one_out = []
    for keys, group in sorted(base_groups.items()):
        for omitted in sorted({row["action"] for row in group}):
            retained = [row for row in group if row["action"] != omitted]
            n = len(retained)
            leave_one_out.append(
                {
                    **dict(zip(("model", "language", "order"), keys, strict=True)),
                    "omitted_action": omitted,
                    "n": n,
                    "direct_accuracy": sum(row["direct_correct"] for row in retained) / n,
                    "modular_accuracy": sum(row["modular_correct"] for row in retained) / n,
                    "fusion_gap": sum(row["gap"] for row in retained) / n,
                }
            )
    return by_action, leave_one_out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--direct-collapsed", type=Path, required=True)
    parser.add_argument("--modular-collapsed", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--bootstrap-samples", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20270829)
    args = parser.parse_args()

    joined = join_trials(read_jsonl(args.direct_collapsed), read_jsonl(args.modular_collapsed))
    table = aggregate(joined, args.bootstrap_samples, args.seed)
    by_action, leave_one_out = sensitivity(joined)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(json.dumps(table, indent=2), encoding="utf-8")
    (args.output_dir / "by_action.json").write_text(
        json.dumps(by_action, indent=2), encoding="utf-8"
    )
    (args.output_dir / "leave_one_action_out.json").write_text(
        json.dumps(leave_one_out, indent=2), encoding="utf-8"
    )
    lines = [
        "# ROLECUE direct-to-modular fusion gap",
        "",
        f"Intervals use {args.bootstrap_samples:,} resamples of the candidate/image cluster.",
        "A positive gap means enforced modular inference is more accurate than one joint call.",
        "",
        "| Model | Language | Order | Candidates | Direct | Modular | Gap [95% CI] |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for row in table:
        lines.append(
            f"| {row['model']} | {row['language']} | {row['order']} | "
            f"{row['n_candidates']} | {100 * row['direct_accuracy']:.1f}% | "
            f"{100 * row['modular_accuracy']:.1f}% | {100 * row['fusion_gap']:.1f} "
            f"[{100 * row['fusion_gap_ci_low']:.1f}, "
            f"{100 * row['fusion_gap_ci_high']:.1f}] |"
        )
    lines.extend(
        [
            "",
            "## Japanese Patient-first leave-one-action-out",
            "",
            "| Model | Omitted action | Direct | Modular | Gap |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for row in leave_one_out:
        if row["language"] == "ja" and row["order"] == "patient_first":
            lines.append(
                f"| {row['model']} | {row['omitted_action']} | "
                f"{100 * row['direct_accuracy']:.1f}% | "
                f"{100 * row['modular_accuracy']:.1f}% | "
                f"{100 * row['fusion_gap']:.1f} |"
            )
    (args.output_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(table)} fusion-gap cells to {args.output_dir}")


if __name__ == "__main__":
    main()
