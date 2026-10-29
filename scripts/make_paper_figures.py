#!/usr/bin/env python3
"""Generate publication figures from frozen ROLECUE analyses."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


MODEL_LABEL = {"InternVL3.5-8B": "InternVL3.5-8B", "Qwen2.5-VL-7B": "Qwen2.5-VL-7B"}
LANGUAGE_LABEL = {"de": "German", "tr": "Turkish", "ja": "Japanese"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save(fig: Any, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(output_dir / f"{stem}.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def factorial_figure(root: Path, output_dir: Path) -> None:
    image_dir = root / "data/processed/rolecue/realistic_v2_prototype"
    red = plt.imread(image_dir / "push_red_agent_left.png")
    blue = plt.imread(image_dir / "push_blue_agent_left.png")
    fig, axes = plt.subplots(2, 2, figsize=(7.1, 5.25), constrained_layout=True)
    sentences = [
        ("Agent-first", "Der Mann im roten T-Shirt schiebt\nden Mann im blauen T-Shirt."),
        ("Patient-first", "Den Mann im blauen T-Shirt schiebt\nder Mann im roten T-Shirt."),
    ]
    for row, (order, sentence) in enumerate(sentences):
        for column, (image, visual_agent) in enumerate(((red, "red"), (blue, "blue"))):
            axis = axes[row, column]
            axis.imshow(image)
            axis.set_xticks([])
            axis.set_yticks([])
            outcome = "MATCH" if visual_agent == "red" else "MISMATCH"
            color = "#217a3c" if outcome == "MATCH" else "#b33a3a"
            axis.set_title(
                f"{order} sentence / visual Agent: {visual_agent}\n{sentence}", fontsize=8
            )
            axis.text(
                0.02,
                0.04,
                outcome,
                transform=axis.transAxes,
                color="white",
                fontsize=9,
                fontweight="bold",
                bbox={"boxstyle": "round,pad=0.25", "facecolor": color, "edgecolor": "none"},
            )
    fig.suptitle(
        "ROLECUE independently varies visual role, grammatical case, and noun order",
        fontsize=11,
        fontweight="bold",
    )
    save(fig, output_dir, "fig1_rolecue_factorial")


def forest_figure(fusion_rows: list[dict[str, Any]], output_dir: Path) -> None:
    rows = sorted(
        fusion_rows,
        key=lambda row: (
            0 if row["model"].startswith("Intern") else 1,
            ("de", "tr", "ja").index(row["language"]),
            0 if row["order"] == "agent_first" else 1,
        ),
    )
    labels = [
        f"{MODEL_LABEL[row['model']]} · {LANGUAGE_LABEL[row['language']]} · "
        f"{'Agent-first' if row['order'] == 'agent_first' else 'Patient-first'}"
        for row in rows
    ]
    values = np.array([100 * row["fusion_gap"] for row in rows])
    low = np.array([100 * row["fusion_gap_ci_low"] for row in rows])
    high = np.array([100 * row["fusion_gap_ci_high"] for row in rows])
    colors = ["#3879b9" if row["order"] == "agent_first" else "#dd7b29" for row in rows]
    y = np.arange(len(rows))[::-1]
    fig, axis = plt.subplots(figsize=(7.0, 5.0))
    axis.axvline(0, color="#555555", linewidth=1, linestyle="--")
    for index in range(len(rows)):
        axis.errorbar(
            values[index],
            y[index],
            xerr=[[values[index] - low[index]], [high[index] - values[index]]],
            fmt="o",
            color=colors[index],
            capsize=3,
            markersize=5,
        )
    axis.set_yticks(y, labels, fontsize=8)
    axis.set_xlabel("Modular minus direct accuracy (percentage points)")
    axis.set_title("Enforced modular inference exposes the joint-call fusion gap", fontweight="bold")
    axis.grid(axis="x", alpha=0.25)
    axis.spines[["top", "right"]].set_visible(False)
    save(fig, output_dir, "fig2_fusion_gap_forest")


def mitigation_figure(
    mitigation_rows: list[dict[str, Any]],
    modular_rows: list[dict[str, Any]],
    output_dir: Path,
) -> None:
    methods = ["direct", "conflict_warning", "role_first", "modular"]
    method_labels = ["Direct", "Case warning", "Role-first\n(one call)", "Enforced\nmodular"]
    models = ["InternVL3.5-8B", "Qwen2.5-VL-7B"]
    values: dict[str, list[float]] = {model: [] for model in models}
    for model in models:
        for method in methods[:-1]:
            row = next(
                item
                for item in mitigation_rows
                if item["model"] == model
                and item["language"] == "ja"
                and item["order"] == "patient_first"
                and item["prompt_variant"] == method
            )
            values[model].append(100 * row["accuracy"])
        modular = next(
            item
            for item in modular_rows
            if item["model"] == model
            and item["language"] == "ja"
            and item["order"] == "patient_first"
        )
        values[model].append(100 * modular["modular_accuracy"])

    x = np.arange(len(methods))
    width = 0.36
    fig, axis = plt.subplots(figsize=(6.8, 3.55))
    for offset, model, color in (
        (-width / 2, models[0], "#3879b9"),
        (width / 2, models[1], "#dd7b29"),
    ):
        bars = axis.bar(x + offset, values[model], width, label=MODEL_LABEL[model], color=color)
        axis.bar_label(bars, fmt="%.1f", fontsize=7, padding=2)
    axis.axhline(50, color="#666666", linestyle="--", linewidth=1, label="Chance")
    axis.set_ylim(0, 112)
    axis.set_ylabel("Semantic accuracy (%)")
    axis.set_xticks(x, method_labels)
    axis.set_title(
        "Japanese Patient-first: prompting is not enforced decomposition", fontweight="bold"
    )
    axis.legend(frameon=False, ncol=3, fontsize=8, loc="upper left")
    axis.spines[["top", "right"]].set_visible(False)
    axis.grid(axis="y", alpha=0.2)
    save(fig, output_dir, "fig3_japanese_mitigation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    fusion = read_json(root / "results/rolecue/realistic_v2_fusion_gap_2model_3lang/summary.json")
    mitigation = read_json(
        root / "results/rolecue/realistic_v2_mitigation_analysis_2model_3lang/summary.json"
    )
    modular = read_json(
        root / "results/rolecue/realistic_v2_modular_analysis_2model_3lang/summary.json"
    )
    factorial_figure(root, args.output_dir)
    forest_figure(fusion, args.output_dir)
    mitigation_figure(mitigation, modular, args.output_dir)
    print(f"Wrote three figures as PDF and PNG to {args.output_dir}")


if __name__ == "__main__":
    main()
