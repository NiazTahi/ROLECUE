from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Iterable

from rolecue.render import render_role_boxes
from rolecue.templates import (
    COLORS,
    ORDERS,
    make_image_prompt,
    make_joint_prompt,
    make_option_map,
    make_sentence,
    make_text_prompt,
)


def _bit(key: str) -> bool:
    return bool(hashlib.sha256(key.encode()).digest()[0] & 1)


def _other_color(color: str) -> str:
    return "blue" if color == "red" else "red"


def render_pilot_images(
    items: Iterable[dict[str, Any]], raw_images_dir: Path, output_dir: Path
) -> None:
    for item in items:
        source = raw_images_dir / item["image_name"]
        for visual_agent_color in COLORS:
            output = output_dir / f"{item['candidate_id']}__agent-{visual_agent_color}.jpg"
            render_role_boxes(
                source,
                output,
                item["agent_box"],
                item["patient_box"],
                (item["width"], item["height"]),
                visual_agent_color,
            )


def build_manifest(
    items: list[dict[str, Any]],
    rendered_images_dir: Path,
    languages: Iterable[str],
    instruction_styles: Iterable[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    instruction_styles = tuple(instruction_styles)
    for item in items:
        candidate_id = item["candidate_id"]
        for visual_agent_color in COLORS:
            image_name = f"{candidate_id}__agent-{visual_agent_color}.jpg"
            # Counterbalance the red/blue option mapping at the item level.
            image_options = make_option_map(_bit(f"image:{candidate_id}"))
            rows.append(
                {
                    "example_id": f"image__{candidate_id}__v-{visual_agent_color}",
                    "task": "image_only",
                    "candidate_id": candidate_id,
                    "verb": item["verb"],
                    "image_path": str(rendered_images_dir / image_name),
                    "visual_agent_color": visual_agent_color,
                    "prompt": make_image_prompt(item["verb"], image_options),
                    "correct_option": image_options.label_for(visual_agent_color == "red"),
                    "option_a_semantics": "red" if image_options.true_label == "A" else "blue",
                    "option_b_semantics": "blue" if image_options.true_label == "A" else "red",
                }
            )

        for language in languages:
            color_options = make_option_map(_bit(f"text:{candidate_id}:{language}"))
            truth_options = make_option_map(_bit(f"joint:{candidate_id}:{language}"))
            for case_agent_color in COLORS:
                for order in ORDERS:
                    sentence = make_sentence(language, item["verb"], case_agent_color, order)
                    for instruction_style in instruction_styles:
                        # Text controls are duplicated per item deliberately: item-clustered analysis
                        # keeps their lexical/action distribution aligned with the joint conditions.
                        rows.append(
                            {
                                "example_id": (
                                    f"text__{candidate_id}__{language}__c-{case_agent_color}"
                                    f"__o-{order}__i-{instruction_style}"
                                ),
                                "task": "text_only",
                                "candidate_id": candidate_id,
                                "verb": item["verb"],
                                "language": language,
                                "instruction_style": instruction_style,
                                "image_path": None,
                                "case_agent_color": case_agent_color,
                                "order": order,
                                "sentence": sentence,
                                "prompt": make_text_prompt(
                                    language, sentence, color_options, instruction_style
                                ),
                                "correct_option": color_options.label_for(
                                    case_agent_color == "red"
                                ),
                                "option_a_semantics": (
                                    "red" if color_options.true_label == "A" else "blue"
                                ),
                                "option_b_semantics": (
                                    "blue" if color_options.true_label == "A" else "red"
                                ),
                            }
                        )
                    for visual_agent_color in COLORS:
                        image_name = f"{candidate_id}__agent-{visual_agent_color}.jpg"
                        truth = visual_agent_color == case_agent_color
                        for instruction_style in instruction_styles:
                            rows.append(
                                {
                                    "example_id": (
                                        f"joint__{candidate_id}__{language}__v-{visual_agent_color}"
                                        f"__c-{case_agent_color}__o-{order}__i-{instruction_style}"
                                    ),
                                    "task": "joint_match",
                                    "candidate_id": candidate_id,
                                    "verb": item["verb"],
                                    "language": language,
                                    "instruction_style": instruction_style,
                                    "image_path": str(rendered_images_dir / image_name),
                                    "visual_agent_color": visual_agent_color,
                                    "case_agent_color": case_agent_color,
                                    "first_mentioned_color": (
                                        case_agent_color
                                        if order == "agent_first"
                                        else _other_color(case_agent_color)
                                    ),
                                    "order": order,
                                    "sentence": sentence,
                                    "truth": truth,
                                    "prompt": make_joint_prompt(
                                        language, sentence, truth_options, instruction_style
                                    ),
                                    "correct_option": truth_options.label_for(truth),
                                    "option_a_semantics": (
                                        "match" if truth_options.true_label == "A" else "mismatch"
                                    ),
                                    "option_b_semantics": (
                                        "mismatch" if truth_options.true_label == "A" else "match"
                                    ),
                                }
                            )
    rows.sort(key=lambda row: row["example_id"])
    return rows
