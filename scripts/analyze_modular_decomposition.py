#!/usr/bin/env python3
"""Evaluate independent vision/language role extraction followed by symbolic comparison."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def mapped_margin(row: dict[str, Any], positive: str) -> float:
    margin = float(row["logit_a"]) - float(row["logit_b"])
    return margin if row["option_a_semantics"] == positive else -margin


def collapse_color(rows: list[dict[str, Any]], task: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["task"] == task:
            groups[row["semantic_stimulus_id"]].append(row)
    output = []
    for stimulus_id, group in groups.items():
        if len(group) != 2:
            raise ValueError(f"Expected two option maps for {stimulus_id}, got {len(group)}")
        row = group[0]
        margin = sum(mapped_margin(item, "red") for item in group) / 2
        predicted_color = "red" if margin >= 0 else "blue"
        categorical = []
        for item in group:
            if item.get("prediction") in {"A", "B"}:
                categorical.append(item[f"option_{item['prediction'].lower()}_semantics"])
            else:
                categorical.append(None)
        output.append(
            {
                **row,
                "predicted_color": predicted_color,
                "semantic_margin": margin,
                "option_consistent": categorical[0] == categorical[1],
            }
        )
    return output


def normalized_candidate_id(row: dict[str, Any]) -> str:
    candidate_id = row["candidate_id"]
    return candidate_id.removeprefix("realv2_")


def evaluate(model: str, image_path: Path, multilingual_path: Path) -> list[dict[str, Any]]:
    images = {
        normalized_candidate_id(row): row
        for row in collapse_color(read_jsonl(image_path), "image_only")
    }
    texts = collapse_color(read_jsonl(multilingual_path), "text_only")
    output = []
    for text_row in texts:
        candidate_id = normalized_candidate_id(text_row)
        if candidate_id not in images:
            raise KeyError(f"No image-only result for {candidate_id}")
        image_row = images[candidate_id]
        predicted_match = image_row["predicted_color"] == text_row["predicted_color"]
        true_match = text_row["visual_agent_color"] == text_row["sentence_agent_color"]
        output.append(
            {
                "model": model,
                "semantic_stimulus_id": text_row["semantic_stimulus_id"],
                "candidate_id": candidate_id,
                "language": text_row["language"],
                "order": text_row["order"],
                "action": text_row["action"],
                "true_match": true_match,
                "predicted_match": predicted_match,
                "modular_correct": predicted_match == true_match,
                "image_prediction": image_row["predicted_color"],
                "image_truth": image_row["visual_agent_color"],
                "image_correct": image_row["predicted_color"] == image_row["visual_agent_color"],
                "text_prediction": text_row["predicted_color"],
                "text_truth": text_row["sentence_agent_color"],
                "text_correct": text_row["predicted_color"] == text_row["sentence_agent_color"],
                "image_option_consistent": image_row["option_consistent"],
                "text_option_consistent": text_row["option_consistent"],
            }
        )
    return output


def aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["model"], row["language"], row["order"])].append(row)
    output = []
    for keys, group in sorted(groups.items()):
        n = len(group)
        output.append(
            {
                **dict(zip(("model", "language", "order"), keys, strict=True)),
                "n": n,
                "image_accuracy": sum(x["image_correct"] for x in group) / n,
                "text_accuracy": sum(x["text_correct"] for x in group) / n,
                "modular_accuracy": sum(x["modular_correct"] for x in group) / n,
                "both_components_correct": (
                    sum(x["image_correct"] and x["text_correct"] for x in group) / n
                ),
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, metavar="MODEL=IMAGE,TEXT")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for spec in args.input:
        model, paths = spec.split("=", 1)
        image_path, text_path = paths.split(",", 1)
        rows.extend(evaluate(model, Path(image_path), Path(text_path)))
    table = aggregate(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "collapsed.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    (args.output_dir / "summary.json").write_text(json.dumps(table, indent=2), encoding="utf-8")
    lines = [
        "# ROLECUE independent modular decomposition",
        "",
        "Image and sentence Agents are inferred in separate calls with counterbalanced",
        "semantic margins, then compared deterministically without a joint VLM call.",
        "",
        "| Model | Language | Order | n | Image Agent | Text Agent | Both correct | Modular match |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in table:
        lines.append(
            f"| {row['model']} | {row['language']} | {row['order']} | {row['n']} | "
            f"{100 * row['image_accuracy']:.1f}% | {100 * row['text_accuracy']:.1f}% | "
            f"{100 * row['both_components_correct']:.1f}% | "
            f"{100 * row['modular_accuracy']:.1f}% |"
        )
    (args.output_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} modular trials to {args.output_dir}")


if __name__ == "__main__":
    main()
