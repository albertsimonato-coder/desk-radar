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
| Bregal Milestone |  |  |  |  |
| MUFG |  |  |  |  |
| Natixis Corporate and Investment Banking |  |  |  |  |
| Pictet |  |  |  |  |
| Wells Fargo |  |  |  |  |
| Td Securities |  |  |  |  |
| Standard Chartered |
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
