"""Procedural, paired visual-event stimuli for the ROLECUE controlled pilot."""

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageDraw


CANVAS = (768, 512)
ACTIONS = ("photographing", "pushing", "kicking", "pulling")
ROBOT_COLORS = {"red": "#d83a3a", "blue": "#2878d0"}
BACKGROUNDS = ("#f5f0e8", "#e9f3ef", "#edf0f7", "#f4edf5")


@dataclass(frozen=True)
class ControlledScene:
    scene_id: str
    action: str
    seed: int
    red_side: str
    agent_color: str
    background: str

    @property
    def patient_color(self) -> str:
        return "blue" if self.agent_color == "red" else "red"


def _mirror_x(x: float, direction: int) -> float:
    return x if direction == 1 else -x


def _line(draw: ImageDraw.ImageDraw, points, fill: str, width: int = 9) -> None:
    draw.line(points, fill=fill, width=width, joint="curve")


def _robot(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    color: str,
    facing: int,
    pose: str,
    scale: float,
) -> dict[str, tuple[float, float]]:
    """Draw a robot and return useful attachment points."""
    cx, cy = center
    ink = "#20252c"
    fill = ROBOT_COLORS[color]
    s = scale
    lean = facing * (10 * s if pose in {"push", "kick"} else 0)
    head_y = cy - 105 * s
    body_y = cy - 25 * s

    head = [cx - 39 * s + lean, head_y - 32 * s, cx + 39 * s + lean, head_y + 32 * s]
    draw.rounded_rectangle(head, radius=12 * s, fill=fill, outline=ink, width=max(3, int(5 * s)))
    eye_y = head_y - 4 * s
    for dx in (-15, 15):
        draw.ellipse(
            [cx + dx * s - 5 * s + lean, eye_y - 5 * s,
             cx + dx * s + 5 * s + lean, eye_y + 5 * s],
            fill="#f8fbff",
            outline=ink,
            width=max(1, int(2 * s)),
        )
    antenna_x = cx + lean
    _line(draw, [(antenna_x, head_y - 32 * s), (antenna_x, head_y - 49 * s)], ink, max(2, int(4 * s)))
    draw.ellipse([antenna_x - 6 * s, head_y - 59 * s, antenna_x + 6 * s, head_y - 47 * s], fill=fill, outline=ink)

    body = [cx - 48 * s, body_y - 50 * s, cx + 48 * s, body_y + 50 * s]
    draw.rounded_rectangle(body, radius=14 * s, fill=fill, outline=ink, width=max(3, int(5 * s)))
    draw.ellipse([cx - 10 * s, body_y - 10 * s, cx + 10 * s, body_y + 10 * s], fill="#f5d96f", outline=ink)

    shoulder = (cx + facing * 42 * s, body_y - 28 * s)
    rear_shoulder = (cx - facing * 42 * s, body_y - 28 * s)
    hand_forward = (cx + facing * 92 * s, body_y + 2 * s)
    hand_rear = (cx - facing * 70 * s, body_y + 13 * s)
    if pose in {"push", "camera", "pull"}:
        _line(draw, [shoulder, hand_forward], ink, max(5, int(10 * s)))
        _line(draw, [rear_shoulder, hand_rear], ink, max(5, int(10 * s)))
    else:
        _line(draw, [shoulder, (cx + facing * 72 * s, body_y + 15 * s)], ink, max(5, int(10 * s)))
        _line(draw, [rear_shoulder, hand_rear], ink, max(5, int(10 * s)))

    hip_y = body_y + 50 * s
    foot_y = cy + 104 * s
    if pose == "kick":
        kick_foot = (cx + facing * 104 * s, cy + 45 * s)
        _line(draw, [(cx + facing * 23 * s, hip_y), kick_foot], ink, max(6, int(12 * s)))
        _line(draw, [(cx - facing * 23 * s, hip_y), (cx - facing * 34 * s, foot_y)], ink, max(6, int(12 * s)))
    else:
        kick_foot = (cx + facing * 34 * s, foot_y)
        _line(draw, [(cx - 22 * s, hip_y), (cx - 30 * s, foot_y)], ink, max(6, int(12 * s)))
        _line(draw, [(cx + 22 * s, hip_y), (cx + 30 * s, foot_y)], ink, max(6, int(12 * s)))
    _line(draw, [(cx - 45 * s, foot_y), (cx - 18 * s, foot_y)], ink, max(5, int(10 * s)))
    if pose != "kick":
        _line(draw, [(cx + 18 * s, foot_y), (cx + 45 * s, foot_y)], ink, max(5, int(10 * s)))
    else:
        _line(draw, [kick_foot, (kick_foot[0] + facing * 25 * s, kick_foot[1])], ink, max(5, int(10 * s)))

    return {
        "hand_forward": hand_forward,
        "torso": (cx, body_y),
        "kick_foot": kick_foot,
        "waist": (cx, hip_y - 15 * s),
    }


def _motion_lines(draw: ImageDraw.ImageDraw, x: float, y: float, direction: int) -> None:
    for offset in (-25, 0, 25):
        _line(draw, [(x - direction * 18, y + offset), (x - direction * 60, y + offset)], "#68717c", 4)


def render_controlled_scene(scene: ControlledScene, output: Path) -> None:
    rng = random.Random(scene.seed)
    image = Image.new("RGB", CANVAS, scene.background)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 405, CANVAS[0], CANVAS[1]], fill="#d7d2c8")
    draw.line([(0, 405), (CANVAS[0], 405)], fill="#8b8b86", width=4)

    left_x = 215 + rng.randint(-12, 12)
    right_x = 553 + rng.randint(-12, 12)
    y = 294 + rng.randint(-5, 5)
    positions = {
        ("red" if scene.red_side == "left" else "blue"): (left_x, y),
        ("blue" if scene.red_side == "left" else "red"): (right_x, y),
    }
    agent_x, agent_y = positions[scene.agent_color]
    patient_x, patient_y = positions[scene.patient_color]
    direction = 1 if patient_x > agent_x else -1
    patient_direction = -direction
    scale = rng.uniform(0.92, 1.04)

    agent_pose = {
        "photographing": "camera",
        "pushing": "push",
        "kicking": "kick",
        "pulling": "pull",
    }[scene.action]
    agent = _robot(draw, (agent_x, agent_y), scene.agent_color, direction, agent_pose, scale)
    patient = _robot(draw, (patient_x, patient_y), scene.patient_color, patient_direction, "idle", scale)

    ink = "#20252c"
    if scene.action == "photographing":
        hx, hy = agent["hand_forward"]
        camera = [hx - 23, hy - 18, hx + 23, hy + 18]
        draw.rounded_rectangle(camera, radius=5, fill="#303945", outline=ink, width=3)
        lens_x = hx + direction * 22
        draw.ellipse([lens_x - 8, hy - 8, lens_x + 8, hy + 8], fill="#8ed2f2", outline=ink, width=2)
        px, py = patient["torso"]
        draw.line([(lens_x, hy), (px, py - 30)], fill="#e5b83b", width=3)
        draw.line([(lens_x, hy), (px, py + 30)], fill="#e5b83b", width=3)
    elif scene.action == "pushing":
        hx, hy = agent["hand_forward"]
        px, py = patient["torso"]
        _line(draw, [(hx, hy), (px - direction * 42, py - 5)], ink, 8)
        _motion_lines(draw, patient_x, patient_y - 15, direction)
    elif scene.action == "kicking":
        fx, fy = agent["kick_foot"]
        px, py = patient["torso"]
        _line(draw, [(fx, fy), (px - direction * 42, py + 35)], ink, 8)
        burst_x, burst_y = px - direction * 47, py + 35
        rays = []
        for angle in range(0, 360, 45):
            radians = math.radians(angle)
            rays.append((burst_x + math.cos(radians) * 19, burst_y + math.sin(radians) * 19))
        for point in rays:
            _line(draw, [(burst_x, burst_y), point], "#f0a126", 3)
    elif scene.action == "pulling":
        hx, hy = agent["hand_forward"]
        px, py = patient["waist"]
        draw.line([(hx, hy), ((hx + px) / 2, hy - 20), (px, py)], fill="#8b5a2b", width=7)
        draw.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], outline=ink, width=4)
        _motion_lines(draw, patient_x, patient_y - 5, -direction)

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=95, subsampling=0)


def build_scenes(scenes_per_action: int, seed: int = 20270821) -> list[ControlledScene]:
    scenes = []
    for action_index, action in enumerate(ACTIONS):
        for index in range(scenes_per_action):
            scene_seed = seed + action_index * 10_000 + index
            red_side = "left" if index % 2 == 0 else "right"
            background = BACKGROUNDS[(action_index + index) % len(BACKGROUNDS)]
            base_id = f"ctrl_{action}_{index:03d}"
            for agent_color in ("red", "blue"):
                scenes.append(ControlledScene(base_id, action, scene_seed, red_side, agent_color, background))
    return scenes


def scene_record(scene: ControlledScene, image_path: Path) -> dict:
    record = asdict(scene)
    record["patient_color"] = scene.patient_color
    record["image_path"] = image_path.as_posix()
    return record
