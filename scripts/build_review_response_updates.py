#!/usr/bin/env python3
"""Regenerate ROLECUE manuscript tables after final review audit."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "rolecue"
TABLE_DIR = ROOT / "wacv-2027-author-kit-template" / "tables"

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

LANGS = ["de", "ja", "tr", "en", "ko", "bn"]
LANG_FULL = {
    "de": "German",
    "ja": "Japanese",
    "tr": "Turkish",
    "en": "English",
    "ko": "Korean",
    "bn": "Bangla",
}
ORDER_FULL = {"agent_first": "Agent-first", "patient_first": "Patient-first"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}"


def fmt(value: float) -> str:
    text = pct(value)
    if value < 0.5:
        return f"\\rcfail{{{text}}}"
    if value >= 0.985:
        return f"\\rcbest{{{text}}}"
    return text


def rowcolor(i: int) -> str:
    return "\\rowcolor{rcStripe} " if i % 2 == 0 else ""


def tex_escape(text: str) -> str:
    return text.replace("&", "\\&")


def image_rows() -> list[dict[str, Any]]:
    rows = []
    for slug, label, primary_set in MODELS:
        summary = read_json(
            RESULTS / "rolecue192_final_image_gate_analysis" / f"analysis_{slug}" / "summary.json"
        )
        by_action = summary["accuracy_by_action"]
        primary_actions = list(by_action) if primary_set == "full" else [
            action for action in by_action if action != "chasing"
        ]
        primary_acc = sum(by_action[action] for action in primary_actions) / len(primary_actions)
        rows.append(
            {
                "model": label,
                "set": primary_set,
                "images": 192 if primary_set == "full" else 176,
                "primary_acc": primary_acc,
                "full_acc": summary["accuracy"],
                "chasing": by_action["chasing"],
                "gate": "\\textcolor{rcGreen}{\\cmark}"
                if primary_set == "full"
                else "\\textcolor{rcRed}{no-chasing}",
            }
        )
    return rows


def multilingual_lookup() -> dict[tuple[str, str, str, str], dict[str, Any]]:
    out = {}
    for slug, _label, _primary_set in MODELS:
        summary = read_json(
            RESULTS / "rolecue192_final_8model_multilingual" / f"analysis_{slug}" / "summary.json"
        )
        for row in summary["main"]:
            out[(slug, row["task"], row["language"], row["order"])] = row
    return out


def modular_groups() -> list[dict[str, Any]]:
    summary = read_json(RESULTS / "rolecue192_final_8model_modular" / "summary.json")
    by_group = summary["by_language_order"]
    ci_lookup = {}
    ci_path = RESULTS / "rolecue192_final_8model_modular" / "bootstrap_modular_gains.json"
    if ci_path.exists():
        for row in read_json(ci_path):
            ci_lookup[(row["model"], row["language"], row["order"])] = row["gain_ci95"]

    yes_counts: dict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    consistency: dict[tuple[str, str, str], list[bool]] = defaultdict(list)
    for row in read_jsonl(RESULTS / "rolecue192_final_8model_modular" / "collapsed_modular.jsonl"):
        key = (row["model"], row["language"], row["order"])
        yes_counts[key][row["direct_prediction"]] += 1
        consistency[key].append(bool(row.get("direct_option_consistent")))

    enriched = []
    for row in by_group:
        key = (row["model"], row["language"], row["order"])
        counts = yes_counts[key]
        total = sum(counts.values())
        yes_rate = counts["yes"] / total if total else 0.0
        option_rate = sum(consistency[key]) / len(consistency[key]) if consistency[key] else 0.0
        out = dict(row)
        out["yes_rate"] = yes_rate
        out["option_consistency"] = option_rate
        out["gain_ci95"] = ci_lookup.get(key)
        enriched.append(out)
    return enriched


def write_visual_gate() -> None:
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{3.5pt}",
        "\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}lccrrrr@{}}",
        "\\toprule",
        "\\rowcolor{rcHeader}",
        "\\textbf{Model} & \\textbf{Primary set} & \\textbf{Images} & \\textbf{Primary acc.} & \\textbf{Full acc.} & \\textbf{Chasing} & \\textbf{Gate} \\\\",
        "\\midrule",
    ]
    for i, row in enumerate(image_rows()):
        lines.append(
            f"{rowcolor(i)}{row['model']} & {row['set']} & {row['images']} & "
            f"{fmt(row['primary_acc'])} & {fmt(row['full_acc'])} & {fmt(row['chasing'])} & {row['gate']} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular*}",
        "\\caption{Image-only visual-role gate on \\rolecue-192. Primary acc. is computed on the set used for integration analysis: all 192 images for full-set models and the 176-image no-chasing subset for restricted models. Full acc. is shown for transparency, and Chasing gives the action-level score that determines the subset.}",
        "\\label{tab:visual-gate}",
        "\\end{table*}",
    ]
    (TABLE_DIR / "table_visual_gate.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_text_patient_first() -> None:
    lookup = multilingual_lookup()
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{2.4pt}",
        "\\begin{tabular*}{\\columnwidth}{@{\\extracolsep{\\fill}}lrrrrrr@{}}",
        "\\toprule",
        "\\rowcolor{rcHeader}",
        "\\textbf{Model} & \\textbf{German} & \\textbf{Japanese} & \\textbf{Turkish} & \\textbf{English} & \\textbf{Korean} & \\textbf{Bangla} \\\\",
        "\\midrule",
    ]
    for i, (slug, label, _primary_set) in enumerate(MODELS):
        vals = [lookup[(slug, "text_only", lang, "patient_first")]["case_accuracy"] for lang in LANGS]
        lines.append(f"{rowcolor(i)}{label} & " + " & ".join(fmt(v) for v in vals) + " \\\\")
    lines += [
        "\\bottomrule",
        "\\end{tabular*}",
        "\\caption{Patient-first text-only role-parsing accuracy. Values are computed over unique sentence templates per language/order condition (24 for full-set models, 22 for no-chasing models). Comparing this table with Figure~\\ref{fig:diagnostic-overview}(a) separates sentence-role parsing failures from joint matching failures.}",
        "\\label{tab:text-only}",
        "\\end{table}",
    ]
    (TABLE_DIR / "table_text_patient_first.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def nonconstant(row: dict[str, Any]) -> bool:
    return 0.025 < row["yes_rate"] < 0.975


def write_fusion_gap() -> None:
    rows = [
        row
        for row in modular_groups()
        if min(row["image_accuracy"], row["text_accuracy"]) >= 0.85
        and row["modular_gain_strict"] >= 0.08
        and nonconstant(row)
    ]
    rows.sort(key=lambda row: row["modular_gain_strict"], reverse=True)
    rows = rows[:10]
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{3.0pt}",
        "\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}lllrrrrr@{}}",
        "\\toprule",
        "\\rowcolor{rcHeader}",
        "\\textbf{Model} & \\textbf{Language} & \\textbf{Order} & \\textbf{Image} & \\textbf{Text} & \\textbf{Joint} & \\textbf{Pred. match} & \\textbf{Gap} \\\\",
        "\\midrule",
    ]
    for i, row in enumerate(rows):
        lines.append(
            f"{rowcolor(i)}{row['model']} & {LANG_FULL[row['language']]} & {ORDER_FULL[row['order']]} & "
            f"{fmt(row['image_accuracy'])} & {fmt(row['text_accuracy'])} & {fmt(row['direct_accuracy'])} & "
            f"{pct(row['yes_rate'])} & \\rcfail{{\\textbf{{{pct(row['modular_gain_strict'])}}}}} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular*}",
        "\\caption{Largest non-degenerate integration gaps among settings with strong component performance. Gap is \\(\\min(\\mathrm{Image},\\mathrm{Text})-\\mathrm{Joint}\\). Pred. match is the percentage of direct-joint trials where the model predicts that the sentence matches the image; near-constant match cells are reported as response-compliance failures in the supplement.}",
        "\\label{tab:fusion-gaps}",
        "\\end{table*}",
    ]
    (TABLE_DIR / "table_fusion_gaps.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def selected_modular_rows() -> list[dict[str, Any]]:
    candidates = [
        row
        for row in modular_groups()
        if min(row["image_accuracy"], row["text_accuracy"]) >= 0.85
        and row["modular_gain_strict"] > 0
        and nonconstant(row)
    ]
    best_by_model = {}
    for row in candidates:
        current = best_by_model.get(row["model"])
        if current is None or row["modular_gain_strict"] > current["modular_gain_strict"]:
            best_by_model[row["model"]] = row
    rows = sorted(best_by_model.values(), key=lambda row: row["modular_gain_strict"], reverse=True)
    return rows[:6]


def write_modular_tables() -> None:
    rows = selected_modular_rows()
    lines = [
        "\\begin{table}[H]",
        "\\centering",
        "\\tiny",
        "\\setlength{\\tabcolsep}{1.4pt}",
        "\\begin{tabular*}{\\columnwidth}{@{\\extracolsep{\\fill}}lllrrr@{}}",
        "\\toprule",
        "\\rowcolor{rcHeader}",
        "\\textbf{Model} & \\textbf{Language} & \\textbf{Order} & \\textbf{Direct} & \\textbf{Modular} & \\textbf{Gain [95\\% CI]} \\\\",
        "\\midrule",
    ]
    for i, row in enumerate(rows):
        ci = row["gain_ci95"] or [row["modular_gain_strict"], row["modular_gain_strict"]]
        lines.append(
            f"{rowcolor(i)}{row['model']} & {LANG_FULL[row['language']]} & {ORDER_FULL[row['order']]} & "
            f"{pct(row['direct_accuracy'])} & {pct(row['modular_accuracy_strict'])} & "
            f"\\rcgain{{+{pct(row['modular_gain_strict'])} [{pct(ci[0])}, {pct(ci[1])}]}} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular*}",
        "\\caption{Selected non-degenerate enforced modular comparisons. Modular is a deterministic external comparison of the model's own image-only and text-only role predictions; the gain is therefore a readable presentation of the component--joint gap, not an independent model call.}",
        "\\label{tab:supp-modular}",
        "\\end{table}",
    ]
    (TABLE_DIR / "table_supp_modular_selected.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    main_lines = [line.replace("tab:supp-modular", "tab:modular") for line in lines]
    (TABLE_DIR / "table_modular_selected.tex").write_text("\n".join(main_lines) + "\n", encoding="utf-8")


def write_response_compliance() -> None:
    rows = []
    for row in modular_groups():
        if row["yes_rate"] >= 0.975 or row["yes_rate"] <= 0.025:
            rows.append(row)
    rows.sort(key=lambda row: (row["model"], row["language"], row["order"]))
    lines = [
        "\\begin{table}[H]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{2.5pt}",
        "\\begin{tabular*}{\\columnwidth}{@{\\extracolsep{\\fill}}lllrr@{}}",
        "\\toprule",
        "\\rowcolor{rcHeader}",
        "\\textbf{Model} & \\textbf{Language} & \\textbf{Order} & \\textbf{Joint} & \\textbf{Pred. match} \\\\",
        "\\midrule",
    ]
    for i, row in enumerate(rows[:12]):
        lines.append(
            f"{rowcolor(i)}{row['model']} & {LANG_FULL[row['language']]} & {ORDER_FULL[row['order']]} & "
            f"{pct(row['direct_accuracy'])} & {pct(row['yes_rate'])} \\\\"
        )
    lines += [
        "\\bottomrule",
        "\\end{tabular*}",
        "\\caption{Response-compliance diagnostics for direct joint inference. These rows are not treated as clean integration failures because the model almost always emits the same semantic answer. With balanced match/mismatch items, a constant ``yes'' policy yields chance accuracy.}",
        "\\label{tab:supp-response-compliance}",
        "\\end{table}",
    ]
    (TABLE_DIR / "table_supp_response_compliance.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_full_supp_tables() -> None:
    lookup = multilingual_lookup()
    blocks = [
        ("joint_match", "agent_first", "Agent-first direct joint accuracy.", "tab:supp-joint-af"),
        ("joint_match", "patient_first", "Patient-first direct joint accuracy.", "tab:supp-joint-pf"),
        ("text_only", "agent_first", "Agent-first text-only role-parsing accuracy.", "tab:supp-text-af"),
        ("text_only", "patient_first", "Patient-first text-only role-parsing accuracy.", "tab:supp-text-pf"),
    ]
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3.0pt}",
    ]
    for block_idx, (task, order, caption, label) in enumerate(blocks):
        if block_idx:
            lines.append("\\vspace{3pt}")
        lines += [
            "\\begin{subtable}{\\textwidth}",
            "\\centering",
            "\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}llrrrrrr@{}}",
            "\\toprule",
            "\\rowcolor{rcHeader}\\textbf{Model} & \\textbf{Set} & \\textbf{German} & \\textbf{Japanese} & \\textbf{Turkish} & \\textbf{English} & \\textbf{Korean} & \\textbf{Bangla} \\\\",
            "\\midrule",
        ]
        for i, (slug, label_name, primary_set) in enumerate(MODELS):
            vals = [lookup[(slug, task, lang, order)]["case_accuracy"] for lang in LANGS]
            lines.append(f"{rowcolor(i)}{label_name} & {primary_set} & " + " & ".join(fmt(v) for v in vals) + " \\\\")
        lines += [
            "\\bottomrule",
            "\\end{tabular*}",
            f"\\caption{{{caption}}}",
            f"\\label{{{label}}}",
            "\\end{subtable}",
            "",
        ]
    lines += [
        "\\caption{Full \\rolecue-192 direct joint and text-only results. Values are percentages. The full set contains all 12 actions; the no-chasing visual-control set contains 11 actions. Text-only percentages are over unique sentence templates per language/order condition.}",
        "\\label{tab:supp-full-results}",
        "\\end{table*}",
    ]
    (TABLE_DIR / "table_supp_full_results.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_model_inventory() -> None:
    rows = [
        ("Qwen3-VL-8B", "main", "full", "--"),
        ("Gemma-4-12B-it", "main", "full", "--"),
        ("InternVL3.5-8B", "main", "no-chasing", "--"),
        ("LLaVA-OneVision-7B", "main", "no-chasing", "--"),
        ("MiniCPM-V-4.5", "main", "no-chasing", "--"),
        ("Qwen2.5-VL-32B", "main", "no-chasing", "--"),
        ("Qwen3-VL-32B", "main", "full", "--"),
        ("InternVL3.5-38B", "main", "full", "--"),
        ("Aya-Vision-8B", "diagnostic", "\\rcfail{failed gate}", "81.2 full, 62.5 chasing"),
        ("GLM-4.1V-9B-Thinking", "diagnostic", "protocol probe", "0.0 option-map agreement"),
        ("Phi-4-RV-15B", "attempted", "\\rcfail{excluded}", "runtime stack incompatible"),
    ]
    lines = [
        "\\begin{center}",
        "\\tiny",
        "\\setlength{\\tabcolsep}{1.6pt}",
        "\\begin{tabular*}{\\columnwidth}{@{\\extracolsep{\\fill}}llll@{}}",
        "\\toprule",
        "\\rowcolor{rcHeader}\\textbf{Model} & \\textbf{Role} & \\textbf{Set} & \\textbf{Diagnostic note} \\\\",
        "\\midrule",
    ]
    for i, row in enumerate(rows):
        lines.append(f"{rowcolor(i)}{row[0]} & {row[1]} & {row[2]} & {row[3]} \\\\")
    lines += [
        "\\bottomrule",
        "\\end{tabular*}",
        "\\captionof{table}{Frozen model inventory. The eight main rows are the open-weight \\rolecue-192 comparison. Diagnostic/attempted rows make exclusions transparent.}",
        "\\label{tab:model-inventory-supp}",
        "\\end{center}",
    ]
    (TABLE_DIR / "table_supp_model_inventory.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    write_visual_gate()
    write_text_patient_first()
    write_fusion_gap()
    write_modular_tables()
    write_response_compliance()
    write_full_supp_tables()
    write_model_inventory()
    print("Wrote reviewed ROLECUE tables.")


if __name__ == "__main__":
    main()
