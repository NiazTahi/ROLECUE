#!/usr/bin/env python3
"""Build ROLECUE-192 supplementary LaTeX tables from analysis summaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = ROOT / "results" / "rolecue" / "rolecue192_final_8model_multilingual"
TABLE_DIR = ROOT / "wacv-2027-author-kit-template" / "tables"

MODELS = [
    ("qwen3_vl_8b", "Qwen3-8B", "full"),
    ("gemma_4_12b", "Gemma-12B", "full"),
    ("internvl3_5_8b", "InternVL-8B", "noC"),
    ("llava_onevision_7b", "LLaVA-7B", "noC"),
    ("minicpm_v45", "MiniCPM", "noC"),
    ("qwen2_5_vl_32b", "Qwen2.5-32B", "noC"),
    ("qwen3_vl_32b", "Qwen3-32B", "full"),
    ("internvl3_5_38b_hf", "InternVL-38B", "full"),
]

LANGS = ["de", "ja", "tr", "en", "ko", "bn"]
LANG_LABEL = {
    "de": "German",
    "ja": "Japanese",
    "tr": "Turkish",
    "en": "English",
    "ko": "Korean",
    "bn": "Bangla",
}


def pct(x: float) -> str:
    return f"{100.0 * x:.1f}"


def load_rows() -> dict[tuple[str, str, str], dict[str, float]]:
    rows: dict[tuple[str, str, str], dict[str, float]] = {}
    for slug, _model_name, _primary_set in MODELS:
        path = ANALYSIS_DIR / f"analysis_{slug}" / "summary.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data["main"]:
            key = (slug, row["task"], row["language"], row["order"])
            rows[key] = row
    return rows


def write_task_order_table(rows, task: str, order: str, filename: str, caption: str, label: str) -> None:
    order_label = "agent-first" if order == "agent_first" else "patient-first"
    lines = [
        "\\begin{table}[H]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{2.0pt}",
        "\\resizebox{\\columnwidth}{!}{%",
        "\\begin{tabular}{llrrrrrr}",
        "\\toprule",
        "Model & Set & de & ja & tr & en & ko & bn \\\\",
        "\\midrule",
    ]
    for slug, model_name, primary_set in MODELS:
        values = []
        for lang in LANGS:
            row = rows[(slug, task, lang, order)]
            values.append(pct(row["case_accuracy"]))
        lines.append(f"{model_name} & {primary_set} & " + " & ".join(values) + " \\\\")
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "}%",
            f"\\caption{{{caption} Values are percentages; noC denotes the no-chasing visual-control subset.}}",
            f"\\label{{{label}}}",
            "\\end{table}",
            "",
        ]
    )
    (TABLE_DIR / filename).write_text("\n".join(lines), encoding="utf-8")


def write_joint_match_bias_table(rows) -> None:
    """Write a compact table exposing match/mismatch asymmetry for selected failures."""
    selected = [
        ("qwen3_vl_8b", "ja", "agent_first"),
        ("qwen3_vl_8b", "tr", "patient_first"),
        ("internvl3_5_8b", "ja", "patient_first"),
        ("internvl3_5_8b", "tr", "agent_first"),
        ("llava_onevision_7b", "ko", "agent_first"),
        ("minicpm_v45", "tr", "patient_first"),
        ("qwen2_5_vl_32b", "de", "patient_first"),
    ]
    by_model = {slug: name for slug, name, _set in MODELS}
    by_set = {slug: primary_set for slug, _name, primary_set in MODELS}
    # Need joint_by_match rows, which are inside each per-model summary.
    lookup = {}
    for slug, _name, _set in MODELS:
        path = ANALYSIS_DIR / f"analysis_{slug}" / "summary.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data["joint_by_match"]:
            lookup[(slug, row["language"], row["order"], bool(row["is_match"]))] = row

    lines = [
        "\\begin{table}[H]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{2.0pt}",
        "\\resizebox{\\columnwidth}{!}{%",
        "\\begin{tabular}{lllrrr}",
        "\\toprule",
        "Model & Set & Setting & Match & Mismatch & Gap \\\\",
        "\\midrule",
    ]
    for slug, lang, order in selected:
        match = lookup[(slug, lang, order, True)]["case_accuracy"]
        mismatch = lookup[(slug, lang, order, False)]["case_accuracy"]
        gap = match - mismatch
        order_short = "AF" if order == "agent_first" else "PF"
        setting = f"{lang}, {order_short}"
        lines.append(
            f"{by_model[slug]} & {by_set[slug]} & {setting} & "
            f"{pct(match)} & {pct(mismatch)} & {100.0 * gap:+.1f} \\\\"
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "}%",
            "\\caption{Selected match/mismatch asymmetries in direct joint inference. A large positive gap means the model is much better when the sentence agrees with the image than when it must reject a mismatching sentence, consistent with semantic-match bias rather than pure language parsing failure. Values are percentages.}",
            "\\label{tab:supp-match-bias}",
            "\\end{table}",
            "",
        ]
    )
    (TABLE_DIR / "table_supp_match_bias.tex").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    write_task_order_table(
        rows,
        "joint_match",
        "agent_first",
        "table_supp_joint_agent_first.tex",
        "Agent-first direct joint image--sentence matching accuracy on ROLECUE-192.",
        "tab:supp-joint-af",
    )
    write_task_order_table(
        rows,
        "joint_match",
        "patient_first",
        "table_supp_joint_patient_first.tex",
        "Patient-first direct joint image--sentence matching accuracy on ROLECUE-192.",
        "tab:supp-joint-pf",
    )
    write_task_order_table(
        rows,
        "text_only",
        "agent_first",
        "table_supp_text_agent_first.tex",
        "Agent-first text-only role-parsing accuracy on ROLECUE-192.",
        "tab:supp-text-af",
    )
    write_task_order_table(
        rows,
        "text_only",
        "patient_first",
        "table_supp_text_patient_first.tex",
        "Patient-first text-only role-parsing accuracy on ROLECUE-192.",
        "tab:supp-text-pf",
    )
    write_joint_match_bias_table(rows)


if __name__ == "__main__":
    main()
