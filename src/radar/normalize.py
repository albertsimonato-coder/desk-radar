"""Title / location / employment-type normalisation and the dedup key."""

from __future__ import annotations

import hashlib
import re

# ---------------------------------------------------------------------------
# City aliases. Keys are lowercase fragments matched as whole tokens inside the
# raw location string; values are (canonical city, ISO-2 country).
# ---------------------------------------------------------------------------
CITY_ALIASES: dict[str, tuple[str, str]] = {
    # United Kingdom
    "london": ("London", "GB"),
    "londra": ("London", "GB"),
    "londres": ("London", "GB"),
    "canary wharf": ("London", "GB"),
    "greater london": ("London", "GB"),
    "edinburgh": ("Edinburgh", "GB"),
    "glasgow": ("Glasgow", "GB"),
    "birmingham": ("Birmingham", "GB"),
    "manchester": ("Manchester", "GB"),
    "belfast": ("Belfast", "GB"),
    "bournemouth": ("Bournemouth", "GB"),
    "chester": ("Chester", "GB"),
    "knutsford": ("Knutsford", "GB"),
    "northampton": ("Northampton", "GB"),
    "porto": ("Porto", "PT"),
    # Italy
    "milan": ("Milan", "IT"),
    "milano": ("Milan", "IT"),
    "mailand": ("Milan", "IT"),
    "rome": ("Rome", "IT"),
    "roma": ("Rome", "IT"),
    "turin": ("Turin", "IT"),
    "torino": ("Turin", "IT"),
    # Luxembourg
    "luxembourg": ("Luxembourg", "LU"),
    "luxemburg": ("Luxembourg", "LU"),
    "lussemburgo": ("Luxembourg", "LU"),
    "kirchberg": ("Luxembourg", "LU"),
    "esch-sur-alzette": ("Luxembourg", "LU"),
    # Switzerland
    "zurich": ("Zurich", "CH"),
    "zürich": ("Zurich", "CH"),
    "zuerich": ("Zurich", "CH"),
    "zurigo": ("Zurich", "CH"),
    "opfikon": ("Zurich", "CH"),
    "geneva": ("Geneva", "CH"),
    "genève": ("Geneva", "CH"),
    "geneve": ("Geneva", "CH"),
    "genf": ("Geneva", "CH"),
    "ginevra": ("Geneva", "CH"),
    "lugano": ("Lugano", "CH"),
    "basel": ("Basel", "CH"),
    "bern": ("Bern", "CH"),
    "baar": ("Zug", "CH"),
    "zug": ("Zug", "CH"),
    "lausanne": ("Lausanne", "CH"),
    # France
    "paris": ("Paris", "FR"),
    "parigi": ("Paris", "FR"),
    "la défense": ("Paris", "FR"),
    "la defense": ("Paris", "FR"),
    "puteaux": ("Paris", "FR"),
    "courbevoie": ("Paris", "FR"),
    "montrouge": ("Paris", "FR"),
    "nanterre": ("Paris", "FR"),
    "levallois-perret": ("Paris", "FR"),
    "issy-les-moulineaux": ("Paris", "FR"),
    "ile-de-france": ("Paris", "FR"),
    "île-de-france": ("Paris", "FR"),
    # Ireland
    "dublin": ("Dublin", "IE"),
    "dublino": ("Dublin", "IE"),
    # Other European
    "frankfurt": ("Frankfurt", "DE"),
    "frankfurt am main": ("Frankfurt", "DE"),
    "eschborn": ("Frankfurt", "DE"),
    "francoforte": ("Frankfurt", "DE"),
    "berlin": ("Berlin", "DE"),
    "munich": ("Munich", "DE"),
    "münchen": ("Munich", "DE"),
    "amsterdam": ("Amsterdam", "NL"),
    "rotterdam": ("Rotterdam", "NL"),
    "brussels": ("Brussels", "BE"),
    "bruxelles": ("Brussels", "BE"),
    "madrid": ("Madrid", "ES"),
    "lisbon": ("Lisbon", "PT"),
    "lisboa": ("Lisbon", "PT"),
    "vienna": ("Vienna", "AT"),
    "wien": ("Vienna", "AT"),
    "copenhagen": ("Copenhagen", "DK"),
    "stockholm": ("Stockholm", "SE"),
    "oslo": ("Oslo", "NO"),
    "warsaw": ("Warsaw", "PL"),
    "warszawa": ("Warsaw", "PL"),
    "krakow": ("Krakow", "PL"),
    "kraków": ("Krakow", "PL"),
    "wroclaw": ("Wroclaw", "PL"),
    "wrocław": ("Wroclaw", "PL"),
    "budapest": ("Budapest", "HU"),
    "prague": ("Prague", "CZ"),
    "praha": ("Prague", "CZ"),
    "bucharest": ("Bucharest", "RO"),
    "athens": ("Athens", "GR"),
    "sofia": ("Sofia", "BG"),
    "monaco": ("Monaco", "MC"),
    # Americas
    "new york": ("New York", "US"),
    "nyc": ("New York", "US"),
    "chicago": ("Chicago", "US"),
    "houston": ("Houston", "US"),
    "boston": ("Boston", "US"),
    "san francisco": ("San Francisco", "US"),
    "los angeles": ("Los Angeles", "US"),
    "miami": ("Miami", "US"),
    "stamford": ("Stamford", "US"),
    "greenwich": ("Greenwich", "US"),
    "jersey city": ("Jersey City", "US"),
    "atlanta": ("Atlanta", "US"),
    "dallas": ("Dallas", "US"),
    "charlotte": ("Charlotte", "US"),
    "toronto": ("Toronto", "CA"),
    "calgary": ("Calgary", "CA"),
    "montreal": ("Montreal", "CA"),
    "sao paulo": ("Sao Paulo", "BR"),
    "são paulo": ("Sao Paulo", "BR"),
    "mexico city": ("Mexico City", "MX"),
    "buenos aires": ("Buenos Aires", "AR"),
    # APAC / Middle East
    "singapore": ("Singapore", "SG"),
    "hong kong": ("Hong Kong", "HK"),
    "tokyo": ("Tokyo", "JP"),
    "shanghai": ("Shanghai", "CN"),
    "beijing": ("Beijing", "CN"),
    "sydney": ("Sydney", "AU"),
    "melbourne": ("Melbourne", "AU"),
    "mumbai": ("Mumbai", "IN"),
    "bengaluru": ("Bengaluru", "IN"),
    "bangalore": ("Bengaluru", "IN"),
    "hyderabad": ("Hyderabad", "IN"),
    "pune": ("Pune", "IN"),
    "chennai": ("Chennai", "IN"),
    "gurugram": ("Gurugram", "IN"),
    "gurgaon": ("Gurugram", "IN"),
    "dubai": ("Dubai", "AE"),
    "abu dhabi": ("Abu Dhabi", "AE"),
    "doha": ("Doha", "QA"),
    "riyadh": ("Riyadh", "SA"),
    "seoul": ("Seoul", "KR"),
    "taipei": ("Taipei", "TW"),
    "kuala lumpur": ("Kuala Lumpur", "MY"),
    "manila": ("Manila", "PH"),
    "johannesburg": ("Johannesburg", "ZA"),
    "cape town": ("Cape Town", "ZA"),
}

COUNTRY_ALIASES: dict[str, str] = {
    "united kingdom": "GB",
    "uk": "GB",
    "gb": "GB",
    "great britain": "GB",
    "england": "GB",
    "scotland": "GB",
    "regno unito": "GB",
    "italy": "IT",
    "italia": "IT",
    "it": "IT",
    "luxembourg": "LU",
    "lu": "LU",
    "switzerland": "CH",
    "schweiz": "CH",
    "suisse": "CH",
    "svizzera": "CH",
    "ch": "CH",
    "france": "FR",
    "fr": "FR",
    "francia": "FR",
    "ireland": "IE",
    "ie": "IE",
    "irlanda": "IE",
    "germany": "DE",
    "deutschland": "DE",
    "de": "DE",
    "netherlands": "NL",
    "the netherlands": "NL",
    "nl": "NL",
    "belgium": "BE",
    "be": "BE",
    "spain": "ES",
    "es": "ES",
    "portugal": "PT",
    "austria": "AT",
    "denmark": "DK",
    "sweden": "SE",
    "norway": "NO",
    "poland": "PL",
    "hungary": "HU",
    "czech republic": "CZ",
    "czechia": "CZ",
    "romania": "RO",
    "greece": "GR",
    "united states": "US",
    "united states of america": "US",
    "usa": "US",
    "us": "US",
    "canada": "CA",
    "brazil": "BR",
    "mexico": "MX",
    "argentina": "AR",
    "singapore": "SG",
    "hong kong": "HK",
    "hong kong sar": "HK",
    "japan": "JP",
    "china": "CN",
    "australia": "AU",
    "india": "IN",
    "united arab emirates": "AE",
    "uae": "AE",
    "qatar": "QA",
    "saudi arabia": "SA",
    "south korea": "KR",
    "korea": "KR",
    "taiwan": "TW",
    "malaysia": "MY",
    "philippines": "PH",
    "south africa": "ZA",
}

# Longest aliases first so "frankfurt am main" wins over "frankfurt", "new york" over "york".
_CITY_KEYS = sorted(CITY_ALIASES, key=len, reverse=True)
_CITY_RE = re.compile(r"(?<![a-z])(" + "|".join(re.escape(k) for k in _CITY_KEYS) + r")(?![a-z])")
_COUNTRY_KEYS = sorted(COUNTRY_ALIASES, key=len, reverse=True)
_COUNTRY_RE = re.compile(
    r"(?<![a-z])(" + "|".join(re.escape(k) for k in _COUNTRY_KEYS) + r")(?![a-z])"
)

_REMOTE_RE = re.compile(r"\b(remote|work from home|wfh|anywhere)\b", re.I)


def normalize_location(location_raw: str) -> tuple[str, str]:
    """Return (city, country ISO-2). Unknown -> ("", "") or ("", country) or ("Remote", "")."""
    if not location_raw:
        return "", ""
    text = location_raw.lower().replace("_", " ")
    text = re.sub(r"\s+", " ", text).strip()
    city, country = "", ""
    m = _CITY_RE.search(text)
    if m:
        city, country = CITY_ALIASES[m.group(1)]
    # Country: explicit mention wins only when it does not contradict the city.
    cm = _COUNTRY_RE.search(text)
    if cm:
        c = COUNTRY_ALIASES[cm.group(1)]
        # Two-letter aliases are noisy ("IT", "US" as words); accept them only when upper-case
        # in the raw string or clearly delimited by punctuation.
        if len(cm.group(1)) == 2:
            raw_tokens = re.findall(r"[A-Za-z]+", location_raw)
            if cm.group(1).upper() not in raw_tokens:
                c = ""
        if c and not country:
            country = c
    if not city and _REMOTE_RE.search(text):
        city = "Remote"
    return city, country


# ---------------------------------------------------------------------------
# Titles
# ---------------------------------------------------------------------------
_TITLE_JUNK = [
    re.compile(
        r"\((?:m/f/d|m/w/d|f/m/d|f/h|h/f|m/f|w/m|m/w/x|f/m/x|m/f/x|x/f/m|all genders)\)", re.I
    ),
    re.compile(r"\b(?:m/f/d|m/w/d|f/m/d|f/h|h/f|m/w/x|x/f/m)\b", re.I),
    re.compile(r"\[[^\]]*\]"),  # [anything]
    re.compile(r"\([^)]*\b(?:req|requisition|id|ref|job)\b[^)]*\)", re.I),
    re.compile(r"\b(?:req|requisition|job)\s*(?:id|no\.?|#)?\s*[:#-]?\s*[A-Z0-9-]{4,}\b", re.I),
    re.compile(r"\b[A-Z]{1,4}-?\d{4,}\b"),  # JR123456, R-0012345
    re.compile(r"\b\d{5,}\b"),  # bare numeric ids
    re.compile(r"\b(?:19|20)\d{2}(?:\s*[-/]\s*(?:19|20)?\d{2})?\b"),  # years / ranges
    re.compile(r"[–—\-–—]\s*$"),
]
_WS = re.compile(r"\s+")


def normalize_title(title: str) -> str:
    t = title or ""
    t = t.replace(" ", " ")
    for rx in _TITLE_JUNK:
        t = rx.sub(" ", t)
    t = t.lower()
    t = re.sub(r"[^\w\s/&+.,-]", " ", t)
    t = re.sub(r"\s*[-–—:|,/]+\s*$", "", t)
    t = _WS.sub(" ", t).strip(" -–—:|,")
    return t


def dedup_key(company_slug: str, title_norm: str, city: str) -> str:
    raw = f"{company_slug}|{title_norm}|{city.lower()}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()
