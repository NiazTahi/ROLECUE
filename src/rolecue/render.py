from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


RED = "#e31a1c"
BLUE = "#1f78b4"


def _scale_box(box: list[int], source_size: tuple[int, int], target_size: tuple[int, int]):
    sx = target_size[0] / source_size[0]
    sy = target_size[1] / source_size[1]
    return tuple(round(value * (sx if index % 2 == 0 else sy)) for index, value in enumerate(box))


def render_role_boxes(
    source: Path,
    output: Path,
    agent_box: list[int],
    patient_box: list[int],
    annotation_size: tuple[int, int],
    visual_agent_color: str = "red",
) -> None:
    with Image.open(source) as loaded:
        image = loaded.convert("RGB")
    colors = {
        "agent": RED if visual_agent_color == "red" else BLUE,
        "patient": BLUE if visual_agent_color == "red" else RED,
    }
    width = max(4, round(min(image.size) / 100))
    draw = ImageDraw.Draw(image)
    for role, box in (("agent", agent_box), ("patient", patient_box)):
        scaled = _scale_box(box, annotation_size, image.size)
        draw.rectangle(scaled, outline=colors[role], width=width)
        inset = max(1, width // 2)
        inner = (scaled[0] + inset, scaled[1] + inset, scaled[2] - inset, scaled[3] - inset)
        if inner[2] > inner[0] and inner[3] > inner[1]:
            draw.rectangle(inner, outline="#ffffff", width=max(1, width // 3))
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=94, subsampling=0)


def build_contact_sheet(
    entries: Iterable[tuple[Path, str]], output: Path, columns: int = 4, tile_size: int = 260
) -> None:
    rows = list(entries)
    if not rows:
        return
    label_height = 34
    row_count = (len(rows) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_size, row_count * (tile_size + label_height)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=14)
    for index, (path, label) in enumerate(rows):
        with Image.open(path) as loaded:
            thumb = loaded.convert("RGB")
        thumb.thumbnail((tile_size - 8, tile_size - 8))
        x = (index % columns) * tile_size + (tile_size - thumb.width) // 2
        y0 = (index // columns) * (tile_size + label_height)
        y = y0 + (tile_size - thumb.height) // 2
        sheet.paste(thumb, (x, y))
        draw.text(
            (index % columns * tile_size + 6, y0 + tile_size + 7), label, fill="black", font=font
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92, subsampling=0)
