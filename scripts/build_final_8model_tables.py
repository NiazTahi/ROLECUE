#!/usr/bin/env python3
"""Build frozen ROLECUE 8-model result tables for the WACV draft."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path("results/rolecue")
OUT = ROOT / "rolecue96_final_8model_tables"

MODELS = [
    {
        "label": "Qwen3-VL-8B",
        "set": "full",
        "image_summary": ROOT / "rolecue96_wave1_image_gate/analysis_qwen3_vl_8b/summary.json",
        "ml_summary": ROOT / "rolecue96_wave1_multilingual/analysis_qwen3_vl_8b/summary.json",
    },
    {
        "label": "Gemma-4-12B-it",
        "set": "full",
        "image_summary": ROOT / "rolecue96_wave1_image_gate/analysis_gemma_4_12b/summary.json",
        "ml_summary": ROOT / "rolecue96_wave1_multilingual/analysis_gemma_4_12b/summary.json",
    },
    {
        "label": "InternVL3.5-8B",
        "set": "no-chasing",
        "image_summary": ROOT / "rolecue96_wave1_image_gate/analysis_internvl3_5_8b_no_chasing/summary.json",
        "ml_summary": ROOT / "rolecue96_wave1_multilingual/analysis_internvl3_5_8b_no_chasing/summary.json",
    },
    {
        "label": "LLaVA-OneVision-7B",
        "set": "no-chasing",
        "image_summary": ROOT / "rolecue96_wave1_image_gate/analysis_llava_onevision_7b_no_chasing/summary.json",
        "ml_summary": ROOT / "rolecue96_wave1_multilingual/analysis_llava_onevision_7b_no_chasing/summary.json",
    },
    {
        "label": "MiniCPM-V-4.5",
        "set": "no-chasing",
        "image_summary": ROOT / "rolecue96_wave1_image_gate/analysis_minicpm_v45_no_chasing/summary.json",
        "ml_summary": ROOT / "rolecue96_wave1_multilingual/analysis_minicpm_v45_no_chasing/summary.json",
    },
    {
        "label": "Qwen3-VL-32B",
        "set": "full",
        "image_summary": ROOT / "rolecue96_wave2_a100/analysis_qwen3_vl_32b_image_gate/summary.json",
        "ml_summary": ROOT / "rolecue96_wave2_a100/analysis_qwen3_vl_32b_multilingual/summary.json",
    },
    {
        "label": "Qwen2.5-VL-32B",
        "set": "full",
        "image_summary": ROOT / "rolecue96_wave2_a100/analysis_qwen2_5_vl_32b_image_gate/summary.json",
        "ml_summary": ROOT / "rolecue96_wave2_a100/analysis_qwen2_5_vl_32b_multilingual/summary.json",
    },
    {
        "label": "InternVL3.5-38B",
        "set": "full",
        "image_summary": ROOT / "rolecue96_wave2_a100/analysis_internvl3_5_38b_hf_image_gate/summary.json",
        "ml_summary": ROOT / "rolecue96_wave2_a100/analysis_internvl3_5_38b_hf_multilingual/summary.json",
    },
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(value: float | None) -> str:
    if value is None:
        return "--"
    return f"{100 * value:.1f}"


def md_pct(value: float | None) -> str:
    return pct(value) + ("" if value is None else "%")


def ml_lookup(summary: dict[str, Any], task: str, language: str, order: str) -> dict[str, Any]:
    rows = summary.get("by_task_language_order", summary.get("main", []))
    for row in rows:
        if row["task"] == task and row["language"] == language and row["order"] == order:
            return row
    raise KeyError((task, language, order))


def tex_table_visual(rows: list[dict[str, Any]]) -> str:
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{4pt}",
        "\\begin{tabular}{lccccc}",
        "\\toprule",
        "Model & Set & Acc. & Reversal & Chasing & Gate \\\\",
        "\\midrule",
    ]
    for row in rows:
        gate = "\\cmark" if row["gate"] == "pass" else ("no-chasing" if row["gate"] == "no-chasing" else row["gate"])
        lines.append(
            f"{row['model']} & {row['set']} & {pct(row['accuracy'])} & "
            f"{pct(row['role_reversal_success'])} & {pct(row['chasing_accuracy'])} & {gate} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Image-only visual-role gate for the frozen 8-model main set. Values are percentages. Models marked no-chasing are evaluated on the 11-action visual-control subset in downstream integration tables because their image-only predictions on \\emph{chasing} are unreliable.}",
        "\\label{tab:visual-gate}",
        "\\end{table*}",
    ]
    return "\n".join(lines) + "\n"


def tex_table_joint(rows: list[dict[str, Any]]) -> str:
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{3.2pt}",
        "\\begin{tabular}{llrrrrrr}",
        "\\toprule",
        "Model & Set & \\multicolumn{2}{c}{German} & \\multicolumn{2}{c}{Japanese} & \\multicolumn{2}{c}{Turkish} \\\\",
        " & & Agent-first & Patient-first & Agent-first & Patient-first & Agent-first & Patient-first \\\\",
        "\\midrule",
    ]
    for row in rows:
        vals = row["joint"]
        lines.append(
            f"{row['model']} & {row['set']} & {pct(vals['de_agent_first'])} & {pct(vals['de_patient_first'])} & "
            f"{pct(vals['ja_agent_first'])} & {pct(vals['ja_patient_first'])} & "
            f"{pct(vals['tr_agent_first'])} & {pct(vals['tr_patient_first'])} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Direct joint image--sentence matching accuracy by language and word order for the frozen 8-model main set. Values are percentages after collapsing reversed answer mappings.}",
        "\\label{tab:joint-main}",
        "\\end{table*}",
    ]
    return "\n".join(lines) + "\n"


def tex_table_text_pf(rows: list[dict[str, Any]]) -> str:
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{3.5pt}",
        "\\begin{tabular}{lccc}",
        "\\toprule",
        "Model & de & ja & tr \\\\",
        "\\midrule",
    ]
    for row in rows:
        vals = row["text"]
        lines.append(
            f"{row['model']} & {pct(vals['de_patient_first'])} & {pct(vals['ja_patient_first'])} & {pct(vals['tr_patient_first'])} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Text-only accuracy on patient-first sentences. Values are percentages. Comparing this table with Table~\\ref{tab:joint-main} separates sentence-role parsing failures from multimodal integration failures.}",
        "\\label{tab:text-only}",
        "\\end{table}",
    ]
    return "\n".join(lines) + "\n"


def tex_table_modular_selected(ci_rows: list[dict[str, Any]]) -> str:
    # Select compact, interpretable rows: high component competence with positive gain,
    # plus Qwen2.5 German as a text-failure counterexample.
    wanted = [
        ("Qwen3-VL-8B", "ja", "agent_first"),
        ("Qwen3-VL-8B", "tr", "patient_first"),
        ("Gemma-4-12B-it", "de", "patient_first"),
        ("InternVL3.5-8B", "ja", "patient_first"),
        ("LLaVA-OneVision-7B", "ja", "agent_first"),
        ("MiniCPM-V-4.5", "ja", "patient_first"),
        ("Qwen2.5-VL-32B", "de", "patient_first"),
        ("InternVL3.5-38B", "tr", "agent_first"),
        ("Qwen3-VL-32B", "tr", "agent_first"),
    ]
    index = {(r["model"], r["language"], r["order"]): r for r in ci_rows}
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{3.2pt}",
        "\\begin{tabular}{llrrrrr}",
        "\\toprule",
        "Model & Setting & Direct & Image & Text & Modular & Gain [95\\% CI] \\\\",
        "\\midrule",
    ]
    lang_name = {"de": "de", "ja": "ja", "tr": "tr"}
    order_name = {"agent_first": "agent-first", "patient_first": "patient-first"}
    for key in wanted:
        r = index[key]
        lo, hi = r["gain_ci95"]
        lines.append(
            f"{r['model']} & {lang_name[r['language']]}, {order_name[r['order']]} & "
            f"{pct(r['direct_accuracy'])} & {pct(r['image_accuracy'])} & {pct(r['text_accuracy'])} & "
            f"{pct(r['modular_accuracy'])} & {pct(r['gain'])} [{pct(lo)}, {pct(hi)}] \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Selected enforced modular inference results. Direct is one multimodal yes/no call; Modular compares the model's separate image-only and text-only role predictions outside the model. Positive gains with strong Image and Text scores indicate integration failures, while weak Text scores expose component limitations.}",
        "\\label{tab:modular}",
        "\\end{table*}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in MODELS:
        image = read_json(item["image_summary"])
        ml = read_json(item["ml_summary"])
        joint = {}
        text = {}
        for lang in ("de", "ja", "tr"):
            for order in ("agent_first", "patient_first"):
                key = f"{lang}_{order}"
                joint[key] = ml_lookup(ml, "joint_match", lang, order)["case_accuracy"]
                text[key] = ml_lookup(ml, "text_only", lang, order)["case_accuracy"]
        chasing = image.get("accuracy_by_action", {}).get("chasing")
        gate = "pass" if item["set"] == "full" and image.get("gate_pass") else item["set"]
        rows.append(
            {
                "model": item["label"],
                "set": item["set"],
                "accuracy": image["accuracy"],
                "role_reversal_success": image["role_reversal_success"],
                "chasing_accuracy": chasing,
                "gate": gate,
                "joint": joint,
                "text": text,
            }
        )

    ci_rows = read_json(ROOT / "rolecue96_final_8model_modular/bootstrap_modular_gains.json")
    payload = {"models": rows, "modular_ci": ci_rows}
    (OUT / "final_8model_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = [
        "# ROLECUE final 8-model frozen tables",
        "",
        "## Visual gate",
        "",
        "| Model | Set | Accuracy | Reversal | Chasing | Gate |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        md.append(
            f"| {row['model']} | {row['set']} | {md_pct(row['accuracy'])} | "
            f"{md_pct(row['role_reversal_success'])} | {md_pct(row['chasing_accuracy'])} | {row['gate']} |"
        )
    md += [
        "",
        "## Joint accuracy",
        "",
        "| Model | Set | de AF | de PF | ja AF | ja PF | tr AF | tr PF |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        vals = row["joint"]
        md.append(
            f"| {row['model']} | {row['set']} | {md_pct(vals['de_agent_first'])} | {md_pct(vals['de_patient_first'])} | "
            f"{md_pct(vals['ja_agent_first'])} | {md_pct(vals['ja_patient_first'])} | "
            f"{md_pct(vals['tr_agent_first'])} | {md_pct(vals['tr_patient_first'])} |"
        )
    md += [
        "",
        "## Patient-first text-only accuracy",
        "",
        "| Model | de | ja | tr |",
        "|---|---:|---:|---:|",
    ]
    for row in rows:
        vals = row["text"]
        md.append(
            f"| {row['model']} | {md_pct(vals['de_patient_first'])} | {md_pct(vals['ja_patient_first'])} | {md_pct(vals['tr_patient_first'])} |"
        )
    (OUT / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    (OUT / "table_visual_gate.tex").write_text(tex_table_visual(rows), encoding="utf-8")
    (OUT / "table_joint_main.tex").write_text(tex_table_joint(rows), encoding="utf-8")
    (OUT / "table_text_patient_first.tex").write_text(tex_table_text_pf(rows), encoding="utf-8")
    (OUT / "table_modular_selected.tex").write_text(tex_table_modular_selected(ci_rows), encoding="utf-8")
    print(f"Wrote final tables to {OUT}")


if __name__ == "__main__":
    main()
