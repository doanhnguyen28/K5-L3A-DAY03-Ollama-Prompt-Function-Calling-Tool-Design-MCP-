"""Offline live demo for the four new Role C research tools.

Run from starter_v0: python scripts/demo_role_c.py
No API keys or HTTP requests required.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import TOOL_FUNCTIONS


EXAMPLES = [
    ("dedupe_sources", {"items": [
        {"title": "News A", "url": "https://www.example.org/news?utm_source=demo"},
        {"title": "News A copy", "url": "http://example.org/news#article"},
        {"title": "News B", "url": "https://example.org/other"},
    ]}),
    ("date_filter", {"items": [
        {"title": "Inside", "published": "2026-11-05T14:30:00Z"},
        {"title": "Outside", "date": "2026-10-01"},
        {"title": "Undated"},
    ], "start_date": "2026-11-01", "end_date": "2026-11-10"}),
    ("source_audit", {"items": [
        {"title": "Good", "url": "https://example.org/a", "summary": "Summary"},
        {"title": "", "url": "not-a-url", "summary": ""},
    ]}),
    ("keyword_extract", {"text": "Python agent nghiên cứu. Python agent Python.", "max_keywords": 3}),
]


def main() -> None:
    for name, arguments in EXAMPLES:
        print(f"\n=== {name} ===")
        print(json.dumps(TOOL_FUNCTIONS[name](**arguments), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
