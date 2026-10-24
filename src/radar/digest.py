"""Morning digest: the openings that are new since the last run, ranked by fit score.

`python -m radar digest --html out.html --text out.txt` writes the email body (both formats)
and prints the subject line; exit code 3 means "nothing new, do not send".
"""

from __future__ import annotations

import html
from datetime import UTC, datetime

from radar.render import build_payload
from radar.store import Store

LABEL_TYPE = {
    "graduate": "Graduate",
    "internship": "Internship",
    "offcycle": "Off-cycle",
    "analyst_junior": "Analyst / Junior",
    "experienced": "Experienced",
    "other": "Other",
}
LABEL_FN = {
    "sales_trading": "Sales & Trading",
    "commodities": "Commodities",
    "market_making": "Market making",
    "quant": "Quant",
    "market_risk": "Market risk",
    "treasury": "Treasury",
    "ibd": "IBD",
    "advisory_valuation": "Advisory / Valuation",
    "asset_management": "Asset mgmt",
    "operations": "Operations",
    "technology": "Technology",
    "other": "Other",
}


def select_rows(payload: dict, profile: dict, window: bool = False) -> list[dict]:
    """New since the last run by default; `window` widens it to new in the last N days."""
    cfg = profile.get("digest", {})
    min_fit = float(cfg.get("min_fit", 40))
    key = "new" if window else "new_run"
    rows = [r for r in payload["rows"] if r[key] and r["fit"] >= min_fit]
    rows.sort(key=lambda r: (-r["fit"], r["company"], r["title"]))
    return rows[: int(cfg.get("max_items", 25))]


def build_digest(
    store: Store, profile: dict, site_url: str, now: datetime | None = None, always: bool = False
) -> tuple[str, str, str, int]:
    """Returns (subject, html_body, text_body, count).

    `always` is for manual test runs: if nothing is new since the last run, fall back to what
    is new in the last N days, and never report zero rows as "do not send"."""
    now = now or datetime.now(UTC)
    payload = build_payload(store, profile, now=now)
    rows = select_rows(payload, profile)
    scope = "since the last run"
    if not rows and always:
        rows = select_rows(payload, profile, window=True)
        scope = f"in the last {payload['window_days']} days"
    counts = payload["counts"]
    date = now.strftime("%a %d %b")
    subject = f"Desk Radar {date}: {len(rows)} new openings worth a look ({counts['new_run']} new since the last run)"

    def row_html(r: dict) -> str:
        loc = html.escape(r["city"] or r["loc"] or "")
        return (
            f'<tr><td style="padding:6px 8px;font-weight:600;color:{"#1a7f37" if r["fit"] >= 70 else "#b35c00"}">{round(r["fit"])}</td>'
            f'<td style="padding:6px 8px">{html.escape(r["company"])}</td>'
            f'<td style="padding:6px 8px"><a href="{html.escape(r["url"])}">{html.escape(r["title"])}</a></td>'
            f'<td style="padding:6px 8px">{loc}</td>'
            f'<td style="padding:6px 8px">{LABEL_TYPE.get(r["type"], r["type"])}</td>'
            f'<td style="padding:6px 8px">{LABEL_FN.get(r["fn"], r["fn"])}</td></tr>'
        )

    table = (
        '<table style="border-collapse:collapse;font:14px -apple-system,Segoe UI,Roboto,sans-serif">'
        '<thead><tr style="text-align:left;color:#666"><th style="padding:6px 8px">Fit</th><th style="padding:6px 8px">Company</th>'
        '<th style="padding:6px 8px">Title</th><th style="padding:6px 8px">City</th><th style="padding:6px 8px">Type</th>'
        '<th style="padding:6px 8px">Function</th></tr></thead><tbody>'
        + "".join(row_html(r) for r in rows)
        + "</tbody></table>"
    )
    html_body = (
        '<div style="font:14px -apple-system,Segoe UI,Roboto,sans-serif;color:#1b1b1f">'
        f"<p>Good morning. Here are the best <b>{len(rows)}</b> openings new {scope}, by fit score. "
        f"New since the last run: {counts['new_run']}. Open: {counts['open']}, total tracked: {counts['total']}.</p>"
        + table
        + f'<p><a href="{html.escape(site_url)}new.html">All new openings</a> · <a href="{html.escape(site_url)}">Everything</a></p></div>'
    )
    text_lines = [f"Desk Radar {date}: top {len(rows)} openings new {scope}, by fit:", ""]
    for r in rows:
        text_lines.append(
            f"{round(r['fit']):>3}  {r['company']} - {r['title']} ({r['city'] or r['loc']}, {LABEL_TYPE.get(r['type'], r['type'])}, {LABEL_FN.get(r['fn'], r['fn'])})"
        )
        text_lines.append(f"     {r['url']}")
    text_lines += ["", f"All new: {site_url}new.html", f"Everything: {site_url}"]
    return (
        subject,
        html_body,
        "\n".join(text_lines),
        (len(rows) if not always else max(len(rows), 1)),
    )
