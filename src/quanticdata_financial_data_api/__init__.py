"""Financial Data API: Financial data API for Python and the command line: stock quotes, crypto prices, DeFi TVL, ECB exchange rates, LEI records and SEC EDGAR filings in one client, with one sign-in and the same JSON or CSV rows for every source. Free and open source; runs on your QuanticData account.

    from quanticdata_financial_data_api import Finance

    scraper = Finance()   # saved login (`financial-data login`) or QUANTICDATA_API_KEY
    run = scraper.marketwatch(...)   # stock quotes from MarketWatch by ticker
    run = scraper.crypto(...)   # crypto market data from CoinGecko, by coin id or ranking
    run = scraper.defi(...)   # DeFi total value locked per chain from DefiLlama
    run = scraper.fx(...)   # foreign-exchange rates from ECB reference data
    run = scraper.lei(...)   # Legal Entity Identifier records from GLEIF
    run = scraper.sec(...)   # SEC EDGAR filings by full-text search or company
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["Finance", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class Finance:
    """Financial Data API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="financial-data/0.1.0 (+https://github.com/quantumproxies/financial-data-api)", timeout=timeout)

    def marketwatch(
        self, tickers: Union[str, Sequence[str]],
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Latest quote per US ticker from MarketWatch: price, change, session, day and 52-week range, volume, market cap, P/E and EPS, with the time the quote is from.

        Args:
            tickers: US-listed ticker symbols as MarketWatch spells them, e.g. AAPL MSFT BRK.B.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many quotes to deliver at most (1–25). You pay only for delivered quotes.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 25 rows, one per quote: see ``types.MarketwatchQuoteRow``.
        """
        payload = {
            "tickers": _as_list(tickers),
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("marketwatch_quote", payload, wait=wait, timeout=timeout)

    def crypto(
        self, coin_ids: Optional[Union[str, Sequence[str]]] = None,
        *,
        vs_currency: Optional[str] = None,
        category: Optional[str] = None,
        order: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Crypto market rows from CoinGecko, for chosen coins or in market-cap order: price, market cap, volume, 24-hour range and change, supply and all-time high and low.

        Args:
            coin_ids: CoinGecko coin ids, e.g. bitcoin ethereum solana. Omit them for the market-cap ranking.
            vs_currency: Quote currency: usd, eur, btc...
            category: Only coins of this CoinGecko category, e.g. stablecoins or meme-token.
            order: Sort order (default market_cap_desc). One of: market_cap_desc, market_cap_asc, volume_desc, volume_asc, id_asc, id_desc.
            max_results: How many coins to deliver at most (1–250). You pay only for delivered coins.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 250 rows, one per coin: see ``types.CoingeckoCoinsRow``.
        """
        payload = {
            "coin_ids": _as_list(coin_ids),
            "vs_currency": vs_currency,
            "category": category,
            "order": order,
            "max_results": max_results,
        }
        return self.client.run_collector("coingecko_coins", payload, wait=wait, timeout=timeout)

    def defi(
        self, chains: Optional[Union[str, Sequence[str]]] = None,
        *,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Total value locked per blockchain from DefiLlama, in USD, with its rank and share across all chains, the native token and the chain's CoinGecko and CoinMarketCap ids.

        Args:
            chains: Chain names, e.g. Ethereum Solana Arbitrum. Omit them for every chain, ranked by TVL.
            max_results: How many chains to deliver at most (1–200). You pay only for delivered chains.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 200 rows, one per chain: see ``types.DefillamaRow``.
        """
        payload = {
            "chains": _as_list(chains),
            "max_results": max_results,
        }
        return self.client.run_collector("defillama", payload, wait=wait, timeout=timeout)

    def fx(
        self, base: Optional[str] = None,
        *,
        symbols: Optional[Union[str, Sequence[str]]] = None,
        date: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Foreign-exchange rates from the European Central Bank reference data, latest or for a past date, one row per target currency with the inverse rate.

        Args:
            base: Base currency, 3 letters, e.g. EUR (default USD).
            symbols: Target currencies, e.g. USD GBP JPY. Omit them for every currency available.
            date: A past date, YYYY-MM-DD; omit it for the latest rates.
            max_results: How many currencies to deliver at most (1–50). You pay only for delivered currencies.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per rate: see ``types.ExchangeRatesRow``.
        """
        payload = {
            "base": base,
            "symbols": _as_list(symbols),
            "date": date,
            "max_results": max_results,
        }
        return self.client.run_collector("exchange_rates", payload, wait=wait, timeout=timeout)

    def lei(
        self, query: str,
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """LEI records from GLEIF, by legal name or exact LEI: legal name and other names, entity and registration status, legal and headquarters addresses, legal form, register number, BIC codes and renewal date.

        Args:
            query: Legal name to search, e.g. "Apple Inc", or an exact 20-character LEI.
            country: Limit to entities whose legal address is in this country (ISO 3166-1 alpha-2).
            max_results: How many entities to deliver at most (1–100). You pay only for delivered entities.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per entity: see ``types.GleifLeiRow``.
        """
        payload = {
            "query": query,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("gleif_lei", payload, wait=wait, timeout=timeout)

    def sec(
        self, query: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        forms: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """SEC EDGAR filings: full-text search across every filing, or one company's filing history by ticker or CIK, with form, dates, accession number and links to the document and its index.

        Args:
            query: Full-text search across every filing, e.g. "artificial intelligence risk factors". Use this or --ticker / --cik.
            ticker: Company ticker, e.g. AAPL, for that company's filing history.
            cik: SEC Central Index Key, e.g. 320193, instead of a ticker.
            forms: Filter to a form type, e.g. 10-K, 8-K, S-1. Comma-separate several: 10-K,10-Q.
            date_from: Earliest filing date, YYYY-MM-DD.
            date_to: Latest filing date, YYYY-MM-DD.
            max_results: How many filings to deliver at most (1–100). You pay only for delivered filings.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per filing: see ``types.SecFilingsRow``.
        """
        payload = {
            "query": query,
            "ticker": ticker,
            "cik": cik,
            "forms": forms,
            "date_from": date_from,
            "date_to": date_to,
            "max_results": max_results,
        }
        return self.client.run_collector("sec_filings", payload, wait=wait, timeout=timeout)
