#!/usr/bin/env python3
"""Build compact ROLECUE-192 closed-model reference tables for OpenAI runs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path("results/rolecue")
TABLE_DIR = Path("wacv-2027-author-kit-template/tables")
OUT_DIR = ROOT / "rolecue192_openai_closed_reference"

MODELS = [
    {
        "label": "GPT-5.6-Luna",
        "short": "Luna",
        "slug": "gpt56_luna",
        "dir": ROOT / "rolecue192_openai_gpt56_luna",
        "image": "gpt56_luna_image_gate_rolecue192_reasoning_none.jsonl",
        "multi": "gpt56_luna_missing_text_joint_rolecue192_reasoning_none.jsonl",
    },
    {
        "label": "GPT-5.6-Terra",
        "short": "Terra",
        "slug": "gpt56_terra",
        "dir": ROOT / "rolecue192_openai_gpt56_terra",
        "image": "gpt56_terra_image_gate_rolecue192_reasoning_none.jsonl",
        "multi": "gpt56_terra_missing_text_joint_rolecue192_reasoning_none.jsonl",
    },
    {
        "label": "GPT-5.6-Sol",
        "short": "Sol",
        "slug": "gpt56_sol",
        "dir": ROOT / "rolecue192_openai_gpt56_sol",
        "image": "gpt56_sol_image_gate_rolecue192_reasoning_none.jsonl",
        "multi": "gpt56_sol_missing_text_joint_rolecue192_reasoning_none.jsonl",
    },
]

LANGS = ["de", "ja", "tr", "en", "ko", "bn"]


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def parse_failures(path: Path) -> int:
    failures = 0
    if not path.exists():
        return failures
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        failures += int(not row.get("parse_ok"))
    return failures


def run(cmd: list[str]) -> None:
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ml_lookup(summary: dict[str, Any], task: str, language: str, order: str) -> float:
    for row in summary.get("main", []):
        if row["task"] == task and row["language"] == language and row["order"] == order:
            return float(row["case_accuracy"])
    raise KeyError((task, language, order))


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}"


def build_joint_pf_table(ready: list[dict[str, Any]]) -> str:
    lines = [
        "\\begin{table}[H]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3.0pt}",
        "\\begin{tabular}{lrrrrrrr}",
        "\\toprule",
        "Model & Image & de & ja & tr & en & ko & bn \\\\",
        "\\midrule",
    ]
    for item in ready:
        vals = [pct(ml_lookup(item["ml_summary"], "joint_match", lang, "patient_first")) for lang in LANGS]
        lines.append(f"{item['short']} & {pct(item['image_summary']['accuracy'])} & " + " & ".join(vals) + " \\\\")
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Closed-model ROLECUE-192 reference. Image is image-only visual-role accuracy; language columns report patient-first direct joint accuracy. Values are percentages. These proprietary systems are contextual references and are not included in the eight open-weight model count.}",
            "\\label{tab:openai-192-reference}",
            "\\end{table}",
            "",
        ]
    )
    return "\n".join(lines)


def build_text_pf_table(ready: list[dict[str, Any]]) -> str:
    lines = [
        "\\begin{table}[H]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3.0pt}",
        "\\begin{tabular}{lrrrrrr}",
        "\\toprule",
        "Model & de & ja & tr & en & ko & bn \\\\",
        "\\midrule",
    ]
    for item in ready:
        vals = [pct(ml_lookup(item["ml_summary"], "text_only", lang, "patient_first")) for lang in LANGS]
        lines.append(f"{item['short']} & " + " & ".join(vals) + " \\\\")
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Closed-model ROLECUE-192 patient-first text-only role-parsing reference. Values are percentages.}",
            "\\label{tab:openai-192-text-reference}",
            "\\end{table}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    ready: list[dict[str, Any]] = []
    statuses: list[dict[str, Any]] = []
    for model in MODELS:
        image_path = model["dir"] / model["image"]
        multi_path = model["dir"] / model["multi"]
        status = {
            "label": model["label"],
            "image_rows": count_jsonl(image_path),
            "multi_rows": count_jsonl(multi_path),
            "parse_failures": parse_failures(multi_path),
        }
        status["complete"] = (
            status["image_rows"] == 384
            and status["multi_rows"] == 13824
            and status["parse_failures"] == 0
        )
        statuses.append(status)
        if not status["complete"]:
            continue
        image_out = OUT_DIR / f"image_gate_{model['slug']}"
        ml_out = OUT_DIR / f"multilingual_{model['slug']}"
        run(
            [
                sys.executable,
                "rolecue/scripts/analyze_controlled_image_gate.py",
                str(image_path),
                str(image_out),
                "--model",
                model["label"],
                "--bootstrap-samples",
                "2000",
            ]
        )
        run(
            [
                sys.executable,
                "rolecue/scripts/analyze_realistic_multilingual.py",
                "--input",
                f"{model['label']}={multi_path}",
                "--output-dir",
                str(ml_out),
            ]
        )
        ready.append(
            {
                **model,
                "image_summary": read_json(image_out / "summary.json"),
                "ml_summary": read_json(ml_out / "summary.json"),
            }
        )

    summary = {"statuses": statuses, "ready": [item["label"] for item in ready]}
    (OUT_DIR / "status.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# OpenAI closed-model ROLECUE-192 reference",
        "",
        "| Model | Image rows | Text+joint rows | Parse failures | Complete |",
        "|---|---:|---:|---:|---|",
    ]
    for status in statuses:
        lines.append(
            f"| {status['label']} | {status['image_rows']}/384 | "
            f"{status['multi_rows']}/13824 | {status['parse_failures']} | "
            f"{'yes' if status['complete'] else 'no'} |"
        )
    (OUT_DIR / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if ready:
        (TABLE_DIR / "table_openai_192_reference.tex").write_text(
            build_joint_pf_table(ready), encoding="utf-8"
        )
        (TABLE_DIR / "table_openai_192_text_reference.tex").write_text(
            build_text_pf_table(ready), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
