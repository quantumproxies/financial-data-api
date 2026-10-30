"""Append a snapshot of a stock and crypto watchlist to a CSV.

    python watchlist_snapshot.py --tickers AAPL MSFT NVDA --coins bitcoin ethereum --out watchlist.csv

Each run adds one row per stock and per coin with a UTC timestamp, the price,
the change (against the previous close for stocks, over 24 hours for coins)
and the time the source gives for the price. Run it from cron to build a
price history:

    */30 * * * *  cd /path/to/here && python watchlist_snapshot.py --tickers AAPL MSFT --coins bitcoin

Needs a login (`financial-data login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_financial_data_api import Finance

FIELDS = ["checked_at", "kind", "symbol", "name", "price", "currency", "change_percent", "session", "as_of"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tickers", nargs="*", default=[], help="US stock tickers, e.g. AAPL MSFT")
    parser.add_argument("--coins", nargs="*", default=[], help="CoinGecko coin ids, e.g. bitcoin ethereum")
    parser.add_argument("--currency", default="usd", help="quote currency for the coins (usd, eur, btc...)")
    parser.add_argument("--out", default="watchlist.csv")
    args = parser.parse_args()
    if not args.tickers and not args.coins:
        parser.error("give --tickers, --coins or both")

    finance = Finance()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    # One quotes run takes up to 25 tickers, one crypto run up to 250 coins.
    for i in range(0, len(args.tickers), 25):
        batch = args.tickers[i:i + 25]
        for q in finance.marketwatch(batch, max_results=len(batch)):
            rows.append({"checked_at": checked_at, "kind": "stock", "symbol": q["ticker"], "name": q["name"],
                         "price": q["price"], "currency": q["currency"], "change_percent": q["change_percent"],
                         "session": q["session"], "as_of": q["quote_time"]})
    for i in range(0, len(args.coins), 250):
        batch = args.coins[i:i + 250]
        for c in finance.crypto(batch, vs_currency=args.currency, max_results=len(batch)):
            rows.append({"checked_at": checked_at, "kind": "crypto", "symbol": c["symbol"], "name": c["name"],
                         "price": c["price"], "currency": c["currency"], "change_percent": c["change_24h_pct"],
                         "session": None, "as_of": c["last_updated"]})

    new_file = not os.path.exists(args.out)
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} rows appended to {args.out}")


if __name__ == "__main__":
    main()
