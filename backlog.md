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
| Deloitte UK | advisory | 1 | Financial advisory: valuation, M&A, transaction services |
| PwC UK | advisory | 1 | Deals practice |
| KPMG UK | advisory | 1 | Deal advisory |
| Deloitte Italia | advisory | 1 | |
| PwC Italia | advisory | 1 | |
| KPMG Italia | advisory | 1 | |
| PwC Luxembourg | advisory | 2 | |
| KPMG Luxembourg | advisory | 2 | |
| Deloitte Luxembourg | advisory | 2 | |
| FTI Consulting | advisory | 1 | Corporate finance & restructuring, economic consulting |
| AlixPartners | advisory | 1 | |
| Accuracy | advisory | 1 | Paris-based financial advisory, Milan and London offices |
| Eight Advisory | advisory | 1 | |
| Teneo | advisory | 2 | Financial advisory arm |
| Interpath Advisory | advisory | 2 | |
| Evelyn Partners | advisory | 2 | |
| Stout | advisory | 2 | Valuation advisory, London office |
| Alantra | boutique | 1 | Madrid HQ, Milan and London |
| Oaklins | boutique | 2 | |
| Clearwater International | boutique | 2 | |
| DC Advisory | boutique | 1 | |
| Baird | boutique | 1 | Global investment banking, London |
| Stifel | bank | 1 | Includes Stifel Europe |
| William Blair | boutique | 1 | |
| Raymond James | boutique | 2 | |
| Piper Sandler | boutique | 2 | |
| Harris Williams | boutique | 2 | |
| Cavendish | boutique | 2 | UK mid-market |
| Arma Partners | boutique | 2 | |
| Fenchurch Advisory | boutique | 2 | |
| Equita | boutique | 1 | Milan: investment banking and sales & trading |
| Vitale & Co | boutique | 1 | Milan |
| Fineurop Soditic | boutique | 2 | Milan |
| Klecha & Co | boutique | 2 | Milan / London |
| Ethica Group | boutique | 2 | Milan |
| Intermonte | boutique | 1 | Milan: sales & trading and investment banking |
| Banca Akros | bank | 1 | Banco BPM group CIB |
| Banca Profilo | bank | 2 | |
| Deutsche Numis | bank | 1 | |
| Berenberg | bank | 1 | London: S&T, research, investment banking |
| Greenhill (Mizuho) | boutique | 2 | May sit on the Mizuho portal |
| Natixis Partners | boutique | 2 | |

## Tier 2: private equity, private credit, infrastructure

| Company | Group | Priority | Hint |
|---|---|---|---|
| KKR | asset_manager | 1 | |
| TPG | asset_manager | 1 | |
| Bain Capital | asset_manager | 1 | |
| CVC Capital Partners | asset_manager | 1 | Luxembourg, London, Milan |
| EQT | asset_manager | 1 | |
| Permira | asset_manager | 1 | |
| Cinven | asset_manager | 1 | |
| Advent International | asset_manager | 1 | |
| Warburg Pincus | asset_manager | 1 | |
| Hg | asset_manager | 1 | |
| Bridgepoint | asset_manager | 1 | |
| PAI Partners | asset_manager | 1 | |
| Eurazeo | asset_manager | 1 | |
| Investindustrial | asset_manager | 1 | London / Milan / Lugano |
| Clessidra | asset_manager | 1 | Milan |
| Ambienta | asset_manager | 1 | Milan |
| Alpha Private Equity | asset_manager | 2 | |
| Charterhouse Capital Partners | asset_manager | 2 | |
| Partners Group | asset_manager | 1 | Zug |
| Intermediate Capital Group (ICG) | asset_manager | 1 | |
| Triton Partners | asset_manager | 2 | |
| Nordic Capital | asset_manager | 2 | |
| General Atlantic | asset_manager | 1 | |
| Silver Lake | asset_manager | 2 | |
| Thoma Bravo | asset_manager | 2 | |
| Oaktree Capital Management | asset_manager | 1 | |
| Ares Management | asset_manager | 1 | |
| Brookfield | asset_manager | 1 | |
| Antin Infrastructure Partners | asset_manager | 1 | Paris / London / Luxembourg |
| 3i Group | asset_manager | 1 | |
| Inflexion | asset_manager | 2 | |
| Livingbridge | asset_manager | 2 | |
| LDC | asset_manager | 2 | |
| ECI Partners | asset_manager | 2 | |
| Montagu | asset_manager | 2 | |
| Astorg | asset_manager | 1 | Luxembourg / Paris / London |
| Tikehau Capital | asset_manager | 1 | |
| Arcmont Asset Management | asset_manager | 2 | |
| Hayfin Capital Management | asset_manager | 2 | |
| Blue Owl | asset_manager | 2 | |
| HPS Investment Partners | asset_manager | 1 | |
| Sixth Street | asset_manager | 2 | |
| Golub Capital | asset_manager | 2 | |
| Fondo Italiano d'Investimento | asset_manager | 1 | Milan |
| Quadrivio Group | asset_manager | 2 | Milan |
| Wise Equity | asset_manager | 2 | Milan |
| NB Renaissance | asset_manager | 2 | Milan |
| F2i | asset_manager | 1 | Milan infrastructure |
| Mandarin Capital Partners | asset_manager | 2 | |
| Green Arrow Capital | asset_manager | 2 | |
| Xenon Private Equity | asset_manager | 2 | |
| Tamburi Investment Partners | asset_manager | 2 | |
| Apax Partners | asset_manager | 1 | |
| Coller Capital | asset_manager | 2 | |
| Pantheon | asset_manager | 2 | |
| HarbourVest | asset_manager | 2 | |
| LGT Capital Partners | asset_manager | 2 | Pfäffikon |
| Capital Dynamics | asset_manager | 2 | |
| Unigestion | asset_manager | 2 | Geneva |
| Hamilton Lane | asset_manager | 2 | |
| StepStone Group | asset_manager | 2 | |
| Vista Equity Partners | asset_manager | 2 | |
| Francisco Partners | asset_manager | 2 | |
| Searchlight Capital | asset_manager | 2 | |
| Stirling Square | asset_manager | 2 | |
| Exponent Private Equity | asset_manager | 2 | |
| Epiris | asset_manager | 2 | |
| Pollen Street | asset_manager | 2 | |
| AnaCap | asset_manager | 2 | |
| CDP Equity | asset_manager | 1 | Cassa Depositi e Prestiti group |

## Tier 3: corporate finance and treasury inside corporates

| Company | Group | Priority | Hint |
|---|---|---|---|
| Eni | corporate | 1 | Finance, treasury; Eni Trading & Shipping is in tier 5 |
| Leonardo | corporate | 1 | |
| Stellantis | corporate | 1 | |
| Ferrari | corporate | 2 | |
| Prada Group | corporate | 2 | |
| EssilorLuxottica | corporate | 2 | |
| Pirelli | corporate | 2 | |
| TIM (Telecom Italia) | corporate | 2 | |
| A2A | corporate | 1 | Energy trading desk in Milan |
| Snam | corporate | 2 | |
| Terna | corporate | 2 | |
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
