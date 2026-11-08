# Source inventory

Live inventory taken on 2026-10-23 with plain HTTP requests (no browser). "Live" means the
adapter was verified end to end against the real endpoint; the posting count is what the
endpoint reported that day.

## Live sources (55)

| Company | ATS | Config | Postings | Notes |
|---|---|---|---|---|
| Bank of America | workday | `ghr` / wd1 / `Lateral-EMEA` | 74 | US lateral site is `Lateral-US` (~2000). Campus roles are on campus.bankofamerica.com, not Workday. |
| Barclays | workday | `barclays` / wd3 / `External_Career_Site_Barclays` | 717 | |
| BP Trading | workday | `bpinternational` / wd3 / `bpCareers` | 292 | Whole-of-BP board. |
| Citi | workday | `citi` / wd5 / `2` | 2000 (capped) | Workday stops counting at 2000; add `applied_facets` by country if this becomes a problem. |
| Deutsche Bank | workday | `db` / wd3 / `DBWebsite` | 1145 | |
| Euronext | workday | `hrhub` / wd3 / `Euronext_Career_Page` | 150 | Shared tenant. |
| Flow Traders | greenhouse | board `flowtraders` | 47 | Fixture source for the tests. |
| Gunvor | workday | `gunvor` / wd3 / `Gunvor_Careers` | 35 | Rebranding to Centalion. Fixture source for the tests. |
| IMC | greenhouse | board `imc` | 168 | |
| Jane Street | greenhouse | board `janestreet` | 220 | |
| Julius Baer | workday | `juliusbaer` / wd3 / `External` | 179 | |
| Lombard Odier | workday | `lombardodier` / wd3 / `Lombard_Odier_Careers` | 65 | |
| LSEG | workday | `lseg` / wd3 / `Careers` | 670 | |
| Man Group | greenhouse | board `mangroup` | 61 | |
| Moelis | workday | `moelis` / wd1 / `Experienced-Hires` | 36 | Campus hiring is on moelis-careers.tal.net. |
| Optiver | greenhouse | board `optiverus` | 169 | The `optiver` board exists but is empty. |
| PJT Partners | workday | `pjtpartners` / wd1 / `Careers` | 55 | |
| Point72 | greenhouse | board `point72` | 212 | |
| Shell Trading | workday | `shell` / wd3 / `ShellCareers` | 139 | |
| TP ICAP | workday | `tp` / wd107 / `TP-ICAP` | 110 | |
| Trafigura | workday | `trafigura` / wd3 / `TrafiguraCareerSite` | 71 | |
| Vitol | smartrecruiters | company `Vitol` | 35 | |
| Mediobanca | custom (`intervieweb`) | feed discovered from mediobanca.com/it/lavora-con-noi/posizioni-aperte.html | 23 | In-recruiting (Intervieweb) JSON feed; Milan, Madrid, Paris, London roles. |
| Intesa Sanpaolo | sitemap (RSS) | jobs.intesasanpaolo.com/sitemap.xml (an RSS feed) | 322 | SuccessFactors; title, link and location straight from the feed, no page fetches. |
| UniCredit | sitemap (paginated index) | careers.unicredit.eu/en_GB/jobsuche/SearchJobs/?jobOffset=N | ~560 | BeeSite portal; 15 per page, JSON-LD on job pages, backfilled 150 per run. |
| Banca Sella | workday | `sellagroup` / wd3 / `ID01` | 38 | Found via join.sellagroup.eu. |
| Macquarie Group | sitemap (listing only) | recruitment.macquarie.com/en_US/careers/SearchJobs | ~580 | Avature; title, office, date, category read from the listing pages (`fetch_pages: false`), job pages never opened. |
| Pemberton Asset Management | ashby | board `pemberton` | 3 | |
| Fasanara Capital | workable | account `fasanara` | 8 | |
| MUFG | workday | `mufgub` / wd3 / `MUFG-Careers` + `Country` facet | 68 | Global board ~680. |
| TD Securities | workday | `td` / wd3 / `TD_Bank_Careers` + `jobFamilyGroup` (TD Securities) + country facet | 10 | Whole-of-TD board ~1800. |
| Standard Chartered | sitemap | jobs.standardchartered.com/sitemap.xml, city-prefixed URLs only | ~40 of 1200 | SuccessFactors; JSON-LD on job pages. |
| Wells Fargo | sitemap (job XML feed) | wellsfargojobs.com/en/jobs/xml/ | ~1600 (11 in scope) | One 15 MB request per run. |
| Onyx Capital Group | workable | account `onyx-capital-group` | 7 | Graduate Trader / Graduate Quant Analyst roles. |
| Trading 212 | ashby | board `trading212` | 53 | Mostly Sofia; London roles classified by rules. |
| Glencore | custom (`glencore`) | JSON API behind glencore.com/en/careers/jobs | 353 | Workday feed re-published by Glencore's own site. |
| Nomura | sitemap | careers.nomura.com/sitemap.xml, 507 job pages | 507 | SuccessFactors; no JSON-LD, title/location from page metadata. Campus on nomuracampus.tal.net stays manual. |
| Société Générale | sitemap | careers.societegenerale.com/sitemap.xml | ~660 | JSON-LD on every job page, includes 2027 programmes. |
| Marex | sitemap (index page) | marex.com/careers/career-opportunities | 85 | Server-rendered listing; title/location from meta description. |
| Cargill | sitemap | careers.cargill.com/sitemap.xml | ~1300 | JSON-LD; worldwide, backfilled 150 pages per run. |
| Eurex / Deutsche Börse | sitemap | careers.deutsche-boerse.com/sitemap.xml | 181 | JSON-LD; covers Clearstream. |
| Jump Trading | greenhouse | board `jumptrading` | 95 | Added 2026-10-23. |
| Qube Research & Technologies | greenhouse | board `quberesearchandtechnologies` | 194 | Added 2026-10-23. London/Paris heavy, 2027 graduate roles. |
| Squarepoint Capital | greenhouse | board `squarepointcapital` | 92 | Added 2026-10-23. |
| DRW | greenhouse | board `drweng` | 163 | Added 2026-10-23. |
| Tower Research Capital | greenhouse | board `towerresearchcapital` | 101 | Added 2026-10-23. |
| Virtu Financial | greenhouse | board `virtu` | 48 | Added 2026-10-23. |
| Akuna Capital | greenhouse | board `akunacapital` | 39 | Added 2026-10-23. |
| Mako | greenhouse | board `mako` | 4 | Added 2026-10-23. |
| GSA Capital | greenhouse | board `gsacapital` | 13 | Added 2026-10-23. |
| Schonfeld | greenhouse | board `schonfeld` | 68 | Added 2026-10-23. |
| AQR | greenhouse | board `aqr` | 57 | Added 2026-10-23. |
| TransMarket Group | greenhouse | board `transmarketgroup` | 18 | Added 2026-10-23. |
| Keyrock | ashby | board `keyrock` | 8 | Added 2026-10-23. |
| Quadrature Capital | greenhouse | board `quadraturecapital` | 3 | Added 2026-10-23. |

## Identified, adapter not built yet (set `active: false`)

| Company | ATS | Plan |
|---|---|---|
| EY | SAP SuccessFactors (careers.ey.com) | 9,000+ job pages worldwide without JSON-LD; needs a title/URL filter before it is worth crawling. |
| Pictet | Old-style SuccessFactors portal (career012.successfactors.eu, company `banquepict`), JavaScript only | Needs browser |
| ExxonMobil | SAP SuccessFactors (jobs.exxonmobil.com) | Sitemap empty. |

## Manual (blocked, bespoke, or portal not identified)

| Company | What was found | Difficulty |
|---|---|---|
| UBS | jobs.ubs.com and ubs.com/careers return 403 to non-browser clients | Needs browser |
| Jefferies | Both experienced and campus hiring run on jefferies.tal.net (the Workday tenant is not used publicly) | Medium: tal.net board scrape |
| HSBC | mycareer.hsbc.com (Avature); per-locale sitemaps exist but list no job pages | Hard |
| Goldman Sachs | higher.gs.com, bespoke JS portal | Hard |
| JPMorgan | Oracle Recruiting Cloud (jpmc.fa.oraclecloud.com) | Medium: Oracle has a JSON API, could be a later adapter |
| Morgan Stanley | Eightfold | Medium: Eightfold has a JSON API |
| Millennium | Eightfold (mlp.eightfold.ai) | Medium |
| BNP Paribas, BGL BNP Paribas | group.bnpparibas returns 403; BGL careers URLs 404 | Needs browser |
| Natixis CIB | recrutement.natixis.com is a JavaScript app with no feed or sitemap | Needs browser |
| Crédit Agricole CIB | Talentsoft/Cegid (jobs.ca-cib.com) | Medium: try sitemap |
| Banca Monte dei Paschi di Siena | Taleo career section (lavoraconnoi.mps.it); the list is loaded by Taleo's internal joblist.ajax POST, ~20 openings | Medium: replicate the AJAX call |
| EIB, EIF | PeopleSoft eRecruitment | Hard |
| Banque de Luxembourg | Portal not identified | Unknown |
| Peel Hunt, Citadel, Citadel Securities, StoneX | 403 to non-browser clients (Citadel's job pages are also blocked; their sitemap only lists articles) | Needs browser |
| Bregal Milestone | No careers page on the site | n/a |
| ADM, Centerview, Rothschild & Co | JS-rendered careers pages, ATS not visible in the source; sitemaps hold no job pages | Unknown |
| Dare, Vela Trading, Mercuria | Connection/TLS errors from this client | Retry from GitHub runner |
| Louis Dreyfus | `ldc.wd3.myworkdayjobs.com` answers 401 on guessed sites | Medium |
| Evercore | `evercore.wd1.myworkdayjobs.com` answers 401; campus on tal.net | Medium |
| Houlihan Lokey | `hl.wd1` / `External` answers but lists one role; main site unknown | Medium |
| Lazard | Oracle Recruiting Cloud (professionals) + lazard-careers.tal.net (campus) | Medium |
| Perella Weinberg | tal.net job board | Medium |
| ICE | iCIMS/Jibe front end (careers.ice.com); sitemap.xml answers AccessDenied | Medium |
| TotalEnergies Trading | Avature | Hard |

## How the inventory was done

1. Guessed Greenhouse boards straight against `boards-api.greenhouse.io`.
2. Fetched each careers page (and one level of job-ish links) and grepped the source for
   `myworkdayjobs.com`, `greenhouse.io`, `lever.co`, `smartrecruiters.com`, `ashbyhq.com`,
   `oraclecloud.com`, `successfactors`, `avature`, `eightfold`, `tal.net`, `taleo`, `workable`.
3. For every Workday hit, called the CXS `jobs` endpoint to confirm it answers 200 with a
   `jobPostings` array. Workday returns 422 for a wrong site name and 406 for the bare tenant
   root, so a site name must come from the employer's own page.

## Added on 2026-10-23 (second phase)

- Adapters: Lever, SmartRecruiters, Ashby, Workable, sitemap + JSON-LD (with HTML index pages
  and a metadata fallback), and a `custom` adapter for Glencore's JSON API.
- Lever: none of the seed or extra finance employers probed use Lever; the test fixture is a
  generic public board (Palantir) so the adapter stays covered.
- The extra employers were found by probing public Greenhouse/Ashby boards for market makers,
  prop shops and quant funds with London or European desks. Remove any you do not want from
  `companies.yaml`.

## Added on 2026-10-23 (Italian banks)

Mediobanca, Intesa Sanpaolo, UniCredit and Banca Sella are live (see table). Monte dei Paschi
stays manual (Taleo). New adapter features for them: RSS feeds (`rss_url`), offset-paginated
listing pages (`index_url_pattern`), and the `intervieweb` custom kind.

## Added on 2026-10-25 (wishlist batch)

Live check with plain HTTP requests; "in scope" = rows kept after the profile scope filter on
the day of adding (GB/IT/LU/CH/FR/IE, no experienced, no summer internships).

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| PIMCO | workday | `pimco` / wd1 / `pimco-careers` | 182 | 7 | |
| Blackstone | workday | `blackstone` / wd1 / `Blackstone_Careers` | 147 | 5 | Experienced hires. |
| Blackstone Campus | workday | `blackstone` / wd1 / `Blackstone_Campus_Careers` | 26 | 2 | Internships / analyst programmes. |
| BlackRock | workday | `blackrock` / wd1 / `BlackRock_Professional` | 291 | 10 | Campus hiring is on careers.blackrock.com (Radancy), not on this board. |
| Apollo | workday | `athene` / wd5 / `apollo_careers` | 54 | 9 | Shared Athene tenant. |
| The Carlyle Group | workday | `carlyle` / wd1 / `Carlyle` | 72 | 5 | |
| Ardian | workday | `ardian` / wd103 / `ardiancareers` | 67 | 5 | Many stages (summer-type internships) dropped by scope. |
| Castleton Commodities International | workday | `osv-cci` / wd1 / `ccicareers`, `cxs_tenant: osv_cci` | 12 | 3 | The API path uses an underscore while the host uses a hyphen. |
| ICE | custom `jibe` | host careers.ice.com | 341 | 9 | iCIMS Jibe: `/api/jobs` only answers after the `/jobs` page set the session cookie. |
| Susquehanna (SIG) | custom `jibe` | host careers.sig.com | 286 | 54 | Dublin office. |
| RBC | custom `phenom` | jobs.rbc.com, en_ca/ca, country filter | 26 | 8 | Phenom `/widgets` refineSearch API, countries filtered server-side. |
| Brevan Howard | custom `phenom` | careers.brevanhoward.com, en_gb/gb | 27 | 1 | |
| Mizuho EMEA | sitemap | careers.mizuhoemea.com/sitemap.xml | 32 | 6 | SuccessFactors. Mizuho Americas is Workday `mizuho` / wd1 / `MizuhoAmericas` (119), out of geography. |
| ExxonMobil | sitemap (rss_url) | jobs.exxonmobil.com/sitemap.xml | 508 | 27 | The file is a Google-Jobs RSS feed (6 MB); priority 2. |
| Capgemini | custom `capgemini` | wp-json/llm/v1/jobs, 8 country codes | ~600 | 0 | Almost everything is IT and dropped by scope; priority 2. |
| Chevron | manual | careers.chevron.com (Eightfold) | | | Eightfold JSON API answers 404 for this tenant. |
| Capula | manual | careers.capula.com (Hireserve) | | | AWS WAF browser challenge. |

## Added on 2026-10-26 (wishlist batch: banks, boutiques, valuation firms, fund administrators)

Inventory with plain HTTP requests (no browser available that day). "Postings" is what the
source returned; "In scope" is what survived the country / function / employment-type filter.
Three new custom kinds were added for this batch: `bamboohr`, `oracle` (Oracle HCM Cloud
recruiting sites) and `wordpress` (jobs published as a WordPress post type over the REST API).

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Lloyds Banking Group | workday | `lbg` / wd3 / `LBG_Careers` | 70 | 18 | Experienced hires only; campus programmes are elsewhere. |
| Santander CIB | workday | `santander` / wd3 / `SantanderCareers` | 1078 | 487 | Group-wide board (retail, all countries); 6 London rows. |
| BBVA | workday | `bbva` / wd3 / `BBVA` | 618 | 396 | Mostly Mexico and Spain; unknown-country rows are kept by the scope rule. |
| ING | sitemap | careers.ing.com/sitemap.xml, target-city `/en/job/<city>/` URLs | ~700 (9 in target cities) | 9 | Radancy; JSON-LD with datePosted. |
| Nordea | sitemap | careers.nordea.com/sitemap.xml, target cities + the four Nordic head offices | 159 (38 opened) | 0 | SuccessFactors; no London role today. The head-office cities keep the pattern matching something, otherwise the adapter reports an error. |
| Koch Minerals & Trading | sitemap (listing only) | koch.avature.net SearchJobs/Minerals, `fetch_pages: false` | 8 | 0 | Wishlist name "Koch Supply & Trading". London roles today are trade support, middle office and IT, all dropped by the function filter. |
| LionTree | greenhouse | board `liontree` | 3 | 0 | US roles only today. |
| Guggenheim Securities | workday | `guggenheim` / wd1 / `Guggenheim_Partners` | 5 | 1 | US board; Guggenheim Investments is `guggenheiminvestment` / wd5 / `External` (24). |
| Panmure Liberum | custom `bamboohr` | subdomain `panmure` | 3 | 2 | Incl. the entry-level expression of interest. No posting date. |
| Kroll | sitemap | careers.kroll.com/en/sitemap.xml, target-city `/en/job/<city>/` URLs | 350 (34 in target cities) | 8 | Valuation / portfolio-valuation analyst roles in London, Milan, Paris, Luxembourg. JSON-LD without datePosted (backfilled over the next runs). |
| BDO | sitemap | careers.bdo.co.uk/sitemap.xml, London URLs only | 199 (91 London) | 4 so far | Radancy; 60 pages per run, the rest follows tomorrow. |
| Forvis Mazars | workday | `forvismazarsuk` / wd107 / `FM_1`, locale en-GB | 188 | 43 | UK board; treasury advisory, valuations, deals. |
| S&P Global | workday | `spgi` / wd5 / `SPGI_Careers` | 321 | 33 | Wishlist name "S&P Global Portfolio Valuations"; whole group. |
| Lincoln International | greenhouse | board `lincolninternational` | 5 | 5 | M&A analyst/associate roles; apply links go to lincolninternational.com/greenhouse/. |
| Aztec Group | workday | `aztecgroup` / wd103 / `External` | 28 | 10 | |
| Langham Hall | sitemap (listing only) | langhamhall.com/apply/current-vacancies, `fetch_pages: false` | 7 | 0 | Hong Kong, Singapore, New York today. No posting date. |
| Alter Domus | sitemap | careers.alterdomus.com/sitemap.xml, target-city URLs | 221 (37 in target cities) | 7 | Radancy; JSON-LD. |
| IQ-EQ | custom `wordpress` | iqeq.com/careers/wp-json/wp/v2, type `vacancy`, taxonomies `vacancy_location` / `department` | 110 | 4 | Location is country-level (United Kingdom, Luxembourg...), so the city stays empty. |
| Apex Group | workday | `theapexgroup` / wd3 / `apexgroupcareers` | 1085 | 11 | |
| Citco | custom `oracle` | host fa-euxc-saasfaprod1.fa.ocs.oraclecloud.com, site `CX_1` | 536 | 20 | Dublin and London fund-services roles; some requisitions have no location. |
| Ocorian | sitemap | ocorian.com/sitemap.xml, `/job/` URLs | 53 | 2 | Drupal; JSON-LD. |
| JTC | custom `wordpress` | jtcgroup.com/wp-json/wp/v2, type `job`, taxonomies `location` / `job_department` | 56 | 9 | Office names like "Jersey - St Helier" are not target cities; applications go to a Cornerstone portal. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| ENEL | Avature portal; the SearchJobs page is an empty client-rendered shell, no sitemap, no feed. | Needs a browser or the Avature XHR endpoint. |
| NatWest Markets | jobs.natwestgroup.com answers 403 to every non-browser request. | Bot protection. |
| Rabobank | rabobank.jobs answered 403 "Tijdelijk niet beschikbaar" all day. | Retry the inventory. |
| Alvarez & Marsal | alvarezandmarsal.com answers 403; no Workday/iCIMS tenant found by guessing. | Needs a browser to see the job-search XHR. |
| Grant Thornton (UK) | Job pages carry JSON-LD but are not in the sitemap; the job search is a JavaScript app with no visible API. | Needs a browser. |
| RSM UK | AEM site, job search rendered client-side. | Needs a browser. |
| Crowe UK | crowe.com answers 403. | Bot protection. |
| Valuation Research Corporation | ADP Workforce Now portal. | JavaScript only; tiny London office. |
| Robey Warshaw, Zaoui & Co, Ondra Partners | No careers page or job feed (Robey Warshaw and Ondra sites did not answer). | Headhunter-driven hiring. |

## Added on 2026-11-03 (evening routine)

First 20 rows of `backlog.md` (tier 1: valuation, transaction services, M&A advisory); the wishlist had no new rows. Plain HTTP only. "Postings" is what the source returned; "In scope" is what survived the country / function / employment-type filter.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Deloitte UK | sitemap (listing only) | apply.deloitte.co.uk/UKCareers/SearchJobs, 20 per page, `fetch_pages: false` | ~594 | 3 | Avature; title, office, service line and date from the listing. Mostly non-finance roles. |
| KPMG UK | sitemap | experienced.kpmgcareers.co.uk/sitemap.xml, London URLs only | 121 London (190 total) | 0 so far | SuccessFactors; 60 pages opened per run, 61 left for tomorrow. Graduate vacancies are on www.kpmgcareers.co.uk (not read). |
| KPMG Italia | sitemap | careers.kpmg.it/sitemap.xml | 222 | 27 so far | SuccessFactors; 140 pages left for the next runs. |
| KPMG Luxembourg | sitemap | careers.kpmg.lu/sitemap.xml | 54 | 18 | SuccessFactors. |
| Deloitte Luxembourg | sitemap | jobs.deloitte.lu/sitemap.xml | 82 | 19 | SuccessFactors; 3 pages left for the next run. |
| Evelyn Partners | smartrecruiters | company `EvelynPartners` | 17 | 9 | |
| Stout | workday | `stout` / wd5 / `Stout-Careers` | 41 | 2 | Mostly US roles. |
| Alantra | workday | `alantra` / wd3 / `Alantra` | 51 | 3 | |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| PwC UK, PwC Italia, PwC Luxembourg | pwc.co.uk, pwc.com and pwc.lu answer 403 to plain clients. | Bot protection. |
| Teneo, Clearwater International | teneo.com and clearwatercf.com answer 403. | Bot protection. |
| Deloitte Italia | Avature portal deloittecm.avature.net shared with Greece and others; 418 roles, 6 per page, no location in the listing. | Could be done with ~70 requests per run plus job pages; not worth it blind. |
| FTI Consulting | Coveo JavaScript search; jobs.fticonsulting.com not reachable. | Needs a browser. |
| AlixPartners | Client-rendered job search; no ATS link in page source, no job URLs in sitemaps. | Needs a browser. |
| Accuracy | Openings embedded from app-accuracy.bc.direct (JavaScript app). | Needs a browser or the app's XHR. |
| Eight Advisory | eight-advisory.com fails the TLS handshake (unrecognized name). | Retry later. |
| Interpath Advisory | Workable account `interpath-advisory` exists, but Workable answered 429 (Retry-After ~24h) to this egress IP. | Retry tomorrow and switch to `workable`. |
| Oaklins | Network of independent firms; no central vacancy list. | Per-member-firm sites. |

## Added on 2026-11-04 (evening routine)

First 20 processable rows of `backlog.md` (tier 1 rows 1-18 and Berenberg, plus KKR from tier 2); the wishlist had no new rows. Deutsche Numis, Greenhill (Mizuho) and Natixis Partners are already covered by the Deutsche Bank, Mizuho EMEA and Natixis entries and did not use a slot. Plain HTTP only. "Postings" is what the source returned; "In scope" is what survived the country / function / employment-type filter.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| William Blair | greenhouse | board `williamblair` | 48 | 3 | Mostly Chicago and New York; 6 London roles, 3 in scope. |
| Piper Sandler | workday | `pipersandler` / wd501 / `Piper_Sandler_Careers` | 51 | 9 | Mostly US; data centre wd501 is on the company page. |
| Harris Williams | workday | `pnc` / wd5 / `HarrisWilliams` | 13 | 7 | PNC's tenant; 2027 M&A associate hiring. |
| Stifel | sitemap | careers-stifel.icims.com/sitemap.xml | ~143 | 0 so far | iCIMS; 60 pages opened per run, 83 left, mostly US. SmartRecruiters company `stifel` is a stale 2016 posting. |
| Berenberg | sitemap (listing) | careers.berenberg.com/search-our-jobs | 48 | 10 | Concrete CMS; the sitemap is stale (404s), so the listing page is harvested; JSON-LD on job pages. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| DC Advisory, Baird, Raymond James | dcadvisory.com, bairdcareers.com and raymondjames.com answer 403 to plain clients. | Bot protection. |
| Cavendish | Hand-made WordPress vacancy pages (2 roles), no feed. | Small; re-check by hand. |
| Arma Partners | Vacancies page says none open. | Email applications. |
| Fenchurch Advisory, Equita, Vitale & Co | No vacancy list, applications by email. | No public feed. |
| Fineurop Soditic, Klecha & Co | Sites fail TLS or proxy (502) from this egress. | Retry later. |
| Ethica Group, Intermonte | No careers page found. | Parent / LinkedIn hiring. |
| Banca Akros | Banco BPM Intervieweb spontaneous-application form only; the vacancy feed key is not public. | Needs the feed key or a browser. |
| Banca Profilo | One teaser card (Junior Private Banker) and a form. | Small. |
| KKR | Greenhouse embed on kkr.com/careers/career-opportunities, board token not in the page source (`for=stage`). | Needs a browser. |

## Added on 2026-11-05 (evening routine)

First 20 rows of `backlog.md` (tier 2, TPG to Triton Partners); tier 1 was empty and the wishlist had no new rows. Plain HTTP only. "Postings" is what the source returned; "In scope" is what survived the country / function / employment-type filter (the run log figure).

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| TPG | greenhouse | board `tpgcareers` | 19 | 0 | Fort Worth, New York, remote. |
| Bain Capital | workday | `baincapital` / wd1 / `External_Public` | 31 | 1 | |
| EQT | greenhouse | board `eqtpartners` | 13 | 2 | Mostly Stockholm; 3 London roles. |
| Permira | greenhouse | board `permiraexternalprivate` | 7 | 1 | EU-hosted job pages. |
| PAI Partners | sitemap | careers.paipartners.com/sitemap.xml | 42 open | 5 | Recruitee; `closed-` slugs excluded; Paris internships. |
| Partners Group | sitemap | jobs.partnersgroup.com/sitemap.xml | 79 | 11 | SuccessFactors; target-city slugs only (Zug, Zurich, London, Luxembourg, Milan, Paris, Dublin, Geneva). |
| Intermediate Capital Group (ICG) | workday | `icg` / wd3 / `external_careers` | 15 | 2 | |
| Triton Partners | workday | `tritonpartners` / wd3 / `External` | 5 | 0 | |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| CVC Capital Partners | No careers page on cvc.com; CVC Credit Partners Workable account answers 429 and shows no openings. | Retry Workable later. |
| Cinven, Hg, Investindustrial, Charterhouse, Alpha Private Equity | No vacancy list, feed or ATS link on their sites (careers pages 404 or editorial only). | No public feed. |
| Advent International | Site answers 403 to plain clients. | Bot protection. |
| Warburg Pincus | ClearCompany portal is JavaScript only; main site 403. | Needs a browser. |
| Bridgepoint | SmartRecruiters company `Bridgepoint` has 0 postings; site behind a bot challenge. | Switch to `smartrecruiters` when it fills. |
| Eurazeo | JobTeaser / Cornerstone flow. | Needs a browser. |
| Clessidra, Ambienta | /lavora and /careers pages have no job list (form only). | No public feed. |

## Added on 2026-11-06 (evening routine)

First 20 rows of `backlog.md` (tier 2, Nordic Capital to HPS Investment Partners); tier 1 was empty and the wishlist had no new rows. Plain HTTP only. "Postings" is what the source returned; "In scope" is what survived the country / function / employment-type filter (the run log figure).

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Nordic Capital | sitemap (RSS) | career.nordiccapital.com/jobs.rss | 4 | 0 | Teamtailor; feed read directly. Frankfurt / Stockholm internships. |
| General Atlantic | greenhouse | board `generalatlantic` | 14 | 0 | |
| Brookfield | workday | `brookfield` / wd5 / `brookfield` | 142 | 7 | Whole-of-Brookfield board. |
| Antin Infrastructure Partners | sitemap (RSS) | antininfrastructurepartners-1655458195.teamtailor.com/jobs.rss | 1 | 0 | Teamtailor; feed read directly. |
| Tikehau Capital | smartrecruiters | company `tikehaucapital` | 1 | 1 | |
| HPS Investment Partners | greenhouse | board `hpsinvestmentpartners` | 1 | 0 | |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Oaktree Capital Management | Workday `oaktree` / wd1 / `Oaktree`, 52 roles. The workday adapter takes the first bullet field as the job id, which is the country here, so every posting collapses to 2. | Adapter fix: derive id from the path when bullet fields repeat; then switch to `workday`. |
| Hayfin Capital Management | Workable account `hayfin-capital-management` (~5 London roles); Workable answered 429 to every request tonight. | Retry the `workable` adapter later. |
| Silver Lake | silverlake.com 403; Greenhouse page `silverlakecareerpage` is a talent-database form, boards API 404. | Bot protection / no list. |
| Ares Management, 3i Group, Blue Owl | Sites answer 403 to plain clients; no ATS link visible. | Bot protection. |
| Thoma Bravo | Careers page has no ATS link or job list. | No public feed. |
| Inflexion, Livingbridge, ECI Partners, Montagu, Astorg | Careers URLs 404; no ATS link on the sites. | No public feed. |
| LDC | Editorial careers page, applications by email. | No public feed. |
| Arcmont Asset Management | arcmontam.com fails through the proxy. | Retry later. |

## Added on 2026-11-07 (evening routine)

First 20 rows of `backlog.md` (tier 2, Sixth Street to StepStone Group); tier 1 was empty and the wishlist had no new rows. Plain HTTP only. "Postings" is what the source returned; "In scope" is what survived the country / function / employment-type filter (the run log figure).

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Sixth Street | workday | `sixthstreet` / wd1 / `sixthstreetcareers` | 18 | 0 | Mostly Dallas / US. |
| Apax Partners | lever | company `apax` | 0 | 0 | Board exists, empty tonight. |
| Pantheon | greenhouse | board `pantheonpublic` | 7 | 1 | The `pantheon` slug is an unrelated company. |
| HarbourVest | workday | `harbourvest` / wd5 / `HVP` | 77 | 6 | |
| LGT Capital Partners | workday | `lgtcp` / wd502 / `lgtcpcurrentvacancies` | ~20 | 8 | Pfäffikon, Dublin, London. |
| Capital Dynamics | greenhouse | board `capitaldynamicsag` | 10 | 1 | |
| Hamilton Lane | workday | `hamiltonlane` / wd108 / `search` | 50 | 5 | |
| StepStone Group | greenhouse | board `stepstone` | 62 | 1 | Board embedded on the careers page; London, Zurich, Dublin programmes. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Golub Capital | Site 403; Workday tenant `golub` (wd1) exists but the site name is unknown (422 on guesses). | Bot protection / site name. |
| Coller Capital | Teamtailor `jobs.rss` answers 200 but is empty, so the sitemap adapter errors. | Switch to `sitemap` with `rss_url` when roles appear. |
| Unigestion | Join page has an application form only. | No public feed. |
| NB Renaissance | No vacancy list; only a Neuberger Berman Workday tenant link (`nb`, wd1, site unknown). | No public feed. |
| Fondo Italiano d'Investimento, Quadrivio Group, Wise Equity, Xenon Private Equity, Tamburi Investment Partners | No careers page or job list (404, editorial or spontaneous-application page only). | No public feed. |
| F2i, Mandarin Capital Partners, Green Arrow Capital | Sites unreachable through the proxy (F2i only via f2isgr.it, no careers page). | Retry later. |

## Added on 2026-11-08 (evening routine)

Rest of tier 2 (Vista Equity Partners to CDP Equity) and the first eleven rows of tier 3 (Eni to Terna); tier 1 was empty and the wishlist had no new rows. Plain HTTP only. "Postings" is what the source returned; "In scope" is what survived the country / function / employment-type filter (the run log figure).

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Leonardo | workday | `leonardocompany` / wd3 / `LeonardoCareerSite` | 849 | 253 | Found on leonardo.com/en/careers/work-with-us. |
| Ferrari | sitemap | jobs.ferrari.com/sitemap.xml, city-prefixed slugs | 1 | 1 | SuccessFactors; only Italian and target-city pages opened (~25 jobs, mostly US). |
| Prada Group | sitemap | jobs.pradagroup.com/sitemap.xml, city-prefixed slugs | 26 | 26 | SuccessFactors; ~240 jobs worldwide, target-city pages only (a few more backfill next run). |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Vista Equity Partners, Searchlight Capital, Epiris | Sites answer 403 to plain clients. | Bot protection. |
| Francisco Partners | Careers link is a Getro job board covering portfolio companies, JavaScript app. | No public feed. |
| Stirling Square, Exponent Private Equity, AnaCap, Pollen Street | No careers page or job list (404). | No public feed. |
| CDP Equity | cdp.it behind a Radware bot challenge. | Bot protection. |
| Eni | Oracle HCM on jobs.eni.com (site CX_1004); TLS chain fails verification through the proxy. | Retry later, then `custom`/`oracle`. |
| A2A | Oracle HCM (hdeh.fa.em3.oraclecloud.com, CX_1); REST API blocked by WAF (403). | Bot protection. |
| Stellantis | Site 403; WordPress careers site with JavaScript search and no job post type. | No public feed. |
| EssilorLuxottica, Pirelli, TIM, Terna | Careers pages have no ATS link or feed in the source. | JavaScript search. |
| Snam | No careers page reachable (404). | No public feed. |
