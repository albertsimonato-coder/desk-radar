"""Load profile.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_profile(path: str | Path = "profile.yaml") -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    data.setdefault("new_window_days", 7)
    data.setdefault("cities", {})
    data.setdefault("other_city_weight", 0.15)
    data.setdefault("unknown_city_weight", 0.4)
    data.setdefault("remote_weight", 0.5)
    data.setdefault("countries_bonus", {})
    data.setdefault("employment_types", {})
    data.setdefault("functions", {})
    data.setdefault(
        "weights", {"city": 30, "employment_type": 30, "function": 25, "keywords": 10, "recency": 5}
    )
    data.setdefault("recency_half_life_days", 21)
    data.setdefault("keywords_boost", [])
    data.setdefault("keywords_penalty", [])
    data.setdefault("employment_type_rules", {})
    data.setdefault("function_rules", {})
    data.setdefault("scope", {"enabled": False})
    data.setdefault("digest", {"max_items": 25, "min_fit": 40})
    return data
