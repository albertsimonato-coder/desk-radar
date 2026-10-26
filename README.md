# Desk Radar Scanner

Daily monitor of finance job openings, pulled straight from employers' own career sites
(never from aggregators), normalised, deduplicated, classified, scored against your profile,
stored forever in SQLite and rendered as two static pages:

- `docs/index.html`: every opening ever seen (open and closed).
- `docs/new.html`: only the new ones (new in the last N days, or new since the last run).

It runs for free on GitHub Actions and publishes through GitHub Pages.

## Layout

```
companies.yaml            employer registry (ATS + config per employer)
profile.yaml              your targets, cities, keyword lists, score weights
src/radar/                the package (adapters/, normalize, store, classify, score, render, runner)
tests/                    pytest, fixtures/ holds one recorded real response per adapter
docs/                     generated pages + inventory.md (which ATS each employer uses)
data/radar.sqlite         the database, committed by the Actions run
.github/workflows/scan.yml
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest                                  # offline, fixtures only
python -m radar check                   # validate companies.yaml / profile.yaml
python -m radar run --all               # scan every active source, update DB, render pages
python -m radar run --tier daily        # what the scheduler runs (priority 1; priority 2 on Mondays)
python -m radar run --all --only "Optiver,Gunvor"   # a subset, by name or slug
python -m radar run --all --dry-run     # fixtures instead of live sites
python -m radar render                  # re-render pages from the DB without scanning
open docs/index.html
```

If `python -m radar` says `No module named radar` on macOS with Python 3.13, the editable
install's `.pth` file got the hidden flag and Python skips it; fix with
`chflags nohidden .venv/lib/python3.13/site-packages/__editable__*.pth`.

Flags: `--db`, `--companies`, `--profile`, `--docs` override paths; `--workers N` sets how many
employers are fetched at the same time (default 8, `1` = one after another); `--no-llm` skips
the Claude pass; `--no-render` skips the pages; `-v` for debug logging.

Set `ANTHROPIC_API_KEY` to enable the optional Claude pass. It only runs on rows the keyword
rules left as `other`, uses the cheapest current model, asks for strict JSON, and caches the
answer by dedup key in the database so each opening is classified once. Without the key the
pass is skipped silently.

## Add a company

1. Open the employer's careers page and find the ATS. Hints: `myworkdayjobs.com` means
   Workday; `boards.greenhouse.io` / `job-boards.greenhouse.io` means Greenhouse;
   `jobs.lever.co` Lever; `smartrecruiters.com` SmartRecruiters; `jobs.ashbyhq.com` Ashby.
   Bespoke portals: try `sitemap`, otherwise `manual`.
2. Add an entry to `companies.yaml`:

   ```yaml
   - name: Example Bank
     priority: 1            # 1 = daily, 2 = Mondays
     group: bank            # bank | boutique | asset_manager | commodities | exchange | prop_trading | advisory | corporate
     ats: workday
     config:                # adapter-specific, see below
       tenant: example
       wd: wd3
       site: External
     careers_url: https://careers.example.com/   # human page, used as fallback link
     active: true
   ```

   Adapter config keys:

   | ats | keys |
   |---|---|
   | greenhouse | `board` (the slug in `boards.greenhouse.io/<board>`) |
   | workday | `tenant`, `wd` (wd1..wd5, wd107, ...), `site`, optional `locale` (default `en-US`), optional `applied_facets`, `search_text` |
   | lever | `company` |
   | smartrecruiters | `company` |
   | ashby | `board` |
   | workable | `account` (the slug in `apply.workable.com/<account>/`) |
   | sitemap | `job_url_pattern` (regex); optional `sitemap_url` (or `none`), `rss_url` (a job RSS feed, read directly), `index_urls` (HTML listing pages to harvest links from), `index_url_pattern` + `index_step` (offset-paginated listing), `max_new_pages` (default 50), `title_strip`, `location_regex` |
   | custom | `kind` (bespoke JSON APIs kept in `adapters/custom.py`: `glencore`, `intervieweb`, `jibe` (iCIMS Jibe sites), `phenom` (Phenom People sites), `capgemini`, `bamboohr` (`subdomain`), `oracle` (Oracle HCM sites: `host`, `site`), `wordpress` (REST API: `base`, `type`, optional `location_taxonomy`, `department_taxonomy`)) |
   | manual | none; the entry is kept for the record and skipped |

   The sitemap adapter reads each job page once: it diffs the URLs it finds against the ones
   already stored, fetches only the new ones (up to `max_new_pages` per run) and parses the
   schema.org `JobPosting` JSON-LD. Pages without JSON-LD fall back to the page title and
   meta description (good enough for SuccessFactors sites such as Nomura).

   For Workday the site name is in the URL after the locale:
   `https://<tenant>.<wd>.myworkdayjobs.com/en-US/<site>/job/...`. A wrong site answers 422.
3. `python -m radar check`, then `python -m radar run --all --only "Example Bank"`.
4. Note what you found in `docs/inventory.md`.

## How open / closed / new works

Every posting is reduced to a `dedup_key = sha1(company_slug | normalised_title | city)`.
The normalised title is lowercased with requisition ids, years, `(m/f/d)` and bracketed junk
removed; the city comes from an alias map (`London, GB`, `United Kingdom - London`, `Londra`
all become `London`, country `GB`). Two requisitions with the same title in the same city
collapse into one row.

Each row keeps `first_seen`, `last_seen`, `first_run_id`, `status`, `missing_runs` and `reopened`:

- **Seen again**: `last_seen` is refreshed, `missing_runs` reset to 0.
- **Absent** from a *successful* scan of its source: `missing_runs` += 1. A failed source
  (HTTP error, parse error) never counts as a miss, so an outage cannot close anything.
- **Closed**: after two consecutive misses `status` becomes `closed`. The row stays in the
  database and on the "all" page, greyed out. Nothing is ever deleted.
- **Reappeared**: a closed row seen again goes back to `open`, `reopened` += 1, and keeps its
  original `first_seen`. It is never counted as new again.
- **New** = `status = open`, `reopened = 0`, and `first_seen` within `new_window_days`
  (profile.yaml, default 7). "New since last run" = first seen by the latest completed run.

Classification is rule-based (keyword lists in `profile.yaml`, matched on title first, then
department, then the description snippet), with the optional Claude pass for leftovers.
Rule order is priority, so `offcycle` is listed before `internship`; an internship whose title
states a duration of four months or more is off-cycle too, whatever the wording. Summer, spring
and placement internships are out of scope (bachelor-level), only off-cycle ones are kept.
The fit score (0-100) is a weighted sum of city, employment type, function, keyword hits and
recency (25/25/25/10/15 by default, recency halving every 14 days so fresh postings rank
first); the breakdown is stored and shown on hover over the score.

## Saved applications checklist

Every row on both pages has a **Save** button (on a phone, swipe the row to the right). Saved
openings appear under the **Saved** tab as a checklist with a status (to apply, applied,
interview, offer, rejected, dropped), a deadline and free-text notes. The list lives in the
browser's localStorage, so it survives every re-render and keeps a snapshot of openings that are
later closed. It is per device: **Copy sync link** produces a URL that imports the list when
opened on another device (computer to phone and back); **Copy as Markdown** covers notes apps, **Export to Excel** writes a
real `.xlsx` workbook (no library, built in the page) to the browser's download folder, and
**Export JSON / Import** are for backups.

The openings tables have their own **Export to Excel** button: it writes the rows currently
shown (search, filters and sort applied), optionally only the first N, to a workbook in the
browser's download folder.

## Posting dates

`posted_at` is the employer's own date and comes from the source whenever it exists (API
fields, JSON-LD, SuccessFactors' `datePosted` meta, a `posted_regex` over the page text, the
Workday job-detail endpoint when the list hides it). Where a source has none at all, the row
keeps `first_seen`, the moment the scanner first saw it; that is also the rule for what counts
as **new**, so a posting that appears today is new today whatever its stated date. Undated rows
are re-checked a few per run, so a newly added employer fills in over the following days.

## Scope and the morning digest

`profile.yaml` has a `scope` block: postings outside the listed countries (unknown locations
are kept), or classified as an excluded function or employment type, are not stored at all.
Turn it off with `enabled: false`. Rows stored before a scope change are not deleted; the
scanner simply stops seeing them, so they close after two runs. The large Workday boards also
carry a country facet in `companies.yaml` (`applied_facets`) so the request itself is smaller.

`python -m radar digest --html d.html --text d.txt --subject d.subject` writes an email body
with the best openings new since the last run (`digest.max_items` / `digest.min_fit` in the
profile). The workflow sends it after each run through Gmail when two repository secrets exist:
`MAIL_USERNAME` (the Gmail address that sends) and `MAIL_PASSWORD` (a Google "app password"
for that account, not the normal password). Without the secrets the step is skipped. The
digest is also posted as a GitHub issue labelled `digest` on every run that has news, so
email is optional: a wrong Gmail secret (`535 Username and Password not accepted`) is logged
but no longer fails the run. To fix it, turn on 2-Step Verification on the sending Google
account, create an app password at myaccount.google.com/apppasswords and paste the 16-character
value (spaces removed) into the `MAIL_PASSWORD` secret.

## Scheduler

`.github/workflows/scan.yml` runs at 06:17 UTC daily and on demand (`workflow_dispatch`, with
a `tier` input). It installs, runs the offline tests, runs `python -m radar run --tier daily`,
and commits `data/radar.sqlite`, `docs/index.html` and `docs/new.html` if they changed.

Setup once: push the repo, enable GitHub Pages from the `docs/` folder on the default branch,
and (optionally) add `ANTHROPIC_API_KEY` as a repository secret.

## Etiquette

Employers are fetched in parallel (8 at a time), but never more than one request per second
to the same host; the database is written from one thread only. Realistic User-Agent, 20 s
timeout, three retries with backoff on 429/5xx. A source that fails is logged in the `source_health` table and shown on
the page; the run continues. LinkedIn, Indeed and eFinancialCareers are never scraped.
