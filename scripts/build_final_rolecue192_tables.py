#!/usr/bin/env python3
"""Build ROLECUE-192 final 8-model tables for the WACV draft."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path("results/rolecue")
OUT = ROOT / "rolecue192_final_8model_tables"
TEX_OUT = Path("wacv-2027-author-kit-template/tables")

LANGS = [
    ("de", "de"),
    ("ja", "ja"),
    ("tr", "tr"),
    ("en", "en"),
    ("ko", "ko"),
    ("bn", "bn"),
]

MODELS = [
    ("qwen3_vl_8b", "Qwen3-VL-8B", "full"),
    ("gemma_4_12b", "Gemma-4-12B-it", "full"),
    ("internvl3_5_8b", "InternVL3.5-8B", "no-chasing"),
    ("llava_onevision_7b", "LLaVA-OneVision-7B", "no-chasing"),
    ("minicpm_v45", "MiniCPM-V-4.5", "no-chasing"),
    ("qwen2_5_vl_32b", "Qwen2.5-VL-32B", "no-chasing"),
    ("qwen3_vl_32b", "Qwen3-VL-32B", "full"),
    ("internvl3_5_38b_hf", "InternVL3.5-38B", "full"),
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(x: float | None) -> str:
    if x is None:
        return "--"
    return f"{100 * x:.1f}"


def md_pct(x: float | None) -> str:
    return pct(x) + ("" if x is None else "%")


def ml_row(summary: dict[str, Any], task: str, language: str, order: str) -> dict[str, Any]:
    for row in summary["main"]:
        if row["task"] == task and row["language"] == language and row["order"] == order:
            return row
    raise KeyError((task, language, order))


def tex_visual(rows: list[dict[str, Any]]) -> str:
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{4pt}",
        "\\begin{tabular}{lccccc}",
        "\\toprule",
        "Model & Primary set & Images & Acc. & Chasing & Gate \\\\",
        "\\midrule",
    ]
    for row in rows:
        gate = "\\cmark" if row["gate"] else "no-chasing"
        lines.append(
            f"{row['model']} & {row['set']} & {row['images']} & {pct(row['accuracy'])} & "
            f"{pct(row['chasing'])} & {gate} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Image-only visual-role gate on ROLECUE-192. Values are percentages after collapsing reversed A/B answer mappings. Models marked no-chasing are evaluated on the 11-action visual-control subset in the primary integration tables because their image-only predictions on \\emph{chasing} fall below the action gate.}",
        "\\label{tab:visual-gate}",
        "\\end{table*}",
    ]
    return "\n".join(lines) + "\n"


def tex_pf(rows: list[dict[str, Any]], key: str, caption: str, label: str) -> str:
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{3.2pt}",
        "\\begin{tabular}{llrrrrrr}",
        "\\toprule",
        "Model & Set & de & ja & tr & en & ko & bn \\\\",
        "\\midrule",
    ]
    for row in rows:
        vals = row[key]
        lines.append(
            f"{row['model']} & {row['set']} & "
            + " & ".join(pct(vals[lang]) for lang, _ in LANGS)
            + " \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\end{table*}",
    ]
    return "\n".join(lines) + "\n"


def tex_gap(rows: list[dict[str, Any]]) -> str:
    candidates: list[dict[str, Any]] = []
    for row in rows:
        for lang, _ in LANGS:
            for order in ("agent_first", "patient_first"):
                image = row["image_accuracy"]
                text = row["text_all"][(lang, order)]
                joint = row["joint_all"][(lang, order)]
                floor = min(image, text)
                gap = floor - joint
                if floor >= 0.85 and gap >= 0.15:
                    candidates.append(
                        {
                            "model": row["model"],
                            "setting": f"{lang}, {'AF' if order == 'agent_first' else 'PF'}",
                            "image": image,
                            "text": text,
                            "joint": joint,
                            "gap": gap,
                        }
                    )
    candidates.sort(key=lambda x: (-x["gap"], x["model"], x["setting"]))
    candidates = candidates[:12]
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{3.8pt}",
        "\\begin{tabular}{llrrrr}",
        "\\toprule",
        "Model & Setting & Image & Text & Joint & Gap \\\\",
        "\\midrule",
    ]
    for row in candidates:
        lines.append(
            f"{row['model']} & {row['setting']} & {pct(row['image'])} & {pct(row['text'])} & "
            f"{pct(row['joint'])} & {pct(row['gap'])} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\caption{Largest ROLECUE-192 integration gaps among settings with strong component performance. Gap is \\(\\min(\\mathrm{Image},\\mathrm{Text})-\\mathrm{Joint}\\). These are the settings where a joint error is least attributable to missing visual or text-only competence.}",
        "\\label{tab:fusion-gaps}",
        "\\end{table*}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TEX_OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for slug, label, primary_set in MODELS:
        image = read_json(ROOT / f"rolecue192_final_image_gate_analysis/analysis_{slug}/summary.json")
        ml = read_json(ROOT / f"rolecue192_final_8model_multilingual/analysis_{slug}/summary.json")
        text_pf = {lang: ml_row(ml, "text_only", lang, "patient_first")["case_accuracy"] for lang, _ in LANGS}
        joint_pf = {lang: ml_row(ml, "joint_match", lang, "patient_first")["case_accuracy"] for lang, _ in LANGS}
        text_all = {
            (lang, order): ml_row(ml, "text_only", lang, order)["case_accuracy"]
            for lang, _ in LANGS
            for order in ("agent_first", "patient_first")
        }
        joint_all = {
            (lang, order): ml_row(ml, "joint_match", lang, order)["case_accuracy"]
            for lang, _ in LANGS
            for order in ("agent_first", "patient_first")
        }
        rows.append(
            {
                "slug": slug,
                "model": label,
                "set": primary_set,
                "images": image["images"],
                "accuracy": image["accuracy"],
                "chasing": image["accuracy_by_action"].get("chasing"),
                "gate": primary_set == "full",
                "image_accuracy": image["accuracy"],
                "text_pf": text_pf,
                "joint_pf": joint_pf,
                "text_all": text_all,
                "joint_all": joint_all,
            }
        )

    serializable_rows = []
    for row in rows:
        serializable_rows.append(
            {
                key: value
                for key, value in row.items()
                if key not in {"text_all", "joint_all"}
            }
        )
    (OUT / "final_8model_rolecue192_summary.json").write_text(
        json.dumps(serializable_rows, indent=2), encoding="utf-8"
    )

    md = [
        "# ROLECUE-192 final 8-model tables",
        "",
        "## Visual gate",
        "",
        "| Model | Primary set | Images | Acc. | Chasing | Gate |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        md.append(
            f"| {row['model']} | {row['set']} | {row['images']} | {md_pct(row['accuracy'])} | "
            f"{md_pct(row['chasing'])} | {'pass' if row['gate'] else 'no-chasing'} |"
        )
    md += [
        "",
        "## Patient-first joint accuracy",
        "",
        "| Model | Set | de | ja | tr | en | ko | bn |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        md.append(
            f"| {row['model']} | {row['set']} | "
            + " | ".join(md_pct(row["joint_pf"][lang]) for lang, _ in LANGS)
            + " |"
        )
    md += [
        "",
        "## Patient-first text-only accuracy",
        "",
        "| Model | Set | de | ja | tr | en | ko | bn |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        md.append(
            f"| {row['model']} | {row['set']} | "
            + " | ".join(md_pct(row["text_pf"][lang]) for lang, _ in LANGS)
            + " |"
        )
    (OUT / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    (TEX_OUT / "table_visual_gate.tex").write_text(tex_visual(rows), encoding="utf-8")
    (TEX_OUT / "table_joint_main.tex").write_text(
        tex_pf(
            rows,
            "joint_pf",
            "Patient-first direct joint image--sentence matching accuracy on ROLECUE-192. Values are percentages after answer-map collapse. Full-set models use all 12 actions; no-chasing models use the 11-action visual-control subset.",
            "tab:joint-main",
        ),
        encoding="utf-8",
    )
    (TEX_OUT / "table_text_patient_first.tex").write_text(
        tex_pf(
            rows,
            "text_pf",
            "Patient-first text-only role-parsing accuracy on ROLECUE-192. Comparing this table with Table~\\ref{tab:joint-main} separates sentence-role parsing failures from multimodal integration failures.",
            "tab:text-only",
        ),
        encoding="utf-8",
    )
    (TEX_OUT / "table_fusion_gaps.tex").write_text(tex_gap(rows), encoding="utf-8")
    print(f"Wrote ROLECUE-192 tables to {OUT} and {TEX_OUT}")


if __name__ == "__main__":
    main()
