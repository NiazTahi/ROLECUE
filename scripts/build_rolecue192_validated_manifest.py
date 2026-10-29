#!/usr/bin/env python3
"""Build ROLECUE-192 manifests from validated images and validated language CSV.

This intentionally does not regenerate any multilingual sentence.  The sentence
source of truth is the native/revalidated six-language CSV.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Iterable


IMAGE_RE = re.compile(
    r"^(?P<event>push|kicking|photographing|feeding|bandaging|chasing|carrying|lifting|dragging|washing|hugging|tickling)"
    r"(?:_s(?P<seed>[0-9]+))?_"
    r"(?P<visual_agent>red|blue)_agent_(?P<side>left|right)\.png$"
)

EVENT_TO_ACTION = {
    "push": "pushing",
    "kicking": "kicking",
    "photographing": "photographing",
    "feeding": "feeding",
    "bandaging": "bandaging",
    "chasing": "chasing",
    "carrying": "carrying",
    "lifting": "lifting",
    "dragging": "dragging",
    "washing": "washing",
    "hugging": "hugging",
    "tickling": "tickling",
}


def other(color: str) -> str:
    return "blue" if color == "red" else "red"


def other_side(side: str) -> str:
    return "right" if side == "left" else "left"


def write_jsonl(path: Path, rows: Iterable[dict[str, object]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def load_language_rows(path: Path) -> dict[tuple[str, str, str, str], dict[str, str]]:
    rows: dict[tuple[str, str, str, str], dict[str, str]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (
                row["language"],
                row["action"],
                row["sentence_agent_color"],
                row["order"],
            )
            if key in rows:
                raise ValueError(f"Duplicate language row: {key}")
            rows[key] = row
    return rows


def image_rows(images_dirs: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for images_dir in images_dirs:
        for image in sorted(images_dir.glob("*.png")):
            match = IMAGE_RE.fullmatch(image.name)
            if not match:
                continue
            event = match.group("event")
            action = EVENT_TO_ACTION[event]
            visual_agent = match.group("visual_agent")
            side = match.group("side")
            seed = match.group("seed") or "1"
            red_side = side if visual_agent == "red" else other_side(side)
            candidate_id = image.stem
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "image_path": image.as_posix(),
                    "event": event,
                    "action": action,
                    "verb": action,
                    "seed": f"s{seed}",
                    "visual_agent_color": visual_agent,
                    "agent_side": side,
                    "red_side": red_side,
                    "stimulus_source": "rolecue192_validated",
                }
            )
    rows.sort(key=lambda r: (r["action"], r["candidate_id"]))
    return rows


def append_image_only(rows: list[dict[str, object]], base: dict[str, str]) -> None:
    for red_is_a in (True, False):
        option_a = "red" if red_is_a else "blue"
        option_b = other(option_a)
        variant = "map-redA" if red_is_a else "map-redB"
        rows.append(
            {
                **base,
                "task": "image_only",
                "semantic_stimulus_id": f"rolecue192_{base['candidate_id']}",
                "example_id": f"rolecue192_{base['candidate_id']}__image__{variant}",
                "option_variant": variant,
                "prompt": (
                    f"Which person is {base['action']} the other person? "
                    f"A: The person in {option_a}. B: The person in {option_b}. "
                    "Answer with only A or B."
                ),
                "correct_option": "A" if base["visual_agent_color"] == option_a else "B",
                "option_a_semantics": option_a,
                "option_b_semantics": option_b,
            }
        )


def append_text_and_joint(
    rows: list[dict[str, object]],
    image: dict[str, str],
    lang: dict[str, str],
) -> None:
    language = lang["language"]
    sentence_agent = lang["sentence_agent_color"]
    order = lang["order"]
    sentence = lang["sentence"]
    semantic_id = (
        f"rolecue192_{image['candidate_id']}__{language}"
        f"__sent-{sentence_agent}__{order}"
    )
    base = {
        **image,
        "semantic_stimulus_id": semantic_id,
        "language": language,
        "language_name": lang["language_name"],
        "instruction_style": "english",
        "sentence_agent_color": sentence_agent,
        "sentence": sentence,
        "order": order,
        "language_validation_id": lang["validation_id"],
        "language_source_status": lang["source_status"],
    }
    for red_is_a in (True, False):
        option_a = "red" if red_is_a else "blue"
        option_b = other(option_a)
        variant = "map-redA" if red_is_a else "map-redB"
        rows.append(
            {
                **base,
                "task": "text_only",
                "image_path": None,
                "example_id": f"{semantic_id}__text__{variant}",
                "option_variant": variant,
                "prompt": (
                    "According to the sentence, which person performs the action? "
                    f"A: The person in {option_a}. B: The person in {option_b}. "
                    f"Answer with only A or B.\nSentence: \"{sentence}\""
                ),
                "correct_option": "A" if sentence_agent == option_a else "B",
                "option_a_semantics": option_a,
                "option_b_semantics": option_b,
            }
        )
    is_match = sentence_agent == image["visual_agent_color"]
    for yes_is_a in (True, False):
        option_a = "yes" if yes_is_a else "no"
        option_b = "no" if yes_is_a else "yes"
        variant = "map-yesA" if yes_is_a else "map-yesB"
        rows.append(
            {
                **base,
                "task": "joint_match",
                "example_id": f"{semantic_id}__joint__{variant}",
                "option_variant": variant,
                "prompt": (
                    "Does the sentence correctly describe which person is performing "
                    "the action on the other person in the image? "
                    f"A: {option_a.capitalize()}. B: {option_b.capitalize()}. "
                    f"Answer with only A or B.\nSentence: \"{sentence}\""
                ),
                "correct_option": "A" if (is_match == yes_is_a) else "B",
                "option_a_semantics": option_a,
                "option_b_semantics": option_b,
                "is_match": is_match,
            }
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", type=Path, action="append", required=True)
    parser.add_argument("--language-csv", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    images = image_rows(args.images_dir)
    language = load_language_rows(args.language_csv)
    if len(images) != 192:
        raise ValueError(f"Expected 192 images, found {len(images)}")

    actions = sorted({image["action"] for image in images})
    languages = sorted({key[0] for key in language})
    missing = [
        (lang, action, agent, order)
        for lang in languages
        for action in actions
        for agent in ("red", "blue")
        for order in ("agent_first", "patient_first")
        if (lang, action, agent, order) not in language
    ]
    if missing:
        raise ValueError(f"Missing validated language rows, first: {missing[:10]}")

    image_manifest: list[dict[str, object]] = []
    full_manifest: list[dict[str, object]] = []
    for image in images:
        append_image_only(image_manifest, image)
        for lang_code in languages:
            for sentence_agent in ("red", "blue"):
                for order in ("agent_first", "patient_first"):
                    append_text_and_joint(
                        full_manifest,
                        image,
                        language[(lang_code, image["action"], sentence_agent, order)],
                    )

    all_manifest = [*image_manifest, *full_manifest]
    n_image = write_jsonl(args.output_dir / "rolecue192_image_gate.jsonl", image_manifest)
    n_full = write_jsonl(args.output_dir / "rolecue192_six_language_full.jsonl", all_manifest)
    n_multilingual = write_jsonl(
        args.output_dir / "rolecue192_six_language_text_joint.jsonl", full_manifest
    )
    summary = {
        "images": len(images),
        "actions": actions,
        "languages": languages,
        "image_only_rows": n_image,
        "text_joint_rows": n_multilingual,
        "full_rows": n_full,
        "tasks": {
            "image_only": sum(row["task"] == "image_only" for row in all_manifest),
            "text_only": sum(row["task"] == "text_only" for row in all_manifest),
            "joint_match": sum(row["task"] == "joint_match" for row in all_manifest),
        },
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "MANIFEST_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
