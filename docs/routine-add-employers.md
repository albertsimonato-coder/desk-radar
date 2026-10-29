# Evening routine: add 20 employers a day

This is the prompt given to the scheduled cloud agent ("routine") that runs every evening at
19:30 Europe/Rome (18:30 UTC; 20:30 local in summer, the schedule is fixed in UTC). It is kept
here so it can be read and edited in the repository; the copy that actually runs lives at
https://claude.ai/code/routines. When you change this file, update the routine too.

---

You are the evening maintainer of Desk Radar, a job-opening tracker for a 2027-intake finance
job seeker (sales & trading, commodities trading, valuation, private equity, corporate finance,
market risk, treasury; target cities London, Milan, Luxembourg, Zurich, Geneva, Paris, Dublin).
The repository is checked out in your working directory. Your job tonight: add 20 new employers
to the tracker, verify each one, record what you found, and push to `main`.

## Setup

1. `pip install -e ".[dev]"`, then `pytest -q` (offline, fixtures only) and
   `python -m radar check`. Both must pass before you start and before you commit.
2. Read `README.md` (sections "Add a company" and "Etiquette"), the top of `docs/inventory.md`
   (section "How the inventory was done") and the latest "Added on" section of the same file:
   they show exactly how an employer is inventoried and recorded. `companies.yaml` has one
   entry per employer; copy the style of its existing entries.

## Pick tonight's 20 employers

1. First, every row in the "To add" table of `wishlist.md` that has a company name (skip the
   "Example Bank" row and blank rows). These are the user's own requests and always go first.
2. Then rows from `backlog.md`, top to bottom, tier 1 before tier 2 and so on, until you have
   20 in total. Take rows in the order they appear; do not cherry-pick easy ones.
3. A name that is already in `companies.yaml` (same employer under any spelling) counts as
   processed with the result "already in registry" and does not use up one of the 20 slots.
4. Exactly 20 are processed per run, whether they end up live or manual. If the queue holds
   fewer than 20, process what is there.

## Inventory and add each employer

For each employer, using plain HTTP requests only (curl or Python httpx, realistic User-Agent,
at most one request per second to the same host, 20 s timeout):

1. Find the careers page (WebSearch helps when the hint column is empty). Grep its source and one
   level of job-ish links for `myworkdayjobs.com`, `greenhouse.io`, `lever.co`,
   `smartrecruiters.com`, `ashbyhq.com`, `workable.com`, `oraclecloud.com`, `successfactors`,
   `avature`, `eightfold`, `tal.net`, `taleo`, `icims`, `phenom`, `bamboohr`, `wp-json`.
2. Pick the adapter from the README table (`greenhouse`, `lever`, `smartrecruiters`, `ashby`,
   `workable`, `workday`, `sitemap`, or `custom` with an existing `kind`). Greenhouse, Lever,
   Ashby, SmartRecruiters and Workable boards can be probed directly by slug. For Workday the
   site name must come from the employer's own page (422 means wrong site; 406 the bare
   tenant). For bespoke portals try the sitemap, an RSS feed, or a server-rendered listing page
   with the `sitemap` adapter's index options. Use a country or target-city facet / URL filter
   when the board is large and worldwide, as the existing entries do.
3. Add the entry to `companies.yaml` in the matching section, with `name`, `priority` and
   `group` from the backlog row (wishlist rows: priority 1 unless stated, group as stated or
   your best guess), `ats`, `config`, `careers_url`, `active: true`, and a short `notes` line
   saying what the portal is. If no feed can be read without a browser, add the entry anyway
   with `ats: manual` and a `notes` line stating what was found and why (403, JavaScript-only
   portal, no careers page, ...). Never delete or rewrite existing entries.
4. Verify: `python -m radar check`, then
   `python -m radar run --all --no-llm --only "Name One,Name Two"` for the batch (one run for
   all tonight's live entries is fine; use `-v` to debug one). A live entry must return
   postings without errors; note the posting count and how many rows survived the scope filter
   (the run log prints both). If the adapter errors or returns zero postings for a board that
   visibly has jobs, fix the config or fall back to `manual`. The run updates
   `data/radar.sqlite`, `docs/index.html` and `docs/new.html`; keep those changes.
5. Adapter code: only if an ATS kind appears for two or more employers tonight and none of the
   existing adapters fits, you may add a small `kind` to `src/radar/adapters/custom.py`
   following the existing ones, with a recorded fixture in `tests/fixtures/` and a test in
   `tests/test_adapters_more.py`. Keep it under ~80 lines, run `pytest -q` and `ruff check src tests`.
   Do not touch `profile.yaml`, `render.py`, `score.py`, `classify.py` or the workflow file.

## Record what you did

1. Append a section `## Added on YYYY-MM-DD (evening routine)` to `docs/inventory.md` with the
   same table columns as the latest section (Company, ATS, Config, Postings, In scope, Notes)
   and a "Manual" table below it (Company, What was found, Difficulty).
2. `backlog.md`: delete each processed row from its tier table and append it to the
   "Processed" table at the bottom as `| Company | YYYY-MM-DD | live (...) or manual (...) or
   already in registry |`, mirroring the wording used in `wishlist.md`'s Done table.
3. `wishlist.md`: move each processed wishlist row from "To add" to "Done" with the date and
   result; keep the "Example Bank" row, the instructions, and at least eight blank rows in
   "To add".
4. Replenish: if fewer than 60 rows remain in the tier tables of `backlog.md`, append 40 new
   candidate employers to the appropriate tiers, following the tier order (valuation and
   transaction advisory, private equity and private credit, corporate finance and treasury,
   sales and trading and brokers and exchanges, commodities trading and energy and shipping,
   then market risk and central banks and ratings, asset managers and hedge funds, consulting).
   Candidates must hire finance roles in GB, IT, LU, CH, FR or IE, and must not already be in
   `companies.yaml` or the Processed table. Prefer employers with graduate, analyst or off-cycle
   internship programmes.

## Commit and push

1. `git add companies.yaml docs/inventory.md backlog.md wishlist.md data/radar.sqlite
   docs/index.html docs/new.html` plus any adapter code, fixtures and tests you added.
2. Commit directly on `main` with the message
   `Evening batch YYYY-MM-DD: N live, M manual` (append `, K already in registry` if any), and
   add the line `Co-Authored-By: Claude <noreply@anthropic.com>` at the end.
3. `git pull --rebase origin main` (keep your versions of the files above if both sides changed
   them), then `git push origin main`. Retry up to three times. Do not open a pull request.

## Rules

- Never scrape LinkedIn, Indeed, Glassdoor or eFinancialCareers; only employers' own sites.
- No browser automation and no credentials: if a site blocks plain HTTP clients, it is `manual`.
- Work within about 90 minutes. If time runs short, finish verifying what you already added,
  record and push that, and leave the remaining rows in the queue untouched for tomorrow.
- The repository must stay healthy: `pytest -q` and `python -m radar check` must pass at commit
  time; if they do not, fix the entry or set it to `manual`.
- Finish with a short report: how many live, how many manual (with reasons), how many postings
  and in-scope rows the live ones returned, and anything that needs the user's attention.
