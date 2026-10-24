# Source inventory

Live inventory taken on 2026-10-23 with plain HTTP requests (no browser). "Live" means the
adapter was verified end to end against the real endpoint; the posting count is what the
endpoint reported that day.

## Live sources (51)

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
| Pictet | SAP SuccessFactors (career012.successfactors.eu, company `banquepict`) | No sitemap on the SF host. |
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
| Natixis | recrutement.natixis.com, portal not identified | Unknown |
| Crédit Agricole CIB | Talentsoft/Cegid (jobs.ca-cib.com) | Medium: try sitemap |
| Banca Monte dei Paschi di Siena | Taleo career section (lavoraconnoi.mps.it); the list is loaded by Taleo's internal joblist.ajax POST, ~20 openings | Medium: replicate the AJAX call |
| EIB, EIF | PeopleSoft eRecruitment | Hard |
| Banque de Luxembourg | Portal not identified | Unknown |
| Peel Hunt, Citadel, Citadel Securities, StoneX | 403 to non-browser clients (Citadel's job pages are also blocked; their sitemap only lists articles) | Needs browser |
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
