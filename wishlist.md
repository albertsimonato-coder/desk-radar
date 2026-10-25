# Desk Radar wishlist

Companies to add to the tracker. Fill one table row per company; only the name is required.
When a batch is ready, tell Claude "add the companies in wishlist.md" and it will find each
careers portal, add the entry to `companies.yaml`, test it live, and push.

How to fill the columns:

- **Company**: the name as you would say it (e.g. "Banca Generali").
- **Careers URL**: the page where their jobs are listed, if you have it. Optional; a blank
  cell means "find it for me".
- **Priority**: `1` = scanned every day, `2` = scanned on Mondays. Default `1`.
- **Group**: one of `bank`, `boutique`, `asset_manager`, `commodities`, `exchange`,
  `prop_trading`, `advisory`, `corporate`. Optional; it only drives the Group filter on the page.
- **Notes**: anything useful ("only the London office", "their graduate programme opens in
  September", "same portal as X"). Optional.

Rows under "Done" have already been added; move or leave them, they are ignored on the next run.

## To add

| Company | Careers URL | Priority | Group | Notes |
|---|---|---|---|---|
| Example Bank | https://careers.example.com/ | 1 | bank | delete this example row |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## Remove or pause

| Company | Action (`remove` or `pause`) | Why |
|---|---|---|
|  |  |  |

## Done

| Company | Added on | Result |
|---|---|---|
| Mediobanca, Intesa Sanpaolo, UniCredit, Banca Sella | 2026-10-23 | live |
| Banca Monte dei Paschi di Siena | 2026-10-23 | manual (Taleo portal, no public feed) |
| Macquarie Group | 2026-10-24 | live (Avature listing, ~580 roles worldwide, 28 in scope) |
| Pemberton Asset Management | 2026-10-24 | live (Ashby) |
| Fasanara Capital ("Fusanara") | 2026-10-24 | live (Workable) |
| MUFG | 2026-10-24 | live (Workday, UK/EU facet; 2027 UK Summer Analyst programmes) |
| TD Securities | 2026-10-24 | live (Workday, TD Securities family + country facet) |
| Standard Chartered | 2026-10-24 | live (SuccessFactors sitemap, target-city pages only) |
| Wells Fargo | 2026-10-24 | live (job XML feed; EMEA summer analyst programmes) |
| Natixis Corporate and Investment Banking | 2026-10-24 | manual (JavaScript portal, no feed) |
| Pictet | 2026-10-24 | manual (old SuccessFactors portal, no feed) |
| Bregal Milestone | 2026-10-24 | manual (no careers page) |
| TP ICAP, Jefferies, Goldman Sachs, JPMorgan, Houlihan Lokey | 2026-10-25 | already in the registry (TP ICAP live on Workday; the other four manual: bespoke or Oracle portals, Workday site names not public) |
| ICE | 2026-10-25 | live (iCIMS/Jibe JSON API, new `jibe` adapter kind; was manual) |
| Susquehanna (SIG) | 2026-10-25 | live (same Jibe API; ~290 roles, Dublin hub) |
| PIMCO, Blackstone (+ Campus site), BlackRock, Apollo, The Carlyle Group, Ardian | 2026-10-25 | live (Workday) |
| Castleton Commodities International | 2026-10-25 | live (Workday, tenant spelled osv_cci in the API) |
| RBC, Brevan Howard | 2026-10-25 | live (Phenom People search API, new `phenom` adapter kind; RBC filtered to the six countries) |
| Mizuho EMEA | 2026-10-25 | live (SuccessFactors sitemap; Americas board is out of geography) |
| ExxonMobil | 2026-10-25 | live (SuccessFactors RSS feed, was inactive; ~30 UK roles) |
| Capgemini | 2026-10-25 | live (public JSON API by country code; priority 2, nearly all roles are IT and dropped by scope) |
| Chevron | 2026-10-25 | manual (Eightfold portal, JSON API answers 404) |
| Capula | 2026-10-25 | manual (Hireserve portal behind an AWS WAF browser challenge) |
