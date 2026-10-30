"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class MarketwatchQuoteRow(TypedDict, total=False):
    """One row of `financial-data marketwatch` (marketwatch_quote v1.0.2)."""

    rank: int
    """1-based position in the delivered rows."""
    ticker: str
    """Ticker symbol as the quote page states it."""
    requested_ticker: str
    """The symbol you asked for — differs from `ticker` when MarketWatch resolved it to another listing."""
    name: Optional[str]
    """Company name."""
    exchange: Optional[str]
    """Listing exchange, e.g. "U.S.: Nasdaq"."""
    exchange_iso: Optional[str]
    """ISO 10383 MIC, e.g. XNAS."""
    currency: Optional[str]
    """Price currency."""
    instrument_type: Optional[str]
    """Instrument type as MarketWatch classifies it, e.g. Stock."""
    instrument_id: Optional[str]
    """MarketWatch's instrument id; it stays the same when a ticker changes."""
    price: Optional[float]
    """Latest printed price as of `quote_time`. In premarket or after hours this is the extended-hours print, not the last regular close; `session` says which."""
    change: Optional[float]
    """Change against the previous close, in price terms."""
    change_percent: Optional[float]
    """Change against the previous close, in percent (0.45 means +0.45%)."""
    session: Optional[str]
    """Which tape `price` came off: open, premarket, after_hours or closed."""
    quote_time: Optional[str]
    """As-of time exactly as MarketWatch states it, with the exchange timezone, e.g. "Sep 2, 2026 8:20 a.m. EDT"."""
    previous_close: Optional[float]
    """Previous regular-session close, read from the close table MarketWatch renders alongside an extended-hours quote. Null when the page does not carry that table."""
    open: Optional[float]
    """Regular-session open. In premarket or after hours this is the last completed session's open, the same session as `volume`, not the one `price` comes from."""
    day_low: Optional[float]
    """Regular-session low, at the page's full precision. In extended hours it belongs to the last completed session, so it is not a bound on `price`."""
    day_high: Optional[float]
    """Regular-session high, at the page's full precision. In extended hours it belongs to the last completed session, so it is not a bound on `price`."""
    week52_low: Optional[float]
    """52-week low, at the page's full precision."""
    week52_high: Optional[float]
    """52-week high, at the page's full precision."""
    volume: Optional[int]
    """Regular-session volume. Not the extended-hours tape MarketWatch shows as "Before/After Hours Volume"."""
    avg_volume_65d: Optional[int]
    """65-day average volume."""
    market_cap: Optional[float]
    """Market capitalisation, suffix expanded ($4.75T becomes 4750000000000)."""
    pe_ratio: Optional[float]
    """Price/earnings ratio. Null when MarketWatch prints N/A, which it does for loss-making companies."""
    eps: Optional[float]
    """Earnings per share. Negative for loss-making companies."""
    shares_outstanding: Optional[float]
    """Shares outstanding, suffix expanded."""
    public_float: Optional[float]
    """Public float, suffix expanded."""
    beta: Optional[float]
    """Beta."""
    dividend: Optional[float]
    """Dividend per share as most recently declared."""
    dividend_yield_percent: Optional[float]
    """Dividend yield in percent (0.33 means 0.33%)."""
    url: str
    """Quote page the row was read from."""

class CoingeckoCoinsRow(TypedDict, total=False):
    """One row of `financial-data crypto` (coingecko_coins v1.1.0)."""

    rank: int
    """Row order as returned."""
    id: str
    """CoinGecko coin id."""
    symbol: str
    """Ticker symbol (uppercase)."""
    name: Optional[str]
    """Coin name."""
    price: Optional[float]
    """Current price in vs_currency."""
    currency: str
    """Quote currency (uppercase)."""
    market_cap: Optional[float]
    """Market capitalization."""
    market_cap_rank: Optional[int]
    """Global market-cap rank."""
    volume_24h: Optional[float]
    """24h trading volume."""
    change_24h_pct: Optional[float]
    """24h price change %."""
    high_24h: Optional[float]
    """24h high."""
    low_24h: Optional[float]
    """24h low."""
    circulating_supply: Optional[float]
    """Circulating supply."""
    total_supply: Optional[float]
    """Total supply."""
    ath: Optional[float]
    """All-time high price."""
    ath_date: Optional[str]
    """All-time high date."""
    image: Optional[str]
    """Coin icon URL."""
    last_updated: Optional[str]
    """Data timestamp."""
    fully_diluted_valuation: Optional[float]
    """Fully diluted valuation in vs_currency."""
    change_24h: Optional[float]
    """24h price change in vs_currency."""
    change_1h_pct: Optional[float]
    """1h price change %."""
    change_7d_pct: Optional[float]
    """7d price change %."""
    change_30d_pct: Optional[float]
    """30d price change %."""
    market_cap_change_24h_pct: Optional[float]
    """24h market-cap change %."""
    max_supply: Optional[float]
    """Maximum supply, when the coin has a cap."""
    ath_change_pct: Optional[float]
    """Distance from the all-time high, %."""
    atl: Optional[float]
    """All-time low price."""
    atl_date: Optional[str]
    """All-time low date."""

class DefillamaRow(TypedDict, total=False):
    """One row of `financial-data defi` (defillama v1.1.0)."""

    rank: int
    """TVL rank."""
    chain: str
    """Blockchain name."""
    tvl: int
    """Total value locked, USD."""
    token_symbol: Optional[str]
    """Native token symbol."""
    chain_id: Optional[int]
    """EVM chain id when applicable."""
    gecko_id: Optional[str]
    """CoinGecko id (join key)."""
    cmc_id: Optional[str]
    """CoinMarketCap id."""
    tvl_rank: int
    """Rank by TVL across every chain, also on a filtered run."""
    tvl_share_pct: Optional[float]
    """Share of the total TVL of all chains, %."""

class ExchangeRatesRow(TypedDict, total=False):
    """One row of `financial-data fx` (exchange_rates v1.1.0)."""

    rank: int
    """1-based position."""
    currency: str
    """Target currency code."""
    rate: float
    """Rate from base to this currency."""
    base: Optional[str]
    """Base currency."""
    date: Optional[str]
    """Reference date."""
    inverse_rate: Optional[float]
    """1 unit of the target currency expressed in the base currency."""

class GleifLeiRow(TypedDict, total=False):
    """One row of `financial-data lei` (gleif_lei v1.1.0)."""

    rank: int
    """1-based position."""
    lei: str
    """Legal Entity Identifier."""
    legal_name: Optional[str]
    """Legal name."""
    status: Optional[str]
    """Entity status (ACTIVE…)."""
    registration_status: Optional[str]
    """LEI registration status (ISSUED, LAPSED…)."""
    legal_country: Optional[str]
    """Legal address country."""
    legal_city: Optional[str]
    """Legal address city."""
    hq_country: Optional[str]
    """Headquarters country."""
    legal_form: Optional[str]
    """Legal form code."""
    initial_registration: Optional[str]
    """First LEI registration date."""
    last_update: Optional[str]
    """Last update date."""
    url: str
    """GLEIF record URL."""
    other_names: List[str]
    """Trading, previous and transliterated names."""
    legal_region: Optional[str]
    """Region of the legal address (ISO 3166-2)."""
    legal_postal_code: Optional[str]
    """Postal code of the legal address."""
    legal_address: Optional[str]
    """Legal address on one line."""
    hq_city: Optional[str]
    """Headquarters city."""
    hq_address: Optional[str]
    """Headquarters address on one line."""
    jurisdiction: Optional[str]
    """Jurisdiction of formation."""
    legal_form_other: Optional[str]
    """Legal form in words, when it has no ELF code."""
    category: Optional[str]
    """Entity category (GENERAL, FUND, BRANCH…)."""
    registered_as: Optional[str]
    """National business-register number the LEI was validated against."""
    registration_authority: Optional[str]
    """Register that issued registered_as (GLEIF RA code)."""
    entity_created: Optional[str]
    """Date the legal entity was formed."""
    next_renewal: Optional[str]
    """Next LEI renewal date."""
    managing_lou: Optional[str]
    """LEI of the issuing organisation."""
    corroboration_level: Optional[str]
    """How far the record was corroborated against the register."""
    bic: List[str]
    """BIC codes mapped to the entity."""
    conformity_flag: Optional[str]
    """GLEIF conformity flag."""

class SecFilingsRow(TypedDict, total=False):
    """One row of `financial-data sec` (sec_filings v1.1.1)."""

    rank: int
    """1-based position."""
    company: Optional[str]
    """Filer name."""
    cik: Optional[str]
    """SEC CIK."""
    form: Optional[str]
    """Form type (10-K, 8-K…)."""
    filed_date: Optional[str]
    """Filing date."""
    report_date: Optional[str]
    """Period of report (company mode)."""
    file_type: Optional[str]
    """Document type (search mode)."""
    description: Optional[str]
    """Document description (search mode)."""
    accession: Optional[str]
    """Accession number."""
    is_xbrl: Optional[bool]
    """Whether the filing has XBRL data (company mode)."""
    url: Optional[str]
    """Direct link to the filing document."""
    company_name: Optional[str]
    """Filer name without the ticker/CIK suffix."""
    ticker: Optional[str]
    """Ticker, when the filer has one."""
    items: List[str]
    """8-K item numbers the filing reports (e.g. 2.02, 9.01)."""
    file_number: Optional[str]
    """SEC file number."""
    accepted_at: Optional[str]
    """Acceptance timestamp (company mode)."""
    primary_doc_description: Optional[str]
    """Primary document description (company mode)."""
    is_inline_xbrl: Optional[bool]
    """Whether the filing is Inline XBRL (company mode)."""
    size: Optional[int]
    """Filing size in bytes (company mode)."""
    sic: Optional[str]
    """Standard Industrial Classification code."""
    state: Optional[str]
    """State of the business address."""
    location: Optional[str]
    """City and state code of the business address, as EDGAR states them (search mode); null when EDGAR holds a street line instead of a city."""
    inc_state: Optional[str]
    """State or country of incorporation (search mode)."""
    index_url: Optional[str]
    """Filing index page listing every document and exhibit."""
