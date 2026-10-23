"""Fit score 0-100 from profile.yaml weights, with a stored breakdown."""

from __future__ import annotations

import math
import re
from datetime import UTC, datetime

from radar.models import Opening, ScoreBreakdown


def _kw_patterns(words: list[str]) -> list[tuple[str, re.Pattern]]:
    out = []
    for w in words:
        w = str(w).strip().lower()
        if not w:
            continue
        left = r"(?<![a-z0-9])" if w[0].isalnum() else ""
        right = r"(?![a-z0-9])" if w[-1].isalnum() else ""
        out.append((w, re.compile(left + re.escape(w) + right)))
    return out


class Scorer:
    def __init__(self, profile: dict):
        self.p = profile
        self.w = profile["weights"]
        self.boost = _kw_patterns(profile.get("keywords_boost", []))
        self.penalty = _kw_patterns(profile.get("keywords_penalty", []))

    def city_weight(self, o: Opening) -> float:
        cities = self.p["cities"]
        if o.city and o.city in cities:
            return float(cities[o.city])
        if o.city == "Remote":
            return float(self.p["remote_weight"])
        if not o.city:
            if o.country and o.country in self.p["countries_bonus"]:
                return float(self.p["countries_bonus"][o.country])
            return float(self.p["unknown_city_weight"])
        return float(self.p["other_city_weight"])

    def score(self, o: Opening, now: datetime | None = None) -> ScoreBreakdown:
        now = now or datetime.now(UTC)
        bd = ScoreBreakdown()
        bd.city = round(self.w["city"] * self.city_weight(o), 2)
        bd.employment_type = round(
            self.w["employment_type"]
            * float(self.p["employment_types"].get(o.employment_type, 0.5)),
            2,
        )
        bd.function = round(
            self.w["function"] * float(self.p["functions"].get(o.function, 0.35)), 2
        )

        text = " ".join([o.title, o.department, o.description_snippet]).lower()
        hits = [w for w, p in self.boost if p.search(text)]
        pens = [w for w, p in self.penalty if p.search(o.title.lower())]
        kw = min(1.0, 0.34 * len(hits)) - min(1.0, 0.5 * len(pens))
        bd.keyword_hits = hits + [f"-{w}" for w in pens]
        bd.keywords = round(self.w["keywords"] * max(-1.0, kw), 2)

        ref = o.posted_at or o.first_seen
        if ref.tzinfo is None:
            ref = ref.replace(tzinfo=UTC)
        age_days = max(0.0, (now - ref).total_seconds() / 86400)
        hl = float(self.p["recency_half_life_days"])
        bd.recency = round(self.w["recency"] * math.pow(0.5, age_days / hl), 2)

        total = bd.city + bd.employment_type + bd.function + bd.keywords + bd.recency
        bd.total = round(max(0.0, min(100.0, total)), 1)
        return bd
