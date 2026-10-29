from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from nltk.corpus import wordnet as wn


DEFAULT_VERB_ROLES = {
    "carrying": "item",
    "chasing": "chasee",
    "dragging": "item",
    "kicking": "victim",
    "lifting": "item",
    "pushing": "item",
    "tackling": "victim",
}


def _majority(frames: list[dict[str, str]], role: str) -> tuple[str | None, int]:
    counts = Counter(frame.get(role) for frame in frames if frame.get(role))
    return counts.most_common(1)[0] if counts else (None, 0)


def _is_person(synset_id: str | None) -> bool:
    if not synset_id or not synset_id.startswith("n"):
        return False
    try:
        synset = wn.synset_from_pos_and_offset("n", int(synset_id[1:]))
    except (LookupError, ValueError):
        return False
    return synset.lexname() == "noun.person"


def _area(box: list[int]) -> int:
    return max(0, box[2] - box[0]) * max(0, box[3] - box[1])


def _iou(first: list[int], second: list[int]) -> float:
    intersection = max(0, min(first[2], second[2]) - max(first[0], second[0])) * max(
        0, min(first[3], second[3]) - max(first[1], second[1])
    )
    union = _area(first) + _area(second) - intersection
    return intersection / union if union else 0.0


def _center_distance(first: list[int], second: list[int], width: int, height: int) -> float:
    first_center = ((first[0] + first[2]) / 2, (first[1] + first[3]) / 2)
    second_center = ((second[0] + second[2]) / 2, (second[1] + second[3]) / 2)
    diagonal = math.hypot(width, height)
    return math.dist(first_center, second_center) / diagonal if diagonal else 0.0


def _gloss(space: dict[str, Any], synset_id: str | None) -> list[str]:
    if not synset_id:
        return []
    return space["nouns"].get(synset_id, {}).get("gloss", [])


def _stable_jitter(name: str, seed: int) -> float:
    digest = hashlib.sha256(f"{seed}:{name}".encode()).digest()
    return int.from_bytes(digest[:4], "big") / (2**32) * 1e-3


def iter_candidates(
    json_dir: Path,
    verb_roles: dict[str, str] | None = None,
    splits: Iterable[str] = ("dev", "test", "train"),
    min_agreement: int = 2,
    max_iou: float = 0.48,
    min_box_area_ratio: float = 0.012,
    min_center_distance: float = 0.06,
    seed: int = 2027,
) -> Iterable[dict[str, Any]]:
    verb_roles = verb_roles or DEFAULT_VERB_ROLES
    space = json.loads((json_dir / "imsitu_space.json").read_text(encoding="utf-8"))

    for split in splits:
        annotations = json.loads((json_dir / f"{split}.json").read_text(encoding="utf-8"))
        for image_name, annotation in annotations.items():
            verb = annotation["verb"]
            if verb not in verb_roles:
                continue
            patient_role = verb_roles[verb]
            boxes = annotation.get("bb", {})
            if "agent" not in boxes or patient_role not in boxes:
                continue
            agent_box = boxes["agent"]
            patient_box = boxes[patient_role]
            if len(agent_box) != 4 or len(patient_box) != 4:
                continue
            if min(agent_box) < 0 or min(patient_box) < 0:
                continue

            agent_synset, agent_agreement = _majority(annotation["frames"], "agent")
            patient_synset, patient_agreement = _majority(annotation["frames"], patient_role)
            if min(agent_agreement, patient_agreement) < min_agreement:
                continue
            if not (_is_person(agent_synset) and _is_person(patient_synset)):
                continue

            width = annotation["width"]
            height = annotation["height"]
            image_area = width * height
            agent_area_ratio = _area(agent_box) / image_area
            patient_area_ratio = _area(patient_box) / image_area
            overlap = _iou(agent_box, patient_box)
            separation = _center_distance(agent_box, patient_box, width, height)
            if min(agent_area_ratio, patient_area_ratio) < min_box_area_ratio:
                continue
            if overlap > max_iou or separation < min_center_distance:
                continue

            # Prefer annotator consensus, visible people, low box overlap, and spatial separation.
            quality = (
                (agent_agreement + patient_agreement) / 6
                + min(0.25, min(agent_area_ratio, patient_area_ratio))
                + min(0.35, separation)
                - 0.5 * overlap
                + _stable_jitter(image_name, seed)
            )
            yield {
                "candidate_id": image_name.removesuffix(".jpg"),
                "source": "SWiG",
                "source_commit": "70f2cb63aae3f4309bcb520eea1e14805e8c6c42",
                "split": split,
                "image_name": image_name,
                "verb": verb,
                "patient_role": patient_role,
                "width": width,
                "height": height,
                "agent_box": agent_box,
                "patient_box": patient_box,
                "agent_synset": agent_synset,
                "patient_synset": patient_synset,
                "agent_gloss": _gloss(space, agent_synset),
                "patient_gloss": _gloss(space, patient_synset),
                "agent_agreement": agent_agreement,
                "patient_agreement": patient_agreement,
                "agent_area_ratio": round(agent_area_ratio, 6),
                "patient_area_ratio": round(patient_area_ratio, 6),
                "box_iou": round(overlap, 6),
                "center_distance": round(separation, 6),
                "quality_score": round(quality, 6),
                "curation_status": "pending",
            }


def select_candidates(
    candidates: Iterable[dict[str, Any]], limit_per_verb: int
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for candidate in candidates:
        grouped.setdefault(candidate["verb"], []).append(candidate)
    selected: list[dict[str, Any]] = []
    for verb in sorted(grouped):
        ranked = sorted(grouped[verb], key=lambda row: (-row["quality_score"], row["candidate_id"]))
        selected.extend(ranked[:limit_per_verb])
    return selected
