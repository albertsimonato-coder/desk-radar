# Desk Radar employer backlog

The queue the evening routine works through: every evening it takes the first 20 rows that are
still in the tier tables below (after any rows you left in `wishlist.md`), finds each employer's
careers portal, adds it to `companies.yaml`, scans it once, and moves the row to the "Processed"
table at the bottom. Tiers are ordered by closeness to the career path (valuation, private
equity, corporate finance, sales and trading, commodities trading, then the rest), so the queue
is worked top to bottom.

You can edit this file freely: add rows, delete rows you do not want, reorder, or move a row to
the top to get it added tonight. `wishlist.md` still works and is always processed first.

Columns: **Company** as you would say it; **Group** one of `bank`, `boutique`, `asset_manager`,
`commodities`, `exchange`, `prop_trading`, `advisory`, `corporate`; **Priority** `1` = scanned
daily, `2` = Mondays; **Hint** an optional careers URL or note. Leave a row's Hint empty to let
the routine find the portal.

When fewer than 60 rows remain in the tier tables, the routine appends new candidates of its own
(following the same tier order) so the queue never runs dry.

## Tier 1: valuation, transaction services, M&A advisory

| Company | Group | Priority | Hint |
|---|---|---|---|

## Tier 2: private equity, private credit, infrastructure

| Company | Group | Priority | Hint |
|---|---|---|---|

## Tier 3: corporate finance and treasury inside corporates

| Company | Group | Priority | Hint |
|---|---|---|---|

_Dropped on 2026-11-08: the user wants M&A and investment banking, not finance roles inside corporates. Do not refill this tier._

## Tier 4: sales and trading, brokers, exchanges, market infrastructure

| Company | Group | Priority | Hint |
|---|---|---|---|
| Goodbody | bank | 2 | Dublin |
| Sucden Financial | commodities | 1 |  |
| Old Mission Capital | prop_trading | 2 |  |

## Tier 5: commodities trading, energy, metals, agri, shipping

| Company | Group | Priority | Hint |
|---|---|---|---|
| Sucafina | commodities | 1 | Geneva |
| Viterra | commodities | 1 |  |
| Tereos | commodities | 2 |  |
| Argus Media | commodities | 2 |  |
| Kpler | commodities | 2 |  |
| CMA CGM | commodities | 2 |  |
| Hapag-Lloyd | commodities | 2 |  |
| Torm | commodities | 2 |  |

## Tier 6: market risk, treasury, central banks, ratings, insurance markets

| Company | Group | Priority | Hint |
|---|---|---|---|
| Munich Re | corporate | 2 |  |
| Swiss Re | corporate | 2 | Zurich |
| Zurich Insurance Group | corporate | 2 |  |
| Hannover Re | corporate | 2 |  |
| Willis Towers Watson | corporate | 2 |  |
| Lombard International | corporate | 2 | Luxembourg |
| KBRA | corporate | 2 |  |

## Tier 7: asset managers, hedge funds, quant and market makers

| Company | Group | Priority | Hint |
|---|---|---|---|
| Davidson Kempner | asset_manager | 2 | |
| King Street | asset_manager | 2 | |
| Sculptor Capital | asset_manager | 2 | |
| Pharo Management | asset_manager | 2 | |
| Tudor Investment | asset_manager | 2 | |
| Moore Capital | asset_manager | 2 | |
| Graham Capital | asset_manager | 2 | |
| Systematica | asset_manager | 2 | |
| Cheyne Capital | asset_manager | 2 | |
| CQS | asset_manager | 2 | |
| LMR Partners | asset_manager | 2 | |
| Garda Capital | asset_manager | 2 | |
| Symmetry Investments | asset_manager | 2 | |
| Hudson River Trading | prop_trading | 1 | |
| XTX Markets | prop_trading | 1 | |
| Five Rings | prop_trading | 2 | |
| Headlands Technologies | prop_trading | 2 | |
| Da Vinci Derivatives | prop_trading | 2 | Amsterdam |
| Maven Securities | prop_trading | 1 | |
| G-Research | prop_trading | 2 | |
| Two Sigma | prop_trading | 2 | |
| D. E. Shaw | prop_trading | 2 | |
| Arrowstreet Capital | asset_manager | 2 | |
| Ruffer | asset_manager | 2 | |
| Rathbones | asset_manager | 2 | |
| Liontrust | asset_manager | 2 | |
| Polar Capital | asset_manager | 2 | |
| Ninety One | asset_manager | 2 | |
| Federated Hermes | asset_manager | 2 | |
| Columbia Threadneedle | asset_manager | 2 | |
| Candriam | asset_manager | 2 | Luxembourg |
| Swiss Life Asset Managers | asset_manager | 2 | |

## Tier 8: consulting and other finance

| Company | Group | Priority | Hint |
|---|---|---|---|
| McKinsey & Company | advisory | 2 | |
| Boston Consulting Group | advisory | 2 | |
| Bain & Company | advisory | 2 | |
| Oliver Wyman | advisory | 2 | Financial services practice |
| Roland Berger | advisory | 2 | |
| L.E.K. Consulting | advisory | 2 | |
| Kearney | advisory | 2 | |
| Revolut | corporate | 2 | Treasury, trading |
| Wise | corporate | 2 | Treasury |
| Adyen | corporate | 2 | |
| Worldline | corporate | 2 | |
| Hiscox | corporate | 2 | |
| Beazley | corporate | 2 | |

## Processed

Rows the routine has handled. "live" means the source is scanned; "manual" means the entry
exists in `companies.yaml` but no feed could be read (with the reason), and "already in
registry" means it was there before.

| Company | Added on | Result |
|---|---|---|
| Deloitte UK | 2026-11-03 | live (Avature listing, ~594 roles, 3 in scope) |
| PwC UK | 2026-11-03 | manual (403 to non-browser clients) |
| KPMG UK | 2026-11-03 | live (SuccessFactors sitemap, London pages only; 61 pages still to open) |
| Deloitte Italia | 2026-11-03 | manual (Avature portal shared with Greece etc., no location in listing) |
| PwC Italia | 2026-11-03 | manual (403 to non-browser clients) |
| KPMG Italia | 2026-11-03 | live (SuccessFactors sitemap, 27 in scope so far) |
| PwC Luxembourg | 2026-11-03 | manual (403 to non-browser clients) |
| KPMG Luxembourg | 2026-11-03 | live (SuccessFactors sitemap, 18 in scope) |
| Deloitte Luxembourg | 2026-11-03 | live (SuccessFactors sitemap, 19 in scope) |
| FTI Consulting | 2026-11-03 | manual (Coveo JavaScript search, no feed) |
| AlixPartners | 2026-11-03 | manual (client-rendered job search, no feed) |
| Accuracy | 2026-11-03 | manual (JavaScript app on bc.direct, no feed) |
| Eight Advisory | 2026-11-03 | manual (site fails TLS handshake from plain clients) |
| Teneo | 2026-11-03 | manual (403 to non-browser clients) |
| Interpath Advisory | 2026-11-03 | manual (Workable account found but rate-limited with 429; retry later) |
| Evelyn Partners | 2026-11-03 | live (SmartRecruiters, 17 postings, 9 in scope) |
| Stout | 2026-11-03 | live (Workday, 41 postings, 2 in scope) |
| Alantra | 2026-11-03 | live (Workday, 51 postings, 3 in scope) |
| Oaklins | 2026-11-03 | manual (network of local firms, no vacancy list) |
| Clearwater International | 2026-11-03 | manual (403 to non-browser clients) |
| DC Advisory | 2026-11-04 | manual (403 to non-browser clients) |
| Baird | 2026-11-04 | manual (403 to non-browser clients) |
| Stifel | 2026-11-04 | live (iCIMS sitemap, ~143 jobs mostly US, 0 in scope so far; 83 pages still to open) |
| William Blair | 2026-11-04 | live (Greenhouse, 48 postings, 3 in scope) |
| Raymond James | 2026-11-04 | manual (403 to non-browser clients) |
| Piper Sandler | 2026-11-04 | live (Workday wd501, 51 postings, 9 in scope) |
| Harris Williams | 2026-11-04 | live (Workday on PNC's tenant, 13 postings, 7 in scope) |
| Cavendish | 2026-11-04 | manual (static vacancy page, no feed) |
| Arma Partners | 2026-11-04 | manual (no open vacancies, no feed) |
| Fenchurch Advisory | 2026-11-04 | manual (no vacancy list, email applications) |
| Equita | 2026-11-04 | manual (empty open-positions block, email applications) |
| Vitale & Co | 2026-11-04 | manual (no vacancy list, email applications) |
| Fineurop Soditic | 2026-11-04 | manual (site unreachable (TLS error / 502)) |
| Klecha & Co | 2026-11-04 | manual (site unreachable (502)) |
| Ethica Group | 2026-11-04 | manual (no careers page) |
| Intermonte | 2026-11-04 | manual (no careers page) |
| Banca Akros | 2026-11-04 | manual (Banco BPM Intervieweb form only, no feed) |
| Banca Profilo | 2026-11-04 | manual (single teaser card, no feed) |
| Deutsche Numis | 2026-11-04 | already in registry (hires on the Deutsche Bank portal, entry Deutsche Bank) |
| Berenberg | 2026-11-04 | live (search-our-jobs listing, 48 postings, 10 in scope) |
| Greenhill (Mizuho) | 2026-11-04 | already in registry (greenhill.com now redirects to Mizuho; entry Mizuho EMEA) |
| Natixis Partners | 2026-11-04 | already in registry (hires via the Natixis portal, entry Natixis) |
| KKR | 2026-11-04 | manual (Greenhouse embed with hidden board token) |
| TPG | 2026-11-05 | live (Greenhouse, 19 roles, none in scope) |
| Bain Capital | 2026-11-05 | live (Workday, 31 roles) |
| CVC Capital Partners | 2026-11-05 | manual (no careers page or feed; CVC Credit Workable 429) |
| EQT | 2026-11-05 | live (Greenhouse) |
| Permira | 2026-11-05 | live (Greenhouse, slug permiraexternalprivate) |
| Cinven | 2026-11-05 | manual (no vacancy list or feed) |
| Advent International | 2026-11-05 | manual (403 to plain clients) |
| Warburg Pincus | 2026-11-05 | manual (ClearCompany JavaScript portal, 403 on main site) |
| Hg | 2026-11-05 | manual (no vacancy list) |
| Bridgepoint | 2026-11-05 | manual (SmartRecruiters board empty, site behind bot challenge) |
| PAI Partners | 2026-11-05 | live (Recruitee sitemap) |
| Eurazeo | 2026-11-05 | manual (JobTeaser / Cornerstone, no feed) |
| Investindustrial | 2026-11-05 | manual (no careers page) |
| Clessidra | 2026-11-05 | manual (no job list or feed) |
| Ambienta | 2026-11-05 | manual (application form only) |
| Alpha Private Equity | 2026-11-05 | manual (no careers page) |
| Charterhouse Capital Partners | 2026-11-05 | manual (no careers page) |
| Partners Group | 2026-11-05 | live (SuccessFactors sitemap, target-city pages) |
| Intermediate Capital Group (ICG) | 2026-11-05 | live (Workday) |
| Triton Partners | 2026-11-05 | live (Workday, 5 roles, none in scope) |
| Nordic Capital | 2026-11-06 | live (Teamtailor jobs.rss, 4 roles, 0 in scope) |
| General Atlantic | 2026-11-06 | live (Greenhouse, 14 roles, 0 in scope) |
| Silver Lake | 2026-11-06 | manual (site 403; Greenhouse page is a talent-database form) |
| Thoma Bravo | 2026-11-06 | manual (no ATS or job list on careers page) |
| Oaktree Capital Management | 2026-11-06 | manual (Workday, 52 roles, but adapter collapses ids: country is first bullet field) |
| Ares Management | 2026-11-06 | manual (site 403, Workday site not public) |
| Brookfield | 2026-11-06 | live (Workday, 142 roles, 7 in scope) |
| Antin Infrastructure Partners | 2026-11-06 | live (Teamtailor jobs.rss, 1 role, 0 in scope) |
| 3i Group | 2026-11-06 | manual (site 403) |
| Inflexion | 2026-11-06 | manual (no careers page) |
| Livingbridge | 2026-11-06 | manual (no careers page) |
| LDC | 2026-11-06 | manual (email applications, no job list) |
| ECI Partners | 2026-11-06 | manual (no careers page) |
| Montagu | 2026-11-06 | manual (no careers page) |
| Astorg | 2026-11-06 | manual (no careers page, proxy error on astorg-partners.com) |
| Tikehau Capital | 2026-11-06 | live (SmartRecruiters, 1 role, 1 in scope) |
| Arcmont Asset Management | 2026-11-06 | manual (site unreachable through proxy) |
| Hayfin Capital Management | 2026-11-06 | manual (Workable account exists but answered 429 tonight; retry) |
| Blue Owl | 2026-11-06 | manual (site 403, no public ATS found) |
| HPS Investment Partners | 2026-11-06 | live (Greenhouse, 1 role, 0 in scope) |
| Sixth Street | 2026-11-07 | live (Workday, 18 roles, 0 in scope) |
| Golub Capital | 2026-11-07 | manual (site 403, Workday site name not public) |
| Fondo Italiano d'Investimento | 2026-11-07 | manual (no careers page or job list) |
| Quadrivio Group | 2026-11-07 | manual (no careers page or job list) |
| Wise Equity | 2026-11-07 | manual (no careers page) |
| NB Renaissance | 2026-11-07 | manual (no vacancy list; only Neuberger Berman Workday tenant link) |
| F2i | 2026-11-07 | manual (no careers page found; f2i.it unreachable) |
| Mandarin Capital Partners | 2026-11-07 | manual (site unreachable through proxy) |
| Green Arrow Capital | 2026-11-07 | manual (site unreachable through proxy) |
| Xenon Private Equity | 2026-11-07 | manual (no careers page) |
| Tamburi Investment Partners | 2026-11-07 | manual (editorial work-with-us page, no job list) |
| Apax Partners | 2026-11-07 | live (Lever board exists, 0 roles today) |
| Coller Capital | 2026-11-07 | manual (Teamtailor RSS answers but is empty today; switch to sitemap when roles appear) |
| Pantheon | 2026-11-07 | live (Greenhouse `pantheonpublic`, 7 roles, 1 in scope) |
| HarbourVest | 2026-11-07 | live (Workday, 77 roles, 6 in scope) |
| LGT Capital Partners | 2026-11-07 | live (Workday, 8 in scope) |
| Capital Dynamics | 2026-11-07 | live (Greenhouse, 10 roles, 1 in scope) |
| Unigestion | 2026-11-07 | manual (application form only, no job list) |
| Hamilton Lane | 2026-11-07 | live (Workday, 50 roles, 5 in scope) |
| StepStone Group | 2026-11-07 | live (Greenhouse, 62 roles, 1 in scope) |
| Vista Equity Partners | 2026-11-08 | manual (site 403, bot protection) |
| Francisco Partners | 2026-11-08 | manual (careers link is a Getro portfolio job board, JavaScript, no feed) |
| Searchlight Capital | 2026-11-08 | manual (site 403, bot protection) |
| Stirling Square | 2026-11-08 | manual (no careers page or job list) |
| Exponent Private Equity | 2026-11-08 | manual (no careers page or job list) |
| Epiris | 2026-11-08 | manual (site 403, bot protection) |
| Pollen Street | 2026-11-08 | manual (no careers page found) |
| AnaCap | 2026-11-08 | manual (no careers page or job list) |
| CDP Equity | 2026-11-08 | manual (Radware bot challenge on cdp.it) |
| Eni | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: manual (Oracle HCM on jobs.eni.com, TLS chain fails verification through the proxy; retry later)) |
| Leonardo | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: live (Workday, 849 roles, 253 in scope)) |
| Stellantis | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: manual (site 403; WordPress careers site with JavaScript search, no job feed)) |
| Ferrari | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: live (SuccessFactors sitemap, Italian and target-city pages only, 1 role, 1 in scope)) |
| Prada Group | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: live (SuccessFactors sitemap, target-city pages only, 26 roles, 26 in scope)) |
| EssilorLuxottica | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: manual (JavaScript job search, no feed found)) |
| Pirelli | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: manual (JavaScript job search, no feed found)) |
| TIM (Telecom Italia) | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: manual (JavaScript job search, no feed found)) |
| A2A | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: manual (Oracle HCM API blocked by WAF, 403)) |
| Snam | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: manual (no careers page reachable)) |
| Terna | 2026-11-08 | removed 2026-11-08 (corporate finance out of scope; was: manual (no ATS link or feed found)) |
| BNY | 2026-11-09 | live (21 in scope) |
| State Street | 2026-11-09 | live (14 in scope) |
| Northern Trust | 2026-11-09 | live (34 in scope) |
| Scotiabank | 2026-11-09 | live (13 in scope) |
| CIBC | 2026-11-09 | live (0 in scope) |
| BMO Capital Markets | 2026-11-09 | live (0 in scope) |
| ANZ | 2026-11-09 | live (1 in scope) |
| Commerzbank | 2026-11-09 | live (5 in scope) |
| Danske Bank | 2026-11-09 | live (0 in scope) |
| SEB | 2026-11-09 | manual (careers page only) |
| DNB | 2026-11-09 | live (0 in scope) |
| KBC | 2026-11-09 | manual (local per-country portals (kbc.be/jobs, jobs.cbc.be), belgian roles, no feed) |
| ABN AMRO | 2026-11-09 | live (11 in scope) |
| Erste Group | 2026-11-09 | manual (vacancies are a javascript sap job-board app) |
| Raiffeisen Bank International | 2026-11-09 | live (0 in scope) |
| Bank of China (UK) | 2026-11-09 | manual (uk site redirects to boc.cn, bankofchina.co.uk fails tls) |
| ICBC Standard Bank | 2026-11-09 | manual (both domains answer 403 to plain clients) |
| SMBC Group EMEA | 2026-11-09 | live (14 in scope) |
| Daiwa Capital Markets Europe | 2026-11-09 | manual (careers page lists no vacancies and links to no ats) |
| Investec | 2026-11-09 | manual (403 to plain clients) |
| Close Brothers | 2026-11-10 | manual (SuccessFactors portal behind the careers page, no public feed) |
| Cantor Fitzgerald | 2026-11-10 | manual (403 to non-browser clients) |
| BGC Group | 2026-11-10 | manual (403 to non-browser clients) |
| Tradition (Compagnie Financière Tradition) | 2026-11-10 | manual (no vacancy list or ATS link) |
| ODDO BHF | 2026-11-10 | manual (client-rendered job list, no feed) |
| Kepler Cheuvreux | 2026-11-10 | live (Teamtailor RSS feed, 4 roles, 2 in scope) |
| Banco BPM | 2026-11-10 | manual (careers section without reachable ATS or feed) |
| BPER Banca | 2026-11-10 | manual (no careers page reachable) |
| Credem | 2026-11-10 | live (Oracle HCM REST API) |
| Banca Mediolanum | 2026-11-10 | manual (403 to non-browser clients) |
| FinecoBank | 2026-11-10 | manual (careers URL moved, no vacancy portal found) |
| Banca Generali | 2026-11-10 | manual (careers section not reachable, no ATS found) |
| Banca Ifis | 2026-11-10 | live (own job board, 3 listing pages, title from job page) |
| illimity | 2026-11-10 | live (Workday, 1 posting tonight) |
| Vontobel | 2026-11-10 | live (Workday, 58 roles, 13 in scope) |
| EFG International | 2026-11-10 | manual (403 to non-browser clients) |
| Mirabaud | 2026-11-10 | live (server-rendered listing, 10 roles, 2 in scope) |
| Bank Syz | 2026-11-10 | manual (site unreachable through the proxy, 502) |
| Zürcher Kantonalbank | 2026-11-10 | manual (jobs.zkb.ch unreachable through the proxy, 502) |
| Raiffeisen Switzerland | 2026-11-10 | manual (JavaScript career-center app, no feed) |
| Banque Internationale à Luxembourg | 2026-11-11 | manual (portal not identified, careers URLs 404 / 502) |
| Spuerkeess | 2026-11-11 | manual (Cornerstone JavaScript portal, no feed) |
| Quintet Private Bank | 2026-11-11 | live (server-rendered vacancies listing, 6 roles in scope) |
| CACEIS | 2026-11-11 | manual (412 to plain clients) |
| Bpifrance | 2026-11-11 | manual (no careers page or ATS link found) |
| La Banque Postale | 2026-11-11 | manual (403 to non-browser clients) |
| CIC Market Solutions | 2026-11-11 | manual (static join-us page, no vacancy list) |
| Swissquote | 2026-11-11 | live (SmartRecruiters, 7 roles in scope) |
| IG Group | 2026-11-11 | live (Workday, 6 in scope) |
| CMC Markets | 2026-11-11 | live (Workday, 5 in scope) |
| Saxo Bank | 2026-11-11 | live (Workday, 5 in scope) |
| Interactive Brokers | 2026-11-11 | manual (Dayforce JavaScript portal, no feed) |
| XTB | 2026-11-11 | manual (403 to non-browser clients) |
| eToro | 2026-11-11 | live (server-rendered listing, 17 roles, 0 in scope (Israel/US)) |
| Plus500 | 2026-11-11 | manual (no vacancy list or ATS link found) |
| Tradeweb | 2026-11-11 | manual (403 to non-browser clients) |
| MarketAxess | 2026-11-11 | manual (JavaScript job list, no feed) |
| Bloomberg | 2026-11-11 | manual (403 to non-browser clients) |
| CME Group | 2026-11-11 | live (Workday, 2 in scope) |
| Cboe | 2026-11-11 | live (Phenom People, ~114 roles, 0 in scope (US only today)) |
| Nasdaq | 2026-11-12 | live (Workday, 6 in scope) |
| SIX Group | 2026-11-12 | live (SuccessFactors sitemap, 10 in scope) |
| London Metal Exchange | 2026-11-12 | manual (403 to non-browser clients) |
| EEX (European Energy Exchange) | 2026-11-12 | live (SuccessFactors sitemap on Deutsche Börse site, 9 in scope) |
| Liquidnet | 2026-11-12 | manual (JavaScript job list, Workday report needs credentials) |
| Instinet | 2026-11-12 | manual (403 to non-browser clients) |
| Freepoint Commodities | 2026-11-12 | live (Workday, 1 role, 0 in scope) |
| Hartree Partners | 2026-11-12 | manual (403 to non-browser clients) |
| Mabanaft | 2026-11-12 | manual (no job feed, HubSpot form site) |
| Petroineos | 2026-11-12 | manual (403 to non-browser clients) |
| Equinor | 2026-11-12 | live (Workday, 1 in scope) |
| Eni Trading & Shipping | 2026-11-12 | manual (Taleo JavaScript portal) |
| Uniper | 2026-11-12 | live (SuccessFactors sitemap, 7 in scope) |
| RWE Supply & Trading | 2026-11-12 | live (SuccessFactors sitemap, 26 in scope) |
| EDF Trading | 2026-11-12 | live (Workday, 6 in scope) |
| ENGIE Global Energy Management & Sales | 2026-11-12 | manual (portal not identified, 404/502) |
| Axpo | 2026-11-12 | live (Teamtailor RSS, 29 in scope) |
| Alpiq | 2026-11-12 | live (server-rendered listing, 4 in scope) |
| BKW | 2026-11-12 | manual (JavaScript career centre, no feed) |
| Statkraft | 2026-11-12 | live (SmartRecruiters, 31 in scope) |
| Ørsted | 2026-11-13 | manual (JavaScript vacancy list, no feed) |
| Vattenfall | 2026-11-13 | live (SmartRecruiters, 81 kept; Sweden/Germany/NL/Denmark roles) |
| Centrica | 2026-11-13 | live (Workday, 10 in scope) |
| SEFE | 2026-11-13 | live (SuccessFactors sitemap, 5 in scope) |
| Bunge | 2026-11-13 | manual (SuccessFactors without sitemap or feed; bunge.com 403) |
| COFCO International | 2026-11-13 | live (SuccessFactors sitemap, 21 in scope) |
| Olam Agri | 2026-11-13 | live (SuccessFactors sitemap, 30 in scope) |
| ED&F Man | 2026-11-13 | live (job pages harvested from the opportunities listing, 13 in scope) |
| Sucden | 2026-11-13 | manual (no openings listed, spontaneous application only) |
| Czarnikow | 2026-11-13 | manual (Occupop Next.js app, no feed) |
| Wilmar | 2026-11-13 | manual (regional portals only) |
| Amaggi | 2026-11-13 | manual (no careers page found) |
| Concord Resources | 2026-11-13 | manual (no job listings or ATS link) |
| IXM | 2026-11-13 | manual (site refuses plain HTTP clients) |
| Traxys | 2026-11-13 | manual (static careers page, no listings) |
| Ocean Partners | 2026-11-13 | manual (403 to non-browser clients) |
| Transamine | 2026-11-13 | manual (no careers page) |
| Anglo American | 2026-11-13 | live (SmartRecruiters, 52 in scope) |
| Rio Tinto | 2026-11-13 | live (Workday, 70 in scope) |
| BHP | 2026-11-13 | live (SuccessFactors sitemap, 29 in scope, 59 more pages queued) |
| Vale | 2026-11-14 | manual (Eightfold portal, JSON API answers but no adapter yet) |
| Aurubis | 2026-11-14 | live (job-shop sitemap, 54 roles, 0 in scope) |
| Boliden | 2026-11-14 | live (Workday, 37 in scope) |
| Litasco | 2026-11-14 | manual (no listings or ATS link on careers page) |
| SOCAR Trading | 2026-11-14 | manual (no careers page) |
| Aramco Trading | 2026-11-14 | manual (SuccessFactors search rendered by JavaScript, no feed) |
| ADNOC Global Trading | 2026-11-14 | manual (site resets plain clients) |
| PetroChina International (London) | 2026-11-14 | manual (site resets plain clients) |
| Unipec UK | 2026-11-14 | manual (site unreachable) |
| Alvean | 2026-11-14 | manual (no careers page) |
| Ameropa | 2026-11-14 | manual (careers page only links to LinkedIn) |
| Engelhart Commodities Trading Partners | 2026-11-14 | live (Greenhouse, 3 roles, 0 in scope) |
| BB Energy | 2026-11-14 | live (BambooHR, 8 roles, 0 in scope) |
| Varo Energy | 2026-11-14 | manual (no careers page on varopreem.com) |
| Trailstone | 2026-11-14 | manual (no careers page) |
| Danske Commodities | 2026-11-14 | live (own vacancies page, 5 in scope) |
| InCommodities | 2026-11-14 | live (Hr-On listing page, 6 in scope) |
| MET Group | 2026-11-14 | live (SmartRecruiters, 13 in scope of 64) |
| EnBW | 2026-11-14 | live (Phenom API, 139 roles, 0 in scope) |
| E.ON | 2026-11-14 | live (Oracle HCM REST API, 145 roles, 1 in scope) |
| Iberdrola | 2026-11-15 | manual (iberdrola.com answers 403) |
| Octopus Energy | 2026-11-15 | live (Lever, 156 roles, 30 in scope) |
| Drax | 2026-11-15 | manual (drax.com answers 403) |
| SSE | 2026-11-15 | live (own site sitemap with JSON-LD, 80 roles, 27 in scope) |
| ScottishPower | 2026-11-15 | manual (site answers 403) |
| National Grid | 2026-11-15 | manual (site answers 403) |
| Eni Plenitude | 2026-11-15 | manual (Eni Taleo portal, JavaScript search, no feed) |
| Duferco | 2026-11-15 | manual (no careers page) |
| Gerald Group | 2026-11-15 | manual (empty careers stub, no listings) |
| Puma Energy | 2026-11-15 | live (Workday on Trafigura tenant, 44 roles, 7 in scope) |
| Repsol Trading | 2026-11-15 | live (Workday whole-of-Repsol board, 59 roles, 18 in scope) |
| OMV Trading | 2026-11-15 | live (SuccessFactors sitemap, 8 target-city pages opened, 0 in scope) |
| Galp Trading | 2026-11-15 | live (SuccessFactors sitemap, 20 roles, 20 in scope) |
| Moeve (Cepsa) Trading | 2026-11-15 | live (SuccessFactors sitemap, 38 roles, 31 in scope) |
| Phillips 66 (UK) | 2026-11-15 | live (SuccessFactors sitemap, 37 pages opened, 3 in scope) |
| Clarksons | 2026-11-15 | live (SuccessFactors sitemap, 37 roles, 18 in scope) |
| Braemar | 2026-11-15 | manual (roles page only links to LinkedIn) |
| Simpson Spence Young | 2026-11-15 | manual (ssy.co unreachable, no careers page found) |
| Howe Robinson Partners | 2026-11-15 | live (WordPress directory listing, 3 roles, 2 in scope) |
| Affinity Shipping | 2026-11-15 | manual (careers page states no open positions) |
| CSC Commodities | 2026-11-16 | already in registry (CSC is part of Marex and hires on the Marex portal, entry Marex) |
| Maersk | 2026-11-16 | manual (JavaScript vacancies search, Workday site name not public) |
| MSC | 2026-11-16 | manual (403 to non-browser clients) |
| Oldendorff | 2026-11-16 | manual (static careers page, no feed) |
| Klaveness | 2026-11-16 | manual (Squarespace vacancies page, no feed) |
| Hafnia | 2026-11-16 | manual (recruiterpal.com JavaScript portal, no feed) |
| Frontline | 2026-11-16 | manual (no careers page or vacancy list) |
| Scorpio Tankers | 2026-11-16 | manual (no careers page or vacancy list) |
| d'Amico | 2026-11-16 | manual (join-us.it portal refuses connections through the proxy) |
| Grimaldi | 2026-11-16 | manual (site resets connections from plain clients) |
| Amerex | 2026-11-16 | manual (403 to non-browser clients) |
| Bank of England | 2026-11-16 | live (Oracle HCM REST API, 3 in scope) |
| European Central Bank | 2026-11-16 | live (Avature listing, Frankfurt only, 2 in scope) |
| Banca d'Italia | 2026-11-16 | manual (competitions on a static page, no feed) |
| Swiss National Bank | 2026-11-16 | live (SuccessFactors sitemap, 10 in scope) |
| Banque de France | 2026-11-16 | manual (403 to non-browser clients) |
| Central Bank of Ireland | 2026-11-16 | manual (Candidate Manager list has no location, so scope drops it) |
| Bank for International Settlements | 2026-11-16 | manual (Workday tenant behind a Cloudflare challenge, 429 to the adapter) |
| European Banking Authority | 2026-11-16 | live (own recruitment site, 1 in scope) |
| ESMA | 2026-11-16 | manual (adequasys.com login portal, no feed) |
| EBRD | 2026-11-16 | live (SuccessFactors RSS feed, 6 in scope, London) |
| Fitch Ratings | 2026-11-17 | manual (Fitch Group careers sites unreachable from plain clients) |
| Moody's | 2026-11-17 | live (sitemap, careers.moodys.com JSON-LD pages, ~340 roles worldwide) |
| Morningstar DBRS | 2026-11-17 | live (Workday, 54 roles) |
| Scope Ratings | 2026-11-17 | manual (client-rendered single-page app, no feed) |
| MSCI | 2026-11-17 | live (sitemap, careers.msci.com JSON-LD pages, ~130 roles worldwide) |
| FactSet | 2026-11-17 | manual (client-rendered careers page, no ATS or feed found) |
| Lloyd's of London | 2026-11-17 | live (Workday, 8 roles) |
| Aon | 2026-11-17 | live (iCIMS/Jibe API on jobs.aon.com, ~1000 roles worldwide) |
| Marsh McLennan | 2026-11-17 | live (Phenom People site) |
| WTW | 2026-11-17 | live (sitemap of careers.wtwco.com, ~640 job pages worldwide) |
| Nationwide Building Society | 2026-11-17 | manual (Angular single-page app, no sitemap or feed) |
| Legal & General | 2026-11-17 | live (careers.legalandgeneral.com /jobs listing with sitemap adapter; first page only) |
| Prudential plc | 2026-11-17 | live (Workday, ~470 roles, almost all Asia/Africa) |
| Phoenix Group | 2026-11-17 | live (Oracle HCM REST API) |
| Schroders | 2026-11-17 | live (Oracle HCM REST API) |
| abrdn | 2026-11-17 | live (Workday, 21 roles) |
| Legal & General Investment Management | 2026-11-17 | manual (hires on the Legal & General group site; no separate feed) |
| M&G | 2026-11-17 | live (Workday, ~143 roles) |
| Jupiter Asset Management | 2026-11-17 | manual (no careers page or ATS reachable from plain clients) |
| Fidelity International | 2026-11-17 | live (Workday site 001, ~79 roles) |
| Baillie Gifford | 2026-11-18 | live (Workday, 11 roles by curl; adapter run got 429) |
| Aviva Investors | 2026-11-18 | live (Workday, adapter run got 429) |
| Amundi | 2026-11-18 | live (RSS feed read with the sitemap adapter, 6 postings kept) |
| AXA Investment Managers | 2026-11-18 | already in registry (now BNP Paribas Asset Management, entry BNP Paribas) |
| Natixis Investment Managers | 2026-11-18 | manual (no careers page, JavaScript group portal) |
| Eurizon Capital | 2026-11-18 | already in registry (hires on the Intesa Sanpaolo portal, entry Intesa Sanpaolo) |
| Anima SGR | 2026-11-18 | manual (static page, email applications) |
| Generali Investments | 2026-11-18 | manual (JavaScript group portal) |
| Azimut | 2026-11-18 | manual (no vacancy list) |
| Kairos Partners | 2026-11-18 | manual (no careers page) |
| Algebris Investments | 2026-11-18 | manual (403 to non-browser clients) |
| GAM | 2026-11-18 | live (Workday, adapter run got 429) |
| LGT | 2026-11-18 | live (server-rendered job list, 18 postings) |
| Capital Group | 2026-11-18 | live (Workday, adapter run got 429) |
| Vanguard | 2026-11-18 | manual (JavaScript search, US-only postings) |
| Wellington Management | 2026-11-18 | live (Workday, adapter run got 429) |
| T. Rowe Price | 2026-11-18 | live (Workday international site, adapter run got 429) |
| Franklin Templeton | 2026-11-18 | live (Phenom People, 8 postings) |
| Invesco | 2026-11-18 | live (Workday, adapter run got 429) |
| Janus Henderson | 2026-11-18 | live (SuccessFactors sitemap, 7 postings, 76 pages still to open) |
| Neuberger Berman | 2026-11-18 | manual (429 / unreachable) |
| Nuveen | 2026-11-18 | manual (TIAA Phenom site, widgets API 404) |
| Allianz Global Investors | 2026-11-19 | live (Phenom People on the Allianz group site, six-country filter, 335 postings kept) |
| DWS | 2026-11-19 | live (Workday db/DWSWebsite, 83 roles by curl, adapter run got 429) |
| Robeco | 2026-11-19 | live (Workday, 10 roles, none in scope) |
| Carmignac | 2026-11-19 | manual (JavaScript-only careers page) |
| Comgest | 2026-11-19 | manual (static job-offers page, no feed) |
| Marshall Wace | 2026-11-19 | manual (static join-us pages, no feed) |
| Caxton Associates | 2026-11-19 | live (Workable, 30 roles by curl, adapter run got 429) |
| Rokos Capital Management | 2026-11-19 | manual (static page, email only) |
| BlueCrest Capital | 2026-11-19 | manual (no careers page) |
| Eisler Capital | 2026-11-19 | manual (site unreachable, no feed) |
| ExodusPoint | 2026-11-19 | live (Greenhouse, 2 postings kept) |
| Balyasny Asset Management | 2026-11-19 | manual (Salesforce site needs JavaScript) |
| Verition | 2026-11-19 | live (Greenhouse veritiongroupllc, 1 posting kept) |
| Walleye Capital | 2026-11-19 | live (two Greenhouse boards, full-time and students; US roles only, 0 in scope) |
| Winton | 2026-11-19 | live (Greenhouse, 3 postings kept) |
| Aspect Capital | 2026-11-19 | manual (HiBob widget, JavaScript) |
| Lansdowne Partners | 2026-11-19 | manual (page says no open positions) |
| Egerton Capital | 2026-11-19 | manual (no careers page) |
| TCI Fund Management | 2026-11-19 | manual (no careers page) |
| Elliott Management | 2026-11-19 | manual (no careers page) |
| Raine Group | 2026-11-20 | live (Lever, 1 role, Singapore only, 0 in scope) |
| Qatalyst Partners | 2026-11-20 | manual (mailto addresses only) |
| Livingstone Partners | 2026-11-20 | manual (403 to non-browser clients) |
| GP Bullhound | 2026-11-20 | manual (no vacancy list, Sesame HR / email) |
| Bryan Garnier & Co | 2026-11-20 | manual (site unreachable (502)) |
| Oakley Capital | 2026-11-20 | live (Greenhouse board exists, 0 roles today) |
| IK Partners | 2026-11-20 | manual (403 to non-browser clients) |
| Park Square Capital | 2026-11-20 | manual (403 to non-browser clients) |
| Cerberus Capital Management | 2026-11-20 | manual (403 to non-browser clients) |
| Clayton Dubilier & Rice | 2026-11-20 | manual (no careers page) |
| Eight Roads Ventures | 2026-11-20 | manual (no careers page) |
| Argos Wityu | 2026-11-20 | manual (site unreachable (502)) |
| Vitruvian Partners | 2026-11-20 | manual (no careers page) |
| Cairn Capital | 2026-11-20 | manual (TLS handshake fails) |
| Adams Street Partners | 2026-11-20 | live (Greenhouse, 13 roles, 2 in scope) |
| Investcorp | 2026-11-20 | manual (no vacancy list or ATS link) |
| Cambridge Associates | 2026-11-20 | manual (403 to non-browser clients) |
| Euroclear | 2026-11-20 | manual (403 to non-browser clients, no public ATS) |
| LCH | 2026-11-20 | manual (hires via the LSEG portal, see LSEG entry) |
| Davy | 2026-11-20 | manual (editorial careers pages, no feed) |
| Centerview Partners | 2026-11-20 | already in registry (entry Centerview) |
| BGC Group | 2026-11-20 | already in registry (manual, 403 to non-browser clients) |
