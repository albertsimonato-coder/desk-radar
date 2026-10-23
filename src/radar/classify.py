"""Rule-based classification of employment_type and function, with an optional Claude pass."""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

from radar.models import EmploymentType, Function, Opening

log = logging.getLogger(__name__)

EMPLOYMENT_TYPES = ("graduate", "internship", "offcycle", "analyst_junior", "experienced", "other")
FUNCTIONS = (
    "sales_trading",
    "commodities",
    "market_making",
    "quant",
    "market_risk",
    "treasury",
    "ibd",
    "advisory_valuation",
    "asset_management",
    "operations",
    "technology",
    "other",
)


def _compile(rules: dict[str, list[str]]) -> dict[str, list[re.Pattern]]:
    """Keywords match as whole words. A trailing '*' makes it a prefix match
    (e.g. 'commodit*' matches commodity / commodities)."""
    out: dict[str, list[re.Pattern]] = {}
    for label, words in rules.items():
        pats = []
        for w in words:
            w = str(w).strip().lower()
            if not w:
                continue
            prefix = w.endswith("*")
            w = w.rstrip("*")
            left = r"(?<![a-z0-9])" if w[0].isalnum() else ""
            right = "" if prefix or not w[-1].isalnum() else r"(?![a-z0-9])"
            pats.append(re.compile(left + re.escape(w) + right))
        out[label] = pats
    return out


# Words that are reliable in a job title but noisy in free text ("early stage", "take the lead").
TITLE_ONLY = {
    "stage",
    "stagiaire",
    "vie",
    "v.i.e",
    "analyst",
    "assistant",
    "lead",
    "partner",
    "chief",
    "principal",
    "manager",
    "executive",
    "apprentice",
    "trainee",
    "junior",
}


class RuleClassifier:
    def __init__(self, profile: dict):
        emp = profile.get("employment_type_rules", {})
        self.emp_rules = _compile(emp)
        self.emp_rules_text = _compile(
            {
                k: [w for w in v if str(w).lower().rstrip("*") not in TITLE_ONLY]
                for k, v in emp.items()
            }
        )
        fn = profile.get("function_rules", {})
        self.fn_rules = _compile(fn)
        # In titles, an explicit engineering role wins over the division it sits in
        # ("Software Engineer - Global Markets" is technology, not sales & trading).
        self.fn_rules_title = _compile(
            {"technology": fn.get("technology", [])}
            | {k: v for k, v in fn.items() if k != "technology"}
        )

    @staticmethod
    def _first_match(rules: dict[str, list[re.Pattern]], text: str) -> str | None:
        for label, pats in rules.items():
            for p in pats:
                if p.search(text):
                    return label
        return None

    def employment_type(self, title: str, department: str, snippet: str, emp_raw: str) -> str:
        t = title.lower()
        # Title has priority; within the title, rule order wins (internship before graduate ...)
        m = self._first_match(self.emp_rules, t)
        if m:
            # "senior analyst" -> experienced, even though "analyst" matched analyst_junior first
            if m in ("analyst_junior",) and self._first_match(
                {"experienced": self.emp_rules.get("experienced", [])}, t
            ):
                return "experienced"
            return m
        raw = (emp_raw or "").lower()
        if raw:
            if "intern" in raw:
                return "internship"
            if "graduate" in raw or "early career" in raw:
                return "graduate"
        for text in (department.lower(), snippet.lower()):
            m = self._first_match(self.emp_rules_text, text)
            if m and m != "experienced":
                return m
        return "other"

    def function(self, title: str, department: str, snippet: str) -> str:
        m = self._first_match(self.fn_rules_title, title.lower())
        if m:
            return m
        for text in (department.lower(), snippet.lower()):
            m = self._first_match(self.fn_rules, text)
            if m:
                return m
        return "other"

    def classify(
        self, title: str, department: str, snippet: str, emp_raw: str = ""
    ) -> tuple[str, str]:
        return (
            self.employment_type(title, department, snippet, emp_raw),
            self.function(title, department, snippet),
        )


# ---------------------------------------------------------------------------
# Optional Claude pass for rows left as other/other.
# ---------------------------------------------------------------------------
LLM_MODEL = os.environ.get("RADAR_LLM_MODEL", "claude-haiku-5-5")

_SYSTEM = (
    "You classify finance job postings. Reply with a single JSON object and nothing else, "
    "with exactly two keys: employment_type (one of {}) and function (one of {}). "
    "graduate = structured graduate/analyst programme for recent graduates; internship = summer/"
    "spring/placement; offcycle = off-cycle or long-term internship / VIE; analyst_junior = "
    "entry-level permanent role without a programme; experienced = 3+ years or VP and above."
).format(", ".join(EMPLOYMENT_TYPES), ", ".join(FUNCTIONS))


def llm_available() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def llm_classify(openings: list[Opening], store: Any, max_calls: int = 200) -> int:
    """Classify `other` rows with Claude, cached by dedup_key in the store. Returns #updated."""
    if not llm_available():
        return 0
    try:
        import anthropic  # type: ignore
    except ImportError:
        log.warning(
            "ANTHROPIC_API_KEY set but `anthropic` package not installed; skipping LLM pass"
        )
        return 0
    client = anthropic.Anthropic()
    updated = 0
    calls = 0
    for o in openings:
        if o.employment_type != "other" and o.function != "other":
            continue
        cached = store.llm_cache_get(o.dedup_key)
        if cached is None:
            if calls >= max_calls:
                continue
            calls += 1
            prompt = (
                f"Company: {o.company_name}\nTitle: {o.title}\nDepartment: {o.department}\n"
                f"Location: {o.location_raw}\nEmployment type (raw): {o.employment_type_raw}\n"
                f"Description: {o.description_snippet[:600]}"
            )
            try:
                msg = client.messages.create(
                    model=LLM_MODEL,
                    max_tokens=100,
                    system=_SYSTEM,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = "".join(getattr(b, "text", "") for b in msg.content)
                m = re.search(r"\{.*\}", text, re.S)
                cached = json.loads(m.group(0)) if m else {}
            except Exception as e:  # noqa: BLE001
                log.warning("LLM classify failed for %s: %s", o.title, e)
                continue
            store.llm_cache_put(o.dedup_key, LLM_MODEL, cached)
        et = cached.get("employment_type")
        fn = cached.get("function")
        changed = False
        if o.employment_type == "other" and et in EMPLOYMENT_TYPES and et != "other":
            o.employment_type = et  # type: ignore[assignment]
            changed = True
        if o.function == "other" and fn in FUNCTIONS and fn != "other":
            o.function = fn  # type: ignore[assignment]
            changed = True
        if changed:
            o.classified_by = "llm"
            updated += 1
    return updated


__all__ = ["RuleClassifier", "llm_classify", "llm_available", "EmploymentType", "Function"]
