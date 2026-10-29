#!/usr/bin/env python3
"""Compare direct and prompting-mitigation ROLECUE joint results."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def semantic_margin(row: dict[str, Any]) -> float | None:
    if row.get("logit_a") is None or row.get("logit_b") is None:
        return None
    margin = float(row["logit_a"]) - float(row["logit_b"])
    return margin if row["option_a_semantics"] == "yes" else -margin


def semantic_prediction(row: dict[str, Any]) -> str | None:
    if row.get("prediction") in {"A", "B"}:
        return row[f"option_{row['prediction'].lower()}_semantics"]
    if row.get("logit_a") is not None and row.get("logit_b") is not None:
        return (
            row["option_a_semantics"]
            if float(row["logit_a"]) >= float(row["logit_b"])
            else row["option_b_semantics"]
        )
    return None


def collapse(model: str, rows: list[dict[str, Any]], default_variant: str) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["task"] != "joint_match":
            continue
        variant = row.get("prompt_variant", default_variant)
        base_id = row.get("base_semantic_stimulus_id", row["semantic_stimulus_id"])
        grouped[(variant, base_id)].append(row)

    collapsed = []
    for (variant, base_id), group in grouped.items():
        if len(group) != 2:
            raise ValueError(f"Expected two option maps for {variant}/{base_id}, got {len(group)}")
        row = group[0]
        margins = [semantic_margin(item) for item in group]
        valid_margins = [item for item in margins if item is not None]
        margin = sum(valid_margins) / len(valid_margins) if valid_margins else None
        truth = "yes" if row["is_match"] else "no"
        categorical = [semantic_prediction(item) for item in group]
        categorical_prediction = categorical[0] if categorical[0] == categorical[1] else None
        prediction = (
            ("yes" if margin >= 0 else "no")
            if margin is not None
            else categorical_prediction
        )
        collapsed.append(
            {
                "model": model,
                "prompt_variant": variant,
                "base_semantic_stimulus_id": base_id,
                "language": row["language"],
                "order": row["order"],
                "action": row["action"],
                "is_match": row["is_match"],
                "semantic_margin": margin,
                "semantic_prediction": prediction,
                "correct": prediction == truth,
                "option_consistent": categorical[0] == categorical[1],
            }
        )
    return collapsed


def aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["model"], row["prompt_variant"], row["language"], row["order"])].append(row)
    output = []
    for keys, group in sorted(grouped.items()):
        n = len(group)
        output.append(
            {
                **dict(zip(("model", "prompt_variant", "language", "order"), keys, strict=True)),
                "n": n,
                "accuracy": sum(row["correct"] for row in group) / n,
                "option_consistency": sum(row["option_consistent"] for row in group) / n,
                "mean_abs_margin": (
                    sum(abs(row["semantic_margin"]) for row in group if row["semantic_margin"] is not None)
                    / sum(row["semantic_margin"] is not None for row in group)
                    if any(row["semantic_margin"] is not None for row in group)
                    else None
                ),
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--direct", action="append", default=[], metavar="MODEL=PATH")
    parser.add_argument("--mitigation", action="append", default=[], metavar="MODEL=PATH")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    collapsed = []
    for spec in args.direct:
        model, path = spec.split("=", 1)
        collapsed.extend(collapse(model, read_jsonl(Path(path)), "direct"))
    for spec in args.mitigation:
        model, path = spec.split("=", 1)
        collapsed.extend(collapse(model, read_jsonl(Path(path)), "mitigation"))
    table = aggregate(collapsed)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "collapsed.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in collapsed:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    (args.output_dir / "summary.json").write_text(json.dumps(table, indent=2), encoding="utf-8")
    lines = [
        "# ROLECUE prompting mitigation",
        "",
        "Scores use antisymmetric semantic margins collapsed across reversed A/B maps.",
        "",
        "| Model | Prompt | Language | Order | n | Accuracy | Option consistency | Mean |margin| |",
        "|---|---|---|---|---:|---:|---:|---:|",
    ]
    for row in table:
        mean_margin = (
            f"{row['mean_abs_margin']:.3f}"
            if row["mean_abs_margin"] is not None
            else "n/a"
        )
        lines.append(
            f"| {row['model']} | {row['prompt_variant']} | {row['language']} | "
            f"{row['order']} | {row['n']} | {100 * row['accuracy']:.1f}% | "
            f"{100 * row['option_consistency']:.1f}% | {mean_margin} |"
        )
    (args.output_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(collapsed)} collapsed trials to {args.output_dir}")


if __name__ == "__main__":
    main()
