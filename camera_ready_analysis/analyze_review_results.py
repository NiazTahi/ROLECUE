"""Reproduce common-subset and exploratory held-out acceptance-bias analyses."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results/raw/rolecue192_final_8model_multilingual"
OUT = Path(__file__).resolve().parent
MODELS = [
    ("qwen3_vl_8b", "Qwen3-VL-8B"), ("gemma_4_12b", "Gemma-4-12B-it"),
    ("internvl3_5_8b", "InternVL3.5-8B"), ("llava_onevision_7b", "LLaVA-OneVision-7B"),
    ("minicpm_v45", "MiniCPM-V-4.5"), ("qwen2_5_vl_32b", "Qwen2.5-VL-32B"),
    ("qwen3_vl_32b", "Qwen3-VL-32B"), ("internvl3_5_38b_hf", "InternVL3.5-38B"),
]
LANGS = ["de", "ja", "tr", "en", "ko", "bn"]


def optimal_threshold(train):
    """Maximize training accuracy; >= threshold means match. Ties choose nearest zero."""
    scores = np.array([x["semantic_margin"] for x in train], dtype=float)
    truth = np.array([x["is_match"] for x in train], dtype=bool)
    values = np.unique(scores)
    thresholds = np.concatenate(([np.nextafter(values[0], -np.inf)], values,
                                  [np.nextafter(values[-1], np.inf)]))
    accuracy = np.array([np.mean((scores >= t) == truth) for t in thresholds])
    best = thresholds[accuracy == accuracy.max()]
    return float(sorted(best, key=lambda t: (abs(t), t))[0])


def auc(rows):
    pos = np.array([r["semantic_margin"] for r in rows if r["is_match"]])
    neg = np.array([r["semantic_margin"] for r in rows if not r["is_match"]])
    return float(((pos[:, None] > neg[None, :]) + .5 * (pos[:, None] == neg[None, :])).mean())


def main():
    common, bias, score = [], [], []
    for slug, label in MODELS:
        collapsed = [json.loads(line) for line in (RESULTS / f"analysis_{slug}/collapsed.jsonl").open(encoding="utf-8") if line.strip()]
        for lang in LANGS:
            for order in ("agent_first", "patient_first"):
                group = [r for r in collapsed if r["task"] == "joint_match" and r["action"] != "chasing" and r["language"] == lang and r["order"] == order]
                assert len(group) == 352 and len({r['candidate_id'] for r in group}) == 176
                common.append(dict(model=label, language=lang, order=order, images=176, decisions=len(group), accuracy=sum(r["case_correct"] for r in group)/len(group)))
                if any(r["semantic_margin"] is None for r in group):
                    continue
                actions = sorted({r["action"] for r in group})
                preds=[]
                for action in actions:
                    train = [r for r in group if r["action"] != action]
                    test = [r for r in group if r["action"] == action]
                    threshold = optimal_threshold(train)
                    preds.extend((r, r["semantic_margin"] >= threshold) for r in test)
                assert len(preds) == len(group)
                matching = [r for r in group if r["is_match"]]
                mismatch = [r for r in group if not r["is_match"]]
                bias.append(dict(model=label, language=lang, order=order, images=176, decisions=len(group),
                    direct_accuracy=sum(r["case_correct"] for r in group)/len(group),
                    match_acceptance=sum(r["semantic_prediction"] == "yes" for r in matching)/len(matching),
                    mismatch_acceptance=sum(r["semantic_prediction"] == "yes" for r in mismatch)/len(mismatch),
                    auc=auc(group), leave_one_action_out_accuracy=sum(pred == r["is_match"] for r,pred in preds)/len(preds)))
        groups=defaultdict(list)
        for line in (RESULTS / f"{slug}_multilingual_selected.jsonl").open(encoding="utf-8"):
            row=json.loads(line); groups[(row["task"],row["semantic_stimulus_id"])].append(row)
        for task in ("text_only", "joint_match"):
            pairs=[v for (t,_),v in groups.items() if t == task]
            counts=defaultdict(int)
            for pair in pairs:
                assert len(pair)==2
                focal="red" if task=="text_only" else "yes"
                sem=[];margins=[]
                for r in pair:
                    pred=r.get("prediction")
                    if pred not in ("A","B"): counts["parse_failures"]+=1; sem.append(None)
                    else: sem.append(r["option_a_semantics"] if pred=="A" else r["option_b_semantics"])
                    if r.get("logit_a") is not None and r.get("logit_b") is not None:
                        margins.append((r["logit_a"]-r["logit_b"])*(1 if r["option_a_semantics"]==focal else -1))
                if None in sem: counts["pairs_with_unparsed"]+=1
                elif sem[0]!=sem[1]: counts["hard_mapping_conflicts"]+=1
                if len(margins)==2 and sum(margins)==0: counts["zero_margin_pairs"]+=1
            score.append(dict(model=label, task=task, raw_rows=2*len(pairs), semantic_pairs=len(pairs), **{k:counts[k] for k in ("parse_failures","pairs_with_unparsed","hard_mapping_conflicts","zero_margin_pairs")}))
    for name, rows in [("common_no_chasing.csv",common),("acceptance_bias_heldout.csv",bias),("scoring_diagnostics.csv",score)]:
        with (OUT/name).open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    print(f"Wrote {len(common)} common-subset cells, {len(bias)} logit-bearing calibration cells, {len(score)} scoring rows")

if __name__ == "__main__": main()
