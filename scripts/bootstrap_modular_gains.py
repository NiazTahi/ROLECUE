#!/usr/bin/env python3
"""Bootstrap confidence intervals for ROLECUE modular gains.

The resampling unit is the image key within each model/language/order group.
This keeps all sentence-agent/match variants derived from the same visual scene
together during resampling.
"""

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


def metric(rows: list[dict[str, Any]], key: str) -> float:
    return sum(bool(row[key]) for row in rows) / len(rows) if rows else 0.0


def gain(rows: list[dict[str, Any]]) -> float:
    return metric(rows, "modular_correct") - metric(rows, "direct_correct")


def bootstrap_ci(rows: list[dict[str, Any]], samples: int, seed: int) -> tuple[float, float]:
    blocks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        blocks[row["image_key"]].append(row)
    keys = sorted(blocks)
    rng = random.Random(seed)
    estimates = []
    for _ in range(samples):
        chosen = [rng.choice(keys) for _ in keys]
        sample = [row for key in chosen for row in blocks[key]]
        estimates.append(gain(sample))
    estimates.sort()
    lo_idx = int(0.025 * (len(estimates) - 1))
    hi_idx = int(0.975 * (len(estimates) - 1))
    return estimates[lo_idx], estimates[hi_idx]


def pct(value: float) -> str:
    return f"{100 * value:.1f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20270822)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["model"], row["language"], row["order"])].append(row)

    output = []
    for (model, language, order), group in sorted(groups.items()):
        lo, hi = bootstrap_ci(group, args.samples, args.seed)
        output.append(
            {
                "model": model,
                "language": language,
                "order": order,
                "n": len(group),
                "image_blocks": len({row["image_key"] for row in group}),
                "direct_accuracy": metric(group, "direct_correct"),
                "image_accuracy": metric(group, "image_correct"),
                "text_accuracy": metric(group, "text_correct"),
                "modular_accuracy": metric(group, "modular_correct"),
                "gain": gain(group),
                "gain_ci95": [lo, hi],
            }
        )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2), encoding="utf-8")
    lines = [
        "# ROLECUE modular gain bootstrap CIs",
        "",
        "CIs are 95% percentile bootstrap intervals over image keys within each model/language/order group.",
        "",
        "| Model | Language | Order | n | Direct | Image | Text | Modular | Gain [95% CI] |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in output:
        lo, hi = row["gain_ci95"]
        lines.append(
            f"| {row['model']} | {row['language']} | {row['order']} | {row['n']} | "
            f"{pct(row['direct_accuracy'])} | {pct(row['image_accuracy'])} | "
            f"{pct(row['text_accuracy'])} | {pct(row['modular_accuracy'])} | "
            f"{pct(row['gain'])} [{pct(lo)}, {pct(hi)}] |"
        )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(output)} bootstrap rows")


if __name__ == "__main__":
    main()
