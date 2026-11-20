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

Rest of tier 2 (Vista Equity Partners to CDP Equity) was added; the eleven tier-3 corporate rows (Eni, Leonardo, Stellantis, Ferrari, Prada Group, EssilorLuxottica, Pirelli, TIM, A2A, Snam, Terna) were then removed again at the user's request (finance roles inside corporates are out of scope; only M&A and investment banking wanted). Tier 3 of `backlog.md` is dropped.

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Vista Equity Partners, Searchlight Capital, Epiris | Sites answer 403 to plain clients. | Bot protection. |
| Francisco Partners | Careers link is a Getro job board covering portfolio companies, JavaScript app. | No public feed. |
| Stirling Square, Exponent Private Equity, AnaCap, Pollen Street | No careers page or job list (404). | No public feed. |
| CDP Equity | cdp.it behind a Radware bot challenge. | Bot protection. |

## Added on 2026-11-09 (evening routine)

First 20 rows of `backlog.md` (tier 4, BNY to Investec); tiers 1-3 were empty and the wishlist had no new rows. Plain HTTP only. "Postings" is what the source returned before scope (approximate where noted); "In scope" is the run-log figure.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| BNY | custom (oracle) | `eofe.fa.us2.oraclecloud.com` / `CX_3001` | 21 | 21 | Oracle HCM REST API. |
| State Street | workday | `statestreet` / wd1 / `Global`, Location_Country facet | ~118 | 14 | Of ~1160 worldwide. |
| Northern Trust | workday | `ntrs` / wd1 / `northerntrust`, locationCountry facet | ~107 | 34 | Mostly Limerick. |
| Scotiabank | sitemap (rss_url) | sitemap.xml is an RSS feed; London|Dublin links | 43 | 13 | 1293 items worldwide, mostly Canada. |
| CIBC | workday | `cibc` / wd3 / `search`, Country facet | 2 | 0 | Technology / legal roles dropped by scope. |
| BMO Capital Markets | workday | `bmo` / wd3 / `External`, Country facet | 0 | 0 | No role in the six countries tonight (board is Canada/US only). |
| ANZ | sitemap | `careers.anz.com` sitemap, target-city pages | ~4 | 1 | London pages. |
| Commerzbank | sitemap | `jobs.commerzbank.com` sitemap (jobad) | 60 opened of 472 | 5 | 380 pages left for later runs. |
| Danske Bank | custom (oracle) | `ejqi.fa.ocs.oraclecloud.eu` / `CX_1001` | 120 | 0 | Nordic and India roles, all out of scope tonight. |
| DNB | sitemap | `jobb.dnb.no` sitemap, target cities + Oslo | 2 | 0 | Norwegian roles only. |
| ABN AMRO | sitemap | `werkenbijabnamro.nl/sitemap.vacancy.xml` | 40 opened of ~140 | 11 | 102 pages left; mostly NL. |
| RBI (Raiffeisen Bank International) | sitemap | `jobs.rbinternational.com` sitemap, target cities + Wien | 36 | 0 | Vienna roles only. |
| SMBC Group EMEA | sitemap | `careersemea.smbcgroup.com` sitemap, target cities | 60 opened of ~110 | 14 | 96 pages left; London 96, Dublin 40, Paris 19 in sitemap. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Bank of China (UK) | UK site redirects to boc.cn, bankofchina.co.uk fails TLS. | No careers page. |
| ICBC Standard Bank | Both domains answer 403 to plain clients. | Bot protection. |
| Erste Group | Vacancies are a JavaScript SAP job-board app; jobs.erstegroup.com 502 through the proxy. | No public feed. |
| SEB | Careers page only; vacancy portal unreachable (502). | No public feed. |
| KBC | Local per-country portals (kbc.be/jobs, jobs.cbc.be), Belgian roles, no feed. | No public feed. |
| Daiwa Capital Markets Europe | Careers page lists no vacancies and links to no ATS. | No public feed. |
| Investec | 403 to plain clients; rotational graduate programmes paused. | Bot protection. |

## Added on 2026-11-10 (evening routine)

First 20 rows of `backlog.md` (tier 4, Close Brothers to Raiffeisen Switzerland); tiers 1-3 were empty and the wishlist had no new rows. Plain HTTP only. "Postings" is what the source listed (approximate where noted); "In scope" is the number of rows that survived the scope filter.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Kepler Cheuvreux | sitemap (rss_url) | `keplercheuvreux.teamtailor.com/jobs.rss` | 4 | 2 | Teamtailor RSS. |
| Credem | custom (oracle) | `hczf.fa.em2.oraclecloud.com` / `CX_1` | 5+ | 5 | Oracle HCM REST API. |
| Banca Ifis | sitemap (index_urls) | `posizioniaperte.bancaifis.it`, 3 listing pages | ~30 | 20 | Own job board; title from page title, no JSON-LD. |
| illimity | workday | `illimitybank` / wd3 / `Illimity` | 1 | 1 | Only a spontaneous application tonight. |
| Vontobel | workday | `vontobel` / wd3 / `Vontobel_External_Career` | 58 | 13 | Mostly Zurich. |
| Mirabaud | sitemap (listing only) | `mirabaud.com/en/careers/job-opportunities` | 10 | 2 | Server-rendered listing, `fetch_pages: false`. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Close Brothers | SuccessFactors portal behind the careers page; Workday guess 422. | No public feed. |
| Cantor Fitzgerald, BGC Group, Banca Mediolanum, EFG International | Sites answer 403 to plain clients. | Bot protection. |
| Tradition | Static careers page, no vacancy list or ATS link. | No public feed. |
| ODDO BHF | WordPress site, job list client-rendered; jobs subdomains 502. | No public feed. |
| Banco BPM, Banca Generali, FinecoBank, BPER Banca | Careers sections found but no ATS link, or URLs 404. | No public feed. |
| Bank Syz, Zürcher Kantonalbank | Sites unreachable through the proxy (502); ZKB shows ~60 roles on third-party boards. | Retry later. |
| Raiffeisen Switzerland | jobs.raiffeisen.ch is a JavaScript app with an empty HTML shell. | No public feed. |

## Added on 2026-11-11 (evening routine)

First 20 rows of `backlog.md` (tier 4, Banque Internationale à Luxembourg to Cboe); tiers 1-3 were empty and the wishlist had no new rows. Plain HTTP only. "Postings" is what the source listed (approximate where noted); "In scope" is the number of rows that survived the scope filter.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Quintet Private Bank | sitemap (index_urls) | `quintet.com/en-gb/your-career-at-quintet/vacancies` | 15 | 6 | Server-rendered listing grouped by office; `fetch_pages: false`. |
| Swissquote | smartrecruiters | company `Swissquote` | 35 | 7 | |
| IG Group | workday | `ig` / wd103 / `EXT_IG` | 85 | 6 | |
| CMC Markets | workday | `cmcmarkets` / wd3 / `CMC_Markets_Careers` | 76 | 5 | |
| Saxo Bank | workday | `saxobank` / wd3 / `CareeratSaxoBank` | 62 | 5 | |
| eToro | sitemap (index_urls) | `etoro.com/about/careers/` | 17 | 0 | Listing on the careers page; roles are US/Israel today. |
| CME Group | workday | `cmegroup` / wd1 / `cme_careers` | 71 | 2 | |
| Cboe | custom (phenom) | `careers.cboe.com`, en_us | ~114 | 0 | No server-side country filter added; only US roles today. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Banque Internationale à Luxembourg | bil.com careers URLs 404, careers subdomains 502. | Portal not identified. |
| Spuerkeess | Cornerstone (csod) career site. | JavaScript only. |
| CACEIS | 412 to plain clients; careers subdomain 502. | Bot protection. |
| Bpifrance | No careers page or ATS link found. | No public feed. |
| La Banque Postale, XTB, Tradeweb, Bloomberg | Sites answer 403 to non-browser clients. | Bot protection. |
| CIC Market Solutions | Static join-us page on cic-cib.com. | No public feed. |
| Interactive Brokers | Dayforce candidate portal. | JavaScript only. |
| Plus500 | Careers URL redirects to the US home page; no list. | No public feed. |
| MarketAxess | Open-positions list loaded by JavaScript. | No public feed. |

## Added on 2026-11-12 (evening routine)

First 20 rows of `backlog.md` (tier 4, Nasdaq to Instinet; tier 5, Freepoint Commodities to Statkraft); tiers 1-3 were empty and the wishlist had no new rows. Plain HTTP only. "Postings" is what the source listed (listed in-scope plus dropped); "In scope" is the number of rows that survived the scope filter.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Nasdaq | workday | `nasdaq` / wd1 / `Global_External_Site` + `Location_Country` facet | ~175 worldwide, 10 after facet | 6 | Site name from the public Workday listing; nasdaq.com answers 403. |
| SIX Group | sitemap | `jobs.six-group.com/sitemap.xml`, city-prefixed slugs | 39 | 10 | SuccessFactors; only target-city and Swiss office pages opened. |
| EEX (European Energy Exchange) | sitemap | `career.deutsche-boerse.com/sitemap.xml`, paths `/eex/` and `/ecc/` | 20 | 9 | Same SuccessFactors site as Deutsche Börse; mostly Leipzig. |
| Freepoint Commodities | workday | `freepoint` / wd12 / `Freepoint_Commodities` | 1 | 0 | Single Stamford role today; London roles appear when open. |
| Equinor | workday | `equinor` / wd3 / `EQNR` | 17 | 1 | London Junior Deal Handler; rest Norway/Aberdeen. |
| Uniper | sitemap | `jobs.uniper.energy/sitemap.xml`, target cities + Düsseldorf | 30 | 7 | SuccessFactors, mostly German roles. |
| RWE Supply & Trading | sitemap | `jobs.rwe.com/sitemap.xml`, London, Swindon, Essen and target cities | 59 | 26 | Group-wide SuccessFactors sitemap. |
| EDF Trading | workday | `edftrading` / wd1 / `EDFTrading` | 29 | 6 | Link from the job-opportunities page; London and Paris. |
| Axpo | sitemap (RSS) | `careers.axpo.com/jobs.rss` | 71 | 29 | Teamtailor RSS feed. |
| Alpiq | sitemap (index_urls) | `alpiq.com/career/open-jobs`, 3 listing pages | 12 | 4 | Server-rendered list; `fetch_pages: false`. |
| Statkraft | smartrecruiters | company `Statkraft1` | 71 | 31 | |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| London Metal Exchange | lme.com answers 403 to non-browser clients. | Bot protection. |
| Liquidnet | Job list loaded by JavaScript from a Workday custom report that answers 401. | JavaScript only. |
| Instinet | instinet.com answers 403 to non-browser clients. | Bot protection. |
| Hartree Partners | hartreepartners.com answers 403 to non-browser clients. | Bot protection. |
| Mabanaft | Now MB energy; careers pages point to a German HubSpot form site. | No public feed. |
| Petroineos | petroineos.com answers 403 to non-browser clients. | Bot protection. |
| Eni Trading & Shipping | Eni Taleo portal. | JavaScript only. |
| ENGIE Global Energy Management & Sales | Jobs paths 404, careers.engie.com 502. | Portal not identified. |
| BKW | job.bkw.com SuccessFactors career centre, JavaScript "jobabo", no sitemap. | JavaScript only. |

## Added on 2026-11-13 (evening routine)

First 20 rows of `backlog.md` (tier 5, Ørsted to BHP); tiers 1-4 were empty and the wishlist had no new rows. Plain HTTP only. "Postings" is the count the run log printed for the source; "In scope" is the number of openings stored after the scope filter (the two coincide because the run log counts kept rows; the source totals are in Notes).

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Vattenfall | smartrecruiters | company `Vattenfall` | 81 | 81 | 264 listed at the source; roles in Sweden, Germany, NL, Denmark, none in target cities today. Priority 2. |
| Centrica | workday | `centrica` / wd3 / `Centrica` | 10 | 10 | 59 on the board; centrica.com answers 403, site name found by probing. |
| SEFE | sitemap | `careers.sefe.eu/sitemap.xml` | 5 | 5 | SuccessFactors; 25 jobs listed (London, Manchester, Paris, Germany). |
| COFCO International | sitemap | `careers.cofcointernational.com/sitemap.xml` | 21 | 21 | SuccessFactors, 48 jobs listed worldwide. |
| Olam Agri | sitemap | `careers.olamagri.com/sitemap.xml` | 30 | 30 | SuccessFactors, 46 jobs listed; mostly operations. |
| ED&F Man | sitemap (index_urls) | `edfman.com/careers/our-opportunities/` | 13 | 13 | The WordPress jobs sitemap uses CDATA locs the adapter cannot read, so job links are harvested from the listing page. |
| Anglo American | smartrecruiters | company `AngloAmericanDeBeersGroup` | 52 | 52 | 77 listed; found via the SmartRecruiters link on the apply page. |
| Rio Tinto | workday | `riotinto` / wd3 / `RioTinto_Careers` | 70 | 70 | 140 on the board; site name from the careers page. |
| BHP | sitemap | `careers.bhp.com/sitemap.xml` | 29 | 29 | SuccessFactors, 119 jobs listed; 60 pages per run, rest queued. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Ørsted | Vacancy list rendered by JavaScript; no feed or ATS link in the source. | JavaScript only. |
| Bunge | jobs.bunge.com is SuccessFactors with an empty sitemap and no feed; bunge.com answers 403. | No public feed. |
| Sucden | Job-opportunities page lists no openings, only a spontaneous application form. | No listings. |
| Czarnikow | Jobs embedded from an Occupop Next.js app. | JavaScript only. |
| Wilmar | Careers page links only regional portals (Indonesia, ANZ, Vietnam). | No group feed. |
| Amaggi | No careers page or ATS link found. | Portal not identified. |
| Concord Resources | Careers page without listings or ATS link. | Portal not identified. |
| IXM | ixmetals.com refuses connections from plain clients. | Bot protection. |
| Traxys | Static careers page with no listings. | No listings. |
| Ocean Partners | oceanpartners.com answers 403 to non-browser clients. | Bot protection. |
| Transamine | No careers page. | Portal not identified. |

## Added on 2026-11-14 (evening routine)

First 20 rows of `backlog.md` (tier 5, Vale to E.ON); tiers 1-4 were empty and the wishlist had no new rows. Plain HTTP only. "Postings" is the number of raw roles at the source; "In scope" is the number of openings stored after the scope filter.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Aurubis | sitemap | `jobs.aurubis.com/sitemap-jobs.xml` | 54 | 0 | Job-shop portal; German plant and engineering roles. |
| Boliden | workday | `boliden` / wd3 / `BolidenJobs` | 45 | 37 | Sweden, Finland, Norway; none in target cities. |
| Engelhart Commodities Trading Partners | greenhouse | board `engelhart` | 3 | 0 | London data engineer, Berlin, Houston/Stamford treasury analyst. |
| BB Energy | custom (`bamboohr`) | subdomain `bbenergy` | 8 | 0 | London roles are legal, business development and engineering. |
| Danske Commodities | sitemap (index_urls) | `danskecommodities.com/join-us/vacancies` | 5 | 5 | Links harvested from the vacancies page; Aarhus, Singapore, Italy. |
| InCommodities | sitemap (index_urls) | `incommoditiesas.hr-on.com/` | 6 | 6 | Hr-On listing page. |
| MET Group | smartrecruiters | company `metgroup` | 64 | 13 | Zug, Geneva and other offices. |
| EnBW | custom (`phenom`) | `careers.enbw.com`, de_de / de | 139 | 0 | German-language Phenom site, Germany roles. |
| E.ON | custom (`oracle`) | `fa-eylc-saasfaeuraprod1` / `CX_1` | 145 | 1 | Oracle HCM behind jobs.eon.com. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Vale | Eightfold portal (vale.eightfold.ai, ~90 roles); its JSON API answers, but only Vale uses Eightfold tonight so no adapter was written. | No adapter. |
| Litasco | Careers page without listings or ATS link. | Portal not identified. |
| SOCAR Trading | No careers page. | Portal not identified. |
| Aramco Trading | SuccessFactors job search (career23.sapsf.com) rendered by JavaScript, no sitemap. | JavaScript only. |
| ADNOC Global Trading | Site resets connections from plain clients. | Bot protection. |
| PetroChina International (London) | Site resets connections from plain clients. | Bot protection. |
| Unipec UK | Site unreachable through the proxy (502). | Unreachable. |
| Alvean | WordPress site without careers page. | Portal not identified. |
| Ameropa | Career page links only to LinkedIn. | No own listings. |
| Varo Energy | varopreem.com has no careers page. | Portal not identified. |
| Trailstone | Minimal homepage, no careers page. | Portal not identified. |

## Added on 2026-11-15 (evening routine)

First 20 rows of `backlog.md` (tier 5, Iberdrola to Affinity Shipping); tiers 1-4 were empty and the wishlist had no new rows. Plain HTTP only. "Postings" is the number of raw roles at the source (for sitemap sources, the job pages opened tonight); "In scope" is the number of openings stored after the scope filter.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Octopus Energy | lever | company `octoenergy` | 156 | 30 | London, Paris, Italy, Germany. |
| SSE | sitemap | `careers.sse.com/sitemap.xml`, `/jobs/<slug>` pages | 80 | 27 | JSON-LD on job pages; 60 pages per run, rest queued. |
| Puma Energy | workday | `trafigura` / wd3 / `Puma_Energy_Careers` | 44 | 7 | Shared Trafigura tenant; mostly Africa, Asia, Latin America. |
| Repsol Trading | workday | `repsol` / wd3 / `Repsol` | 59 | 18 | Whole-of-Repsol board; trading not separated. |
| OMV Trading | sitemap | `careers.omv.com/sitemap.xml`, target-city and Vienna pages | 8 | 0 | SuccessFactors, ~67 jobs, mostly Romania and Austria. |
| Galp Trading | sitemap | `jobs.galp.com/sitemap.xml` | 20 | 20 | SuccessFactors; mostly Portugal and Spain. |
| Moeve (Cepsa) Trading | sitemap | `jobs.moeveglobal.com/sitemap.xml` | 38 | 31 | SuccessFactors; Madrid and Spanish refineries. |
| Phillips 66 (UK) | sitemap | `careers.phillips66.com/sitemap.xml`, London/Jarrow/Houston pages | 37 | 3 | SuccessFactors, ~75 jobs, nearly all US. |
| Clarksons | sitemap | `careers.clarksons.com/sitemap.xml` | 37 | 18 | SuccessFactors; London broking roles. Early-careers programmes on clarksons.com. |
| Howe Robinson Partners | sitemap (index_urls) | `howerobinson.com/careers/` | 3 | 2 | WordPress directory pages; London, Singapore, Hamburg. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Iberdrola | iberdrola.com answers 403; Workday tenant exists but site name unknown. | Bot protection. |
| Drax | drax.com answers 403; careers site unreachable. | Bot protection. |
| ScottishPower | scottishpower.com answers 403. | Bot protection. |
| National Grid | careers.nationalgrid.com and nationalgrid.com answer 403. | Bot protection. |
| Eni Plenitude | Eni group Taleo portal, JavaScript search, no feed. | JavaScript only. |
| Duferco | WordPress site, no careers page (404). | Portal not identified. |
| Gerald Group | Careers page is an empty stub; main site refuses connections. | No listings. |
| Braemar | Roles page is static text linking to a LinkedIn search. | No own listings. |
| Simpson Spence Young | ssy.co unreachable through the proxy; no careers page found on ssyglobal.com. | Unreachable. |
| Affinity Shipping | Careers page states no open positions (CV submission only). | No listings. |

## Added on 2026-11-16 (evening routine)

First 20 rows of `backlog.md` (tier 5 Maersk to Amerex, tier 6 Bank of England to EBRD); the wishlist had no new rows. CSC Commodities was already covered by the Marex entry (Marex portal, breezy.hr) and did not use a slot. Plain HTTP only. "Postings" is the count the run log printed; "In scope" is the number of openings stored after the scope filter.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Bank of England | custom `oracle` | `eoff.fa.em1.ukg.oraclecloud.com`, site `CX_1001` | 3 | 3 | Oracle HCM REST API, London. |
| European Central Bank | sitemap (index listing) | `talent.ecb.europa.eu/careers/SearchJobs`, 10 per page | 2 | 2 | Avature; Frankfurt, no location in the listing, so rows carry no city. |
| Swiss National Bank | sitemap | `careers.snb.ch/sitemap.xml` | 10 | 10 | SuccessFactors; Swiss cash-logistics and IT roles, few finance. |
| European Banking Authority | sitemap (index_urls) | `careers.eba.europa.eu/en` | 1 | 1 | Own recruitment site, Paris; 3 vacancies linked, page titles only. |
| EBRD | sitemap (rss_url) | `jobs.ebrd.com/sitemap.xml` | 6 | 6 | SuccessFactors Google-Jobs RSS, London HQ. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Maersk | Vacancies page is a JavaScript search; Workday tenant answers 406. | JavaScript only. |
| MSC | msc.com answers 403. | Bot protection. |
| Oldendorff | Static office-careers page, no feed. | No feed. |
| Klaveness | Squarespace vacancies page, no feed. | No feed. |
| Hafnia | hafniabw.recruiterpal.com AngularJS portal. | JavaScript only. |
| Frontline | Corporate site, no careers page. | No listings. |
| Scorpio Tankers | Corporate site, no careers page. | No listings. |
| d'Amico | damicoship.join-us.it refuses connections through the proxy. | Unreachable. |
| Grimaldi | Connection reset from plain clients. | Bot protection. |
| Amerex | amerexenergy.com answers 403. | Bot protection. |
| Banca d'Italia | Competitions on a static page, no ATS. | No feed. |
| Banque de France | banque-france.fr answers 403. | Bot protection. |
| Central Bank of Ireland | Candidate Manager list is server-rendered (2 roles) but has no location, so the scope filter would drop them; could be revisited with a default-location option. | No location. |
| Bank for International Settlements | Workday `bis`/wd3/External answered a manual request but the adapter got a Cloudflare 429; retry later. | Bot protection. |
| ESMA | Vacancies on esmacareers.adequasys.com login portal. | No feed. |

## Added on 2026-11-17 (evening routine)

First 20 rows of `backlog.md` after CSC Commodities (tier 6 Fitch Ratings to Jupiter, then Fidelity International in tier 7); the wishlist had no new rows. CSC Commodities was already covered by the Marex entry and did not use a slot. Plain HTTP only. "Postings" is the count the run log printed (rows kept by the scope filter); "In scope" is the number of openings stored. Workday answered the adapter with 429 for part of the evening (an existing entry, Stout, failed the same way), so four new Workday entries were confirmed with curl only.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Moody's | sitemap | `careers.moodys.com/en/sitemap.xml`, `/en/job/` pages | 7 | 7 | JSON-LD pages, ~340 roles worldwide; 223 pages still to open on later runs. |
| MSCI | sitemap | `careers.msci.com/sitemap.xml`, `/job/` pages | 9 | 9 | iCIMS behind own site, ~130 roles worldwide. |
| Lloyd's of London | workday | `lloyds` / wd3 / `Lloyds-of-London` | 1 | 1 | 8 roles in total. |
| Aon | custom `jibe` | `jobs.aon.com` | 129 | 129 | iCIMS/Jibe API, ~1000 roles worldwide. |
| Marsh McLennan | custom `phenom` | `careers.marsh.com`, lang `en`, country `global` | 91 | 91 | Phenom People site. |
| WTW | sitemap | `careers.wtwco.com/sitemap.xml`, `/jobs/` pages | 18 | 18 | ~640 job pages worldwide; 532 pages still to open on later runs. |
| Legal & General | sitemap (index_urls) | `careers.legalandgeneral.com/jobs` | 0 | 0 | Server-rendered list, first page only (~10 roles, none in scope tonight). |
| Phoenix Group | custom `oracle` | `fa-enor-saasfaprod1.fa.ocs.oraclecloud.com`, site `CX` | 9 | 9 | Oracle HCM REST API. |
| Schroders | custom `oracle` | `ekbq.fa.em2.oraclecloud.com`, site `CX_2` | 20 | 20 | Oracle HCM REST API. |
| abrdn | workday | `abrdn` / wd3 / `abrdn` | 6 | 6 | 21 roles in total. |
| Morningstar DBRS | workday | `morningstar` / wd5 / `MorningstarDBRS` | not run (429) | not run | curl: 54 roles in total. |
| Prudential plc | workday | `prudential` / wd3 / `prudential` | not run (429) | not run | curl: 468 roles, nearly all Asia/Africa; expect few in scope. |
| M&G | workday | `mgpru` / wd3 / `mandgprudential` | not run (429) | not run | curl: 143 roles in total. |
| Fidelity International | workday | `fil` / wd3 / `001` | not run (429) | not run | curl: 79 roles in total; graduate programmes are on fidelityinternational.tal.net. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Fitch Ratings | fitchgroup.com and careers.fitchgroup.com fail through the proxy (502 / refused). | Unreachable. |
| Scope Ratings | Careers page is a client-rendered single-page app. | JavaScript only. |
| FactSet | Careers page is client-rendered, no ATS link or feed in the HTML. | JavaScript only. |
| Nationwide Building Society | nationwide-jobs.co.uk is an Angular app, sitemap answers 404. | JavaScript only. |
| Legal & General Investment Management | Hires on the Legal & General group site (see that entry); am.landg.com careers page answers 404. | No separate feed. |
| Jupiter Asset Management | No careers page or ATS link reachable from plain clients. | No listings. |

## Added on 2026-11-18 (evening routine)

First 20 slots of `backlog.md` (tier 7 from Baillie Gifford to Janus Henderson, then Neuberger Berman and Nuveen); the wishlist had no new rows. AXA Investment Managers (now part of BNP Paribas AM, entry BNP Paribas) and Eurizon Capital (hires on the Intesa Sanpaolo portal, entry Intesa Sanpaolo) were already covered and did not use a slot. Plain HTTP only. "Postings" is the count the run log printed (rows kept by the scope filter); "In scope" is the same number. Workday answered the adapter with 429 all evening, so the seven new Workday entries are unconfirmed by the adapter; Baillie Gifford's board was confirmed with curl (11 roles), the others were read from the employer's own careers page.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Baillie Gifford | workday | `bailliegifford` / wd3 / `BaillieGiffordCareers` | not run (429) | not run | curl: 11 roles in total. |
| Aviva Investors | workday | `aviva` / wd1 / `Aviva_Investors_External` | not run (429) | not run | Site linked from careers.avivainvestors.com. |
| Amundi | sitemap (rss_url) | `jobs.amundi.com/handlers/offerRss.ashx?LCID=2057` | 6 | 6 | ~100 roles in the feed (Paris, Luxembourg 15, Ireland 12, Italy 3); feed has only a postcode, so most fall out of scope. |
| GAM | workday | `gam` / wd3 / `GAM` | not run (429) | not run | Linked from gam.com/en/careers. |
| LGT | sitemap (index_urls) | `lgt.com/global-en/career/jobs`, 5 list pages | 18 | 18 | Server-rendered list; LGT Capital Partners is a separate entry. |
| Capital Group | workday | `capgroup` / wd1 / `capitalgroupcareers` | not run (429) | not run | Mostly US roles expected. |
| Wellington Management | workday | `wellington` / wd5 / `External` | not run (429) | not run | |
| T. Rowe Price | workday | `troweprice` / wd5 / `TRowePriceInternational` | not run (429) | not run | International site; US site is `TRowePrice`. |
| Franklin Templeton | custom `phenom` | `careers.franklintempleton.com`, six-country filter | 8 | 8 | Phenom People site over Workday. |
| Invesco | workday | `invesco` / wd1 / `IVZ` | not run (429) | not run | |
| Janus Henderson | sitemap | `jobs.janushenderson.com/sitemap.xml`, `/job/` pages | 7 | 7 | SuccessFactors; 76 pages still to open on later runs. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Natixis Investment Managers | im.natixis.com has no careers page (404); hiring is on the JavaScript Natixis group portal. | JavaScript only. |
| Anima SGR | Static page with an email address, no vacancy list. | No feed. |
| Generali Investments | Hires on the gogenerali.com group portal, JavaScript app. | JavaScript only. |
| Azimut | Next.js page with only an unsolicited-application link. | No listings. |
| Kairos Partners | No careers page or vacancy list. | No listings. |
| Algebris Investments | algebris.com answers 403. | Bot protection. |
| Vanguard | vanguardjobs.com WordPress site, JavaScript search, US-only postings, no job sitemap. | JavaScript only. |
| Neuberger Berman | nb.com answers 429, careers.nb.com unreachable through the proxy. | Bot protection. |
| Nuveen | TIAA Phenom site (careers.tiaa.org/nuveen); the widgets API answers 404 under the site prefix. | No feed. |

## Added on 2026-11-19 (evening routine)

First 20 slots of `backlog.md` (tier 7 from Allianz Global Investors to Elliott Management); the wishlist had no new rows and none of the 20 was already in the registry. Walleye Capital has two Greenhouse boards (full-time and students), so it got two entries. Plain HTTP only. "Postings" is the count the run log printed (rows kept by the scope filter); "In scope" is the same number. Workday and Workable answered the adapter with 429 for DWS and Caxton Associates (curl worked and confirmed the boards), so those two are unconfirmed by the adapter. Robeco's adapter run succeeded after two 429 retries.

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Allianz Global Investors | custom `phenom` | `careers.allianz.com`, lang `en_global`, six-country filter | 335 | 335 | Allianz group portal; includes group roles, not only AGI (the adapter has no keyword option). |
| DWS | workday | `db` / wd3 / `DWSWebsite` | not run (429) | not run | curl: 83 roles worldwide. |
| Robeco | workday | `robeco` / wd3 / `robecoexternalcareers` | 0 | 0 | curl: 10 roles, mostly Rotterdam. |
| Caxton Associates | workable | account `caxton` | not run (429) | not run | curl: 30 roles incl. London programmes. |
| ExodusPoint | greenhouse | board `exoduspoint` | 2 | 2 | 5 on the board, mostly Asia and US. |
| Verition | greenhouse | board `veritiongroupllc` | 1 | 1 | 14 on the board, mostly US and Asia. |
| Walleye Capital | greenhouse | board `walleyecapital-external-fulltime` | 0 | 0 | 13 roles, all New York. |
| Walleye Capital (students) | greenhouse | board `walleyecapital-external-students` | 0 | 0 | 1 role (Miami). |
| Winton | greenhouse | board `winton` | 3 | 3 | 7 London roles, EU-hosted board; includes the graduate quant role. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Carmignac | Careers page says "This website requires JS enabled and cookies". | JavaScript only. |
| Comgest | Static job-offers page with a generic application form. | No listings. |
| Marshall Wace | Static join-us pages (early careers, internships); no ATS link. | No feed. |
| Rokos Capital Management | Static page with a careers email address. | No listings. |
| BlueCrest Capital | No careers page (404); the SmartRecruiters "BlueCrest" board is another company. | No listings. |
| Eisler Capital | eislercapital.com returns 502 through the proxy; no other page found. | Unreachable. |
| Balyasny Asset Management | Programme pages only; vacancies on a Salesforce site that needs JavaScript. | JavaScript only. |
| Aspect Capital | HiBob careers widget rendered in the browser. | JavaScript only. |
| Lansdowne Partners | Static page: "There are currently no open positions". | No listings. |
| Egerton Capital | No careers page (404). | No listings. |
| TCI Fund Management | No careers page (404). | No listings. |
| Elliott Management | /careers redirects to the contact page. | No listings. |

## Added on 2026-11-20 (evening routine)

The wishlist had no new rows. First slots of `backlog.md` (tier 1 to tier 4, Raine Group to Davy); Centerview Partners and BGC Group were already in the registry and did not use slots (22 rows removed from the queue, 20 processed). Plain HTTP only. Workable and Workday probes were rate-limited (429) tonight, so a Workable or Workday board for the manual employers cannot be ruled out. "Postings" is the count the run log printed (rows kept by the scope filter).

| Company | ATS | Config | Postings | In scope | Notes |
|---|---|---|---|---|---|
| Raine Group | lever | company `raine` | 0 | 0 | 1 role on the board (2027 off-cycle analyst, Singapore), out of geography. |
| Oakley Capital | greenhouse | board `oakleycapital` | 0 | 0 | Board exists, empty tonight. |
| Adams Street Partners | greenhouse | board `adamsstreetpartners` | 2 | 2 | 13 roles on the board, mostly US; one London analyst role. |

Manual (no feed reachable without a browser):

| Company | What was found | Difficulty |
|---|---|---|
| Qatalyst Partners | Only mailto careers addresses. | No listings. |
| Livingstone Partners | Site answers 403. | Bot protection. |
| GP Bullhound | Careers/jobs pages without a list; Sesame HR link answers 503. | No listings. |
| Bryan Garnier & Co | 502 through the proxy. | Unreachable. |
| IK Partners | Site answers 403. | Bot protection. |
| Park Square Capital | Site answers 403. | Bot protection. |
| Cerberus Capital Management | Site answers 403. | Bot protection. |
| Clayton Dubilier & Rice | No careers page (404). | No listings. |
| Eight Roads Ventures | No careers page (404). | No listings. |
| Argos Wityu | 502 through the proxy. | Unreachable. |
| Vitruvian Partners | No careers page (404). | No listings. |
| Cairn Capital | TLS handshake fails. | Unreachable. |
| Investcorp | Careers page without vacancy list or ATS link. | No listings. |
| Cambridge Associates | Site answers 403. | Bot protection. |
| Euroclear | Careers site answers 403; no public ATS found. | Bot protection. |
| LCH | Hires via the LSEG group portal (entry LSEG). | Covered by LSEG. |
| Davy | Editorial careers pages, no vacancy list. | No listings. |
