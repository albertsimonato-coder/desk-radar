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
| Italgas | corporate | 2 | |
| Poste Italiane | corporate | 2 | |
| Generali | corporate | 1 | Group finance, investments |
| Unipol | corporate | 2 | |
| Edison | corporate | 1 | Energy trading in Milan |
| Saipem | corporate | 2 | |
| Tenaris | corporate | 2 | |
| Moncler | corporate | 2 | |
| Campari Group | corporate | 2 | |
| Barilla | corporate | 2 | |
| Ferrero | corporate | 2 | Luxembourg HQ |
| Nestlé | corporate | 2 | Vevey treasury |
| Unilever | corporate | 2 | |
| Diageo | corporate | 2 | |
| Vodafone | corporate | 2 | |
| BAT | corporate | 2 | |
| GSK | corporate | 2 | |
| AstraZeneca | corporate | 2 | |
| Rolls-Royce | corporate | 2 | |
| BAE Systems | corporate | 2 | |
| Airbus | corporate | 2 | |
| LVMH | corporate | 2 | |
| L'Oréal | corporate | 2 | |
| Danone | corporate | 2 | |
| Schneider Electric | corporate | 2 | |
| Novartis | corporate | 2 | |
| Roche | corporate | 2 | |
| ABB | corporate | 2 | |
| Richemont | corporate | 2 | |
| Swiss Re | corporate | 1 | |
| Zurich Insurance | corporate | 1 | |
| Cassa Depositi e Prestiti | corporate | 1 | |
| SACE | corporate | 2 | |
| Mundys (Atlantia) | corporate | 2 | |
| Fincantieri | corporate | 2 | |
| Iveco Group | corporate | 2 | |
| CNH Industrial | corporate | 2 | |
| Prysmian | corporate | 2 | |
| Nexi | corporate | 2 | |
| Webuild | corporate | 2 | |
| Hera | corporate | 2 | Energy trading |
| Iren | corporate | 2 | Energy trading |
| Ryanair | corporate | 2 | Dublin treasury |
| CRH | corporate | 2 | |
| Kerry Group | corporate | 2 | |
| Flutter Entertainment | corporate | 2 | |
| ArcelorMittal | corporate | 2 | Luxembourg HQ |
| SES | corporate | 2 | Luxembourg |
| Allianz | corporate | 2 | |
| AXA | corporate | 2 | |
| Munich Re | corporate | 2 | |

## Tier 4: sales and trading, brokers, exchanges, market infrastructure

| Company | Group | Priority | Hint |
|---|---|---|---|
| BNY | bank | 1 | |
| State Street | bank | 2 | |
| Northern Trust | bank | 2 | |
| Scotiabank | bank | 1 | Global Banking and Markets, London |
| CIBC | bank | 2 | |
| BMO Capital Markets | bank | 2 | |
| ANZ | bank | 2 | |
| Commerzbank | bank | 1 | |
| Danske Bank | bank | 2 | |
| SEB | bank | 2 | |
| DNB | bank | 2 | |
| KBC | bank | 2 | |
| ABN AMRO | bank | 1 | |
| Erste Group | bank | 2 | |
| Raiffeisen Bank International | bank | 2 | |
| Bank of China (UK) | bank | 2 | |
| ICBC Standard Bank | bank | 1 | London commodities and FICC |
| SMBC Group EMEA | bank | 1 | |
| Daiwa Capital Markets Europe | bank | 2 | |
| Investec | bank | 1 | |
| Close Brothers | bank | 2 | Winterflood Securities |
| Cantor Fitzgerald | bank | 1 | |
| BGC Group | bank | 1 | |
| Tradition (Compagnie Financière Tradition) | bank | 1 | |
| ODDO BHF | bank | 1 | |
| Kepler Cheuvreux | bank | 1 | |
| Banco BPM | bank | 1 | |
| BPER Banca | bank | 2 | |
| Credem | bank | 2 | |
| Banca Mediolanum | bank | 2 | |
| FinecoBank | bank | 2 | |
| Banca Generali | bank | 2 | |
| Banca Ifis | bank | 2 | |
| illimity | bank | 2 | |
| Vontobel | bank | 1 | Zurich |
| EFG International | bank | 2 | |
| Mirabaud | bank | 2 | Geneva |
| Bank Syz | bank | 2 | |
| Zürcher Kantonalbank | bank | 1 | |
| Raiffeisen Switzerland | bank | 2 | |
| Banque Internationale à Luxembourg | bank | 1 | |
| Spuerkeess | bank | 2 | |
| Quintet Private Bank | bank | 2 | |
| CACEIS | bank | 2 | |
| Bpifrance | bank | 2 | |
| La Banque Postale | bank | 2 | |
| CIC Market Solutions | bank | 2 | |
| Swissquote | bank | 2 | |
| IG Group | bank | 1 | |
| CMC Markets | bank | 2 | |
| Saxo Bank | bank | 2 | |
| Interactive Brokers | bank | 2 | |
| XTB | bank | 2 | |
| eToro | bank | 2 | |
| Plus500 | bank | 2 | |
| Tradeweb | exchange | 1 | |
| MarketAxess | exchange | 2 | |
| Bloomberg | exchange | 1 | Financial products, analytics |
| CME Group | exchange | 1 | |
| Cboe | exchange | 2 | |
| Nasdaq | exchange | 2 | |
| SIX Group | exchange | 1 | Zurich |
| London Metal Exchange | exchange | 1 | |
| EEX (European Energy Exchange) | exchange | 1 | |
| Liquidnet | exchange | 2 | |
| Instinet | exchange | 2 | |

## Tier 5: commodities trading, energy, metals, agri, shipping

| Company | Group | Priority | Hint |
|---|---|---|---|
| Freepoint Commodities | commodities | 1 | |
| Hartree Partners | commodities | 1 | |
| Mabanaft | commodities | 1 | |
| Petroineos | commodities | 1 | |
| Equinor | commodities | 1 | Marketing, midstream and processing; London trading |
| Eni Trading & Shipping | commodities | 1 | Probably on the Eni portal |
| Uniper | commodities | 1 | |
| RWE Supply & Trading | commodities | 1 | |
| EDF Trading | commodities | 1 | |
| ENGIE Global Energy Management & Sales | commodities | 1 | |
| Axpo | commodities | 1 | Baden, Milan |
| Alpiq | commodities | 1 | |
| BKW | commodities | 2 | |
| Statkraft | commodities | 1 | |
| Ørsted | commodities | 2 | |
| Vattenfall | commodities | 2 | |
| Centrica | commodities | 1 | Centrica Energy |
| SEFE | commodities | 1 | |
| Bunge | commodities | 1 | Geneva |
| COFCO International | commodities | 1 | Geneva |
| Olam Agri | commodities | 1 | |
| ED&F Man | commodities | 1 | |
| Sucden | commodities | 1 | |
| Czarnikow | commodities | 2 | |
| Wilmar | commodities | 2 | |
| Amaggi | commodities | 2 | |
| Concord Resources | commodities | 1 | |
| IXM | commodities | 1 | Geneva |
| Traxys | commodities | 2 | Luxembourg |
| Ocean Partners | commodities | 2 | |
| Transamine | commodities | 2 | Geneva |
| Anglo American | commodities | 1 | Marketing in London |
| Rio Tinto | commodities | 1 | Commercial in London / Singapore |
| BHP | commodities | 2 | |
| Vale | commodities | 2 | |
| Aurubis | commodities | 2 | |
| Boliden | commodities | 2 | |
| Litasco | commodities | 1 | Geneva |
| SOCAR Trading | commodities | 1 | Geneva |
| Aramco Trading | commodities | 2 | |
| ADNOC Global Trading | commodities | 2 | |
| PetroChina International (London) | commodities | 2 | |
| Unipec UK | commodities | 2 | |
| Alvean | commodities | 2 | Geneva |
| Ameropa | commodities | 2 | |
| Engelhart Commodities Trading Partners | commodities | 1 | |
| BB Energy | commodities | 1 | |
| Varo Energy | commodities | 2 | |
| Trailstone | commodities | 1 | |
| Danske Commodities | commodities | 1 | |
| InCommodities | commodities | 1 | |
| MET Group | commodities | 1 | Zug |
| EnBW | commodities | 2 | |
| E.ON | commodities | 2 | |
| Iberdrola | commodities | 2 | |
| Octopus Energy | commodities | 2 | |
| Drax | commodities | 2 | |
| SSE | commodities | 2 | |
| ScottishPower | commodities | 2 | |
| National Grid | commodities | 2 | |
| Eni Plenitude | commodities | 2 | |
| Duferco | commodities | 2 | Lugano |
| Gerald Group | commodities | 2 | |
| Puma Energy | commodities | 2 | Geneva |
| Repsol Trading | commodities | 2 | |
| OMV Trading | commodities | 2 | |
| Galp Trading | commodities | 2 | Geneva |
| Moeve (Cepsa) Trading | commodities | 2 | |
| Phillips 66 (UK) | commodities | 2 | |
| Clarksons | commodities | 1 | Shipbroking, London |
| Braemar | commodities | 2 | |
| Simpson Spence Young | commodities | 2 | |
| Howe Robinson Partners | commodities | 2 | |
| Affinity Shipping | commodities | 2 | |
| Maersk | commodities | 2 | |
| MSC | commodities | 2 | Geneva |
| Oldendorff | commodities | 2 | |
| Klaveness | commodities | 2 | |
| Hafnia | commodities | 2 | |
| Frontline | commodities | 2 | |
| Scorpio Tankers | commodities | 2 | |
| d'Amico | commodities | 2 | |
| Grimaldi | commodities | 2 | |
| CSC Commodities | commodities | 2 | |
| Amerex | commodities | 2 | |

## Tier 6: market risk, treasury, central banks, ratings, insurance markets

| Company | Group | Priority | Hint |
|---|---|---|---|
| Bank of England | corporate | 1 | |
| European Central Bank | corporate | 1 | |
| Banca d'Italia | corporate | 1 | |
| Swiss National Bank | corporate | 2 | |
| Banque de France | corporate | 2 | |
| Central Bank of Ireland | corporate | 2 | |
| Bank for International Settlements | corporate | 2 | Basel |
| European Banking Authority | corporate | 2 | Paris |
| ESMA | corporate | 2 | Paris |
| EBRD | bank | 1 | |
| Fitch Ratings | advisory | 1 | |
| Moody's | advisory | 1 | |
| Morningstar DBRS | advisory | 2 | |
| Scope Ratings | advisory | 2 | |
| MSCI | advisory | 2 | |
| FactSet | advisory | 2 | |
| Lloyd's of London | corporate | 2 | |
| Aon | advisory | 2 | |
| Marsh McLennan | advisory | 2 | |
| WTW | advisory | 2 | |
| Nationwide Building Society | bank | 2 | Treasury |
| Legal & General | corporate | 2 | |
| Prudential plc | corporate | 2 | |
| Phoenix Group | corporate | 2 | |

## Tier 7: asset managers, hedge funds, quant and market makers

| Company | Group | Priority | Hint |
|---|---|---|---|
| Schroders | asset_manager | 1 | |
| abrdn | asset_manager | 2 | |
| Legal & General Investment Management | asset_manager | 2 | |
| M&G | asset_manager | 2 | |
| Jupiter Asset Management | asset_manager | 2 | |
| Fidelity International | asset_manager | 1 | |
| Baillie Gifford | asset_manager | 2 | |
| Aviva Investors | asset_manager | 2 | |
| Amundi | asset_manager | 1 | Paris, Milan, Luxembourg |
| AXA Investment Managers | asset_manager | 2 | |
| Natixis Investment Managers | asset_manager | 2 | |
| Eurizon Capital | asset_manager | 1 | Milan |
| Anima SGR | asset_manager | 1 | Milan |
| Generali Investments | asset_manager | 1 | |
| Azimut | asset_manager | 2 | |
| Kairos Partners | asset_manager | 2 | |
| Algebris Investments | asset_manager | 1 | London / Milan |
| GAM | asset_manager | 2 | |
| LGT | asset_manager | 2 | |
| Capital Group | asset_manager | 2 | |
| Vanguard | asset_manager | 2 | |
| Wellington Management | asset_manager | 2 | |
| T. Rowe Price | asset_manager | 2 | |
| Franklin Templeton | asset_manager | 2 | |
| Invesco | asset_manager | 2 | |
| Janus Henderson | asset_manager | 2 | |
| Neuberger Berman | asset_manager | 2 | |
| Nuveen | asset_manager | 2 | |
| Allianz Global Investors | asset_manager | 2 | |
| DWS | asset_manager | 2 | |
| Robeco | asset_manager | 2 | |
| Carmignac | asset_manager | 2 | |
| Comgest | asset_manager | 2 | |
| Marshall Wace | asset_manager | 1 | |
| Caxton Associates | asset_manager | 1 | |
| Rokos Capital Management | asset_manager | 1 | |
| BlueCrest Capital | asset_manager | 1 | |
| Eisler Capital | asset_manager | 1 | |
| ExodusPoint | asset_manager | 1 | |
| Balyasny Asset Management | asset_manager | 1 | |
| Verition | asset_manager | 1 | |
| Walleye Capital | asset_manager | 2 | |
| Winton | asset_manager | 2 | |
| Aspect Capital | asset_manager | 2 | |
| Lansdowne Partners | asset_manager | 2 | |
| Egerton Capital | asset_manager | 2 | |
| TCI Fund Management | asset_manager | 2 | |
| Elliott Management | asset_manager | 1 | |
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
| Eni | 2026-11-08 | manual (Oracle HCM on jobs.eni.com, TLS chain fails verification through the proxy; retry later) |
| Leonardo | 2026-11-08 | live (Workday, 849 roles, 253 in scope) |
| Stellantis | 2026-11-08 | manual (site 403; WordPress careers site with JavaScript search, no job feed) |
| Ferrari | 2026-11-08 | live (SuccessFactors sitemap, Italian and target-city pages only, 1 role, 1 in scope) |
| Prada Group | 2026-11-08 | live (SuccessFactors sitemap, target-city pages only, 26 roles, 26 in scope) |
| EssilorLuxottica | 2026-11-08 | manual (JavaScript job search, no feed found) |
| Pirelli | 2026-11-08 | manual (JavaScript job search, no feed found) |
| TIM (Telecom Italia) | 2026-11-08 | manual (JavaScript job search, no feed found) |
| A2A | 2026-11-08 | manual (Oracle HCM API blocked by WAF, 403) |
| Snam | 2026-11-08 | manual (no careers page reachable) |
| Terna | 2026-11-08 | manual (no ATS link or feed found) |
