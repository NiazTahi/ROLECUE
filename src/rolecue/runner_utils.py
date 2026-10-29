from __future__ import annotations

import re


def parse_option(text: str) -> str | None:
    match = re.search(r"(?<![A-Za-z])([AB])(?![A-Za-z])", text.upper())
    return match.group(1) if match else None


def parse_color(text: str) -> str | None:
    normalized = text.strip().lower().strip(".!,;: ")
    if normalized.startswith("red"):
        return "red"
    if normalized.startswith("blue"):
        return "blue"
    return None
