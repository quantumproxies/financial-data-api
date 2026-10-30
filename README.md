# Financial Data API

[![ci](https://github.com/quantumproxies/financial-data-api/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/financial-data-api/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Financial data from Python or the command line: stock quotes by ticker, crypto market data, DeFi total value locked per chain, ECB foreign-exchange rates, Legal Entity Identifier records and SEC EDGAR filings, as JSON or CSV. The code is free and open source (MIT). Most of these sources publish their own APIs; this package puts all six behind one client and one QuanticData sign-in, returns the same flat rows and CSV export for every source, retries on rate limits and dropped connections, and runs long jobs in the background.

```bash
pip install git+https://github.com/quantumproxies/financial-data-api
financial-data login
financial-data marketwatch AAPL MSFT -o quotes.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `financial-data marketwatch` | US tickers | Price, change, session, day and 52-week range, volume, market cap, P/E, EPS, 31 fields per row ([fields and price](https://quanticdata.io/collectors/marketwatch-api/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api)) | up to 25 |
| `financial-data crypto` | coin ids (optional) | Price, market cap, volume, 24h range and change, supply, all-time high, 28 fields per row ([fields and price](https://quanticdata.io/collectors/crypto-market-data-api/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api)) | up to 250 |
| `financial-data defi` | chain names (optional) | TVL in USD, rank, share of all chains, native token, chain id, 9 fields per row ([fields and price](https://quanticdata.io/collectors/defillama-api/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api)) | up to 200 |
| `financial-data fx` | base currency (optional) | Rate, inverse rate, reference date, one row per currency, 6 fields per row ([fields and price](https://quanticdata.io/collectors/exchange-rate-api/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api)) | up to 50 |
| `financial-data lei` | legal name or LEI | LEI, legal name, status, addresses, legal form, BIC, renewal date, 29 fields per row ([fields and price](https://quanticdata.io/collectors/lei-api/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api)) | up to 100 |
| `financial-data sec` | full-text query, or --ticker / --cik | Form, filed and report dates, company, ticker, accession, document links, 24 fields per row ([fields and price](https://quanticdata.io/collectors/sec-edgar-api/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api)) | up to 100 |

`sec` searches the full text of every filing (`QUERY`) or lists one company's filings (`--ticker` or `--cik`); `--forms 10-K,10-Q`, `--date-from` and `--date-to` narrow both. `fx` takes `--date` for a past day, and `crypto` takes `--vs-currency` (usd, eur, btc...), `--category` (stablecoins, meme-token...) and `--order` (market cap, volume or id).

## Sample output

A real row from `financial-data marketwatch AAPL MSFT --max-results 2` (2026-10-23):

```json
{
  "eps": 8.72,
  "url": "https://www.marketwatch.com/investing/stock/aapl",
  "beta": 1.17,
  "name": "Apple Inc.",
  "open": 344.94,
  "rank": 1,
  "price": 345.92,
  "change": -2.31,
  "ticker": "AAPL",
  "volume": 46898875,
  "day_low": 342.28,
  "session": "premarket",
  "currency": "USD",
  "day_high": 348.36,
  "dividend": 0.27,
  "exchange": "U.S.: Nasdaq",
  "pe_ratio": 39.92,
  "market_cap": 5080000000000,
  "quote_time": "Oct 23, 2026 4:49 a.m. EDT",
  "week52_low": 243.42,
  "week52_high": 348.36,
  "exchange_iso": "XNAS",
  "public_float": 14580000000,
  "instrument_id": "202934861",
  "avg_volume_65d": 44066082,
  "change_percent": -0.66,
  "previous_close": 348.22,
  "instrument_type": "Stock",
  "requested_ticker": "AAPL",
  "shares_outstanding": 14590000000,
  "dividend_yield_percent": 0.31
}
```

## Python

```python
from quanticdata_financial_data_api import Finance

finance = Finance()  # saved login, or QUANTICDATA_API_KEY

quotes = finance.marketwatch(["AAPL", "MSFT"])
for q in quotes:
    print(q["ticker"], q["price"], q["change_percent"], q["session"], q["quote_time"])

coins = finance.crypto(["bitcoin", "ethereum"], vs_currency="eur")
print([(c["symbol"], c["price"]) for c in coins])

rates = finance.fx("EUR", symbols=["USD", "GBP", "JPY"])
rates.to_csv("eur_rates.csv")

apple = finance.lei("Apple Inc", max_results=1)
print(apple.rows[0]["lei"], apple.rows[0]["registration_status"])

filings = finance.sec(ticker="AAPL", forms="10-K", max_results=5)
for f in filings:
    print(f["filed_date"], f["form"], f["url"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Watchlist snapshots**: Append the current price and change of a list of stocks and coins to one CSV, with a timestamp, every time it runs. See [`examples/watchlist_snapshot.py`](examples/watchlist_snapshot.py).
- **Filing monitor**: List the 10-K, 10-Q and 8-K filings a set of companies made since a date, with links to each document and its index. See [`examples/new_filings.py`](examples/new_filings.py).
- **Counterparty LEI lookup**: Read a list of legal names and add the LEI, entity and registration status, country and next renewal date of the best match to each. See [`examples/lei_lookup.py`](examples/lei_lookup.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `financial-data run <id> -o out.csv` collects it later.

### `financial-data marketwatch`

Latest quote per US ticker from MarketWatch: price, change, session, day and 52-week range, volume, market cap, P/E and EPS, with the time the quote is from.

```
financial-data marketwatch TICKERS [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `TICKERS` | string[] |  | US-listed ticker symbols as MarketWatch spells them, e.g. AAPL MSFT BRK.B. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `10` | How many quotes to deliver at most (1–25). You pay only for delivered quotes. |

### `financial-data crypto`

Crypto market rows from CoinGecko, for chosen coins or in market-cap order: price, market cap, volume, 24-hour range and change, supply and all-time high and low.

```
financial-data crypto [COIN_IDS] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `--vs-currency` | string | `usd` | Quote currency: usd, eur, btc... |
| `COIN_IDS` | string[] |  | CoinGecko coin ids, e.g. bitcoin ethereum solana. Omit them for the market-cap ranking. |
| `--category` | string |  | Only coins of this CoinGecko category, e.g. stablecoins or meme-token. |
| `--order` | market_cap_desc / market_cap_asc / volume_desc / volume_asc / id_asc / id_desc | `market_cap_desc` | Sort order (default market_cap_desc). |
| `--max-results` | integer | `50` | How many coins to deliver at most (1–250). You pay only for delivered coins. |

### `financial-data defi`

Total value locked per blockchain from DefiLlama, in USD, with its rank and share across all chains, the native token and the chain's CoinGecko and CoinMarketCap ids.

```
financial-data defi [CHAINS] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `CHAINS` | string[] |  | Chain names, e.g. Ethereum Solana Arbitrum. Omit them for every chain, ranked by TVL. |
| `--max-results` | integer | `50` | How many chains to deliver at most (1–200). You pay only for delivered chains. |

### `financial-data fx`

Foreign-exchange rates from the European Central Bank reference data, latest or for a past date, one row per target currency with the inverse rate.

```
financial-data fx [BASE] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `BASE` | string | `USD` | Base currency, 3 letters, e.g. EUR (default USD). |
| `--symbols` | string[] |  | Target currencies, e.g. USD GBP JPY. Omit them for every currency available. |
| `--date` | string |  | A past date, YYYY-MM-DD; omit it for the latest rates. |
| `--max-results` | integer | `40` | How many currencies to deliver at most (1–50). You pay only for delivered currencies. |

### `financial-data lei`

LEI records from GLEIF, by legal name or exact LEI: legal name and other names, entity and registration status, legal and headquarters addresses, legal form, register number, BIC codes and renewal date.

```
financial-data lei QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Legal name to search, e.g. "Apple Inc", or an exact 20-character LEI. |
| `--country` | string |  | Limit to entities whose legal address is in this country (ISO 3166-1 alpha-2). |
| `--max-results` | integer | `25` | How many entities to deliver at most (1–100). You pay only for delivered entities. |

### `financial-data sec`

SEC EDGAR filings: full-text search across every filing, or one company's filing history by ticker or CIK, with form, dates, accession number and links to the document and its index.

```
financial-data sec [QUERY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Full-text search across every filing, e.g. "artificial intelligence risk factors". Use this or --ticker / --cik. |
| `--ticker` | string |  | Company ticker, e.g. AAPL, for that company's filing history. |
| `--cik` | string |  | SEC Central Index Key, e.g. 320193, instead of a ticker. |
| `--forms` | string |  | Filter to a form type, e.g. 10-K, 8-K, S-1. Comma-separate several: 10-K,10-Q. |
| `--date-from` | string |  | Earliest filing date, YYYY-MM-DD. |
| `--date-to` | string |  | Latest filing date, YYYY-MM-DD. |
| `--max-results` | integer | `20` | How many filings to deliver at most (1–100). You pay only for delivered filings. |

## Output fields

<details><summary><code>financial-data marketwatch</code>: 31 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position in the delivered rows. |
| `ticker` | string | Ticker symbol as the quote page states it. |
| `requested_ticker` | string | The symbol you asked for — differs from `ticker` when MarketWatch resolved it to another listing. |
| `name` | string or null | Company name. |
| `exchange` | string or null | Listing exchange, e.g. "U.S.: Nasdaq". |
| `exchange_iso` | string or null | ISO 10383 MIC, e.g. XNAS. |
| `currency` | string or null | Price currency. |
| `instrument_type` | string or null | Instrument type as MarketWatch classifies it, e.g. Stock. |
| `instrument_id` | string or null | MarketWatch's instrument id; it stays the same when a ticker changes. |
| `price` | number or null | Latest printed price as of `quote_time`. In premarket or after hours this is the extended-hours print, not the last regular close; `session` says which. |
| `change` | number or null | Change against the previous close, in price terms. |
| `change_percent` | number or null | Change against the previous close, in percent (0.45 means +0.45%). |
| `session` | string or null | Which tape `price` came off: open, premarket, after_hours or closed. |
| `quote_time` | string or null | As-of time exactly as MarketWatch states it, with the exchange timezone, e.g. "Sep 2, 2026 8:20 a.m. EDT". |
| `previous_close` | number or null | Previous regular-session close, read from the close table MarketWatch renders alongside an extended-hours quote. Null when the page does not carry that table. |
| `open` | number or null | Regular-session open. In premarket or after hours this is the last completed session's open, the same session as `volume`, not the one `price` comes from. |
| `day_low` | number or null | Regular-session low, at the page's full precision. In extended hours it belongs to the last completed session, so it is not a bound on `price`. |
| `day_high` | number or null | Regular-session high, at the page's full precision. In extended hours it belongs to the last completed session, so it is not a bound on `price`. |
| `week52_low` | number or null | 52-week low, at the page's full precision. |
| `week52_high` | number or null | 52-week high, at the page's full precision. |
| `volume` | integer or null | Regular-session volume. Not the extended-hours tape MarketWatch shows as "Before/After Hours Volume". |
| `avg_volume_65d` | integer or null | 65-day average volume. |
| `market_cap` | number or null | Market capitalisation, suffix expanded ($4.75T becomes 4750000000000). |
| `pe_ratio` | number or null | Price/earnings ratio. Null when MarketWatch prints N/A, which it does for loss-making companies. |
| `eps` | number or null | Earnings per share. Negative for loss-making companies. |
| `shares_outstanding` | number or null | Shares outstanding, suffix expanded. |
| `public_float` | number or null | Public float, suffix expanded. |
| `beta` | number or null | Beta. |
| `dividend` | number or null | Dividend per share as most recently declared. |
| `dividend_yield_percent` | number or null | Dividend yield in percent (0.33 means 0.33%). |
| `url` | string | Quote page the row was read from. |

</details>

<details><summary><code>financial-data crypto</code>: 28 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Row order as returned. |
| `id` | string | CoinGecko coin id. |
| `symbol` | string | Ticker symbol (uppercase). |
| `name` | string or null | Coin name. |
| `price` | number or null | Current price in vs_currency. |
| `currency` | string | Quote currency (uppercase). |
| `market_cap` | number or null | Market capitalization. |
| `market_cap_rank` | integer or null | Global market-cap rank. |
| `volume_24h` | number or null | 24h trading volume. |
| `change_24h_pct` | number or null | 24h price change %. |
| `high_24h` | number or null | 24h high. |
| `low_24h` | number or null | 24h low. |
| `circulating_supply` | number or null | Circulating supply. |
| `total_supply` | number or null | Total supply. |
| `ath` | number or null | All-time high price. |
| `ath_date` | string or null | All-time high date. |
| `image` | string or null | Coin icon URL. |
| `last_updated` | string or null | Data timestamp. |
| `fully_diluted_valuation` | number or null | Fully diluted valuation in vs_currency. |
| `change_24h` | number or null | 24h price change in vs_currency. |
| `change_1h_pct` | number or null | 1h price change %. |
| `change_7d_pct` | number or null | 7d price change %. |
| `change_30d_pct` | number or null | 30d price change %. |
| `market_cap_change_24h_pct` | number or null | 24h market-cap change %. |
| `max_supply` | number or null | Maximum supply, when the coin has a cap. |
| `ath_change_pct` | number or null | Distance from the all-time high, %. |
| `atl` | number or null | All-time low price. |
| `atl_date` | string or null | All-time low date. |

</details>

<details><summary><code>financial-data defi</code>: 9 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | TVL rank. |
| `chain` | string | Blockchain name. |
| `tvl` | integer | Total value locked, USD. |
| `token_symbol` | string or null | Native token symbol. |
| `chain_id` | integer or null | EVM chain id when applicable. |
| `gecko_id` | string or null | CoinGecko id (join key). |
| `cmc_id` | string or null | CoinMarketCap id. |
| `tvl_rank` | integer | Rank by TVL across every chain, also on a filtered run. |
| `tvl_share_pct` | number or null | Share of the total TVL of all chains, %. |

</details>

<details><summary><code>financial-data fx</code>: 6 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `currency` | string | Target currency code. |
| `rate` | number | Rate from base to this currency. |
| `base` | string or null | Base currency. |
| `date` | string or null | Reference date. |
| `inverse_rate` | number or null | 1 unit of the target currency expressed in the base currency. |

</details>

<details><summary><code>financial-data lei</code>: 29 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `lei` | string | Legal Entity Identifier. |
| `legal_name` | string or null | Legal name. |
| `status` | string or null | Entity status (ACTIVE…). |
| `registration_status` | string or null | LEI registration status (ISSUED, LAPSED…). |
| `legal_country` | string or null | Legal address country. |
| `legal_city` | string or null | Legal address city. |
| `hq_country` | string or null | Headquarters country. |
| `legal_form` | string or null | Legal form code. |
| `initial_registration` | string or null | First LEI registration date. |
| `last_update` | string or null | Last update date. |
| `url` | string | GLEIF record URL. |
| `other_names` | string[] | Trading, previous and transliterated names. |
| `legal_region` | string or null | Region of the legal address (ISO 3166-2). |
| `legal_postal_code` | string or null | Postal code of the legal address. |
| `legal_address` | string or null | Legal address on one line. |
| `hq_city` | string or null | Headquarters city. |
| `hq_address` | string or null | Headquarters address on one line. |
| `jurisdiction` | string or null | Jurisdiction of formation. |
| `legal_form_other` | string or null | Legal form in words, when it has no ELF code. |
| `category` | string or null | Entity category (GENERAL, FUND, BRANCH…). |
| `registered_as` | string or null | National business-register number the LEI was validated against. |
| `registration_authority` | string or null | Register that issued registered_as (GLEIF RA code). |
| `entity_created` | string or null | Date the legal entity was formed. |
| `next_renewal` | string or null | Next LEI renewal date. |
| `managing_lou` | string or null | LEI of the issuing organisation. |
| `corroboration_level` | string or null | How far the record was corroborated against the register. |
| `bic` | string[] | BIC codes mapped to the entity. |
| `conformity_flag` | string or null | GLEIF conformity flag. |

</details>

<details><summary><code>financial-data sec</code>: 24 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `company` | string or null | Filer name. |
| `cik` | string or null | SEC CIK. |
| `form` | string or null | Form type (10-K, 8-K…). |
| `filed_date` | string or null | Filing date. |
| `report_date` | string or null | Period of report (company mode). |
| `file_type` | string or null | Document type (search mode). |
| `description` | string or null | Document description (search mode). |
| `accession` | string or null | Accession number. |
| `is_xbrl` | boolean or null | Whether the filing has XBRL data (company mode). |
| `url` | string or null | Direct link to the filing document. |
| `company_name` | string or null | Filer name without the ticker/CIK suffix. |
| `ticker` | string or null | Ticker, when the filer has one. |
| `items` | string[] | 8-K item numbers the filing reports (e.g. 2.02, 9.01). |
| `file_number` | string or null | SEC file number. |
| `accepted_at` | string or null | Acceptance timestamp (company mode). |
| `primary_doc_description` | string or null | Primary document description (company mode). |
| `is_inline_xbrl` | boolean or null | Whether the filing is Inline XBRL (company mode). |
| `size` | integer or null | Filing size in bytes (company mode). |
| `sic` | string or null | Standard Industrial Classification code. |
| `state` | string or null | State of the business address. |
| `location` | string or null | City and state code of the business address, as EDGAR states them (search mode); null when EDGAR holds a street line instead of a city. |
| `inc_state` | string or null | State or country of incorporation (search mode). |
| `index_url` | string or null | Filing index page listing every document and exhibit. |

</details>

## Sign-in and API keys

- `financial-data login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `financial-data login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `financial-data login --api-key`.
- `financial-data logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/marketwatch_quote/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"tickers": ["AAPL", "MSFT"], "max_results": 2}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this financial data API free?**

The code is free and MIT-licensed. Runs go through your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need an API key for each source?**

No. One QuanticData sign-in covers every command and the requests run on QuanticData's side. SEC EDGAR, GLEIF, CoinGecko and DefiLlama publish their own APIs, and the ECB its reference rates; what this package adds is one client for all of them, the same flat rows and CSV, JSON or JSONL export for every source, retries on rate limits and dropped connections, and background runs (`--no-wait`) you collect later with `financial-data run <run_id>`.

**How many rows can one run return?**

Up to 25 stock quotes, 250 coins, 200 chains, 50 exchange rates, 100 LEI records or 100 filings per run; ask for fewer with --max-results and you pay only for what is delivered.

**How current are the stock quotes?**

Each row carries quote_time, the as-of time MarketWatch states for the price, and session, which says whether the price comes from the open session, premarket, after hours or the close.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Lists such as BIC codes, other names and 8-K items are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/watchlist_snapshot.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Yahoo Finance Scraper](https://github.com/quantumproxies/yahoo-finance-scraper): Yahoo Finance scraper for Python and the command line.
- [Public Data API](https://github.com/quantumproxies/public-data-api): Public data API for Python and the command line.
- [Package Registry API](https://github.com/quantumproxies/package-registry-api): Package registry API for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=financial-data-api).
