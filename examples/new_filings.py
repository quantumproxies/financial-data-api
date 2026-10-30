"""SEC filings a list of companies made since a date, in one CSV.

    python new_filings.py AAPL MSFT NVDA --forms 10-K,10-Q,8-K --since 2026-07-01

One row per filing with the ticker you asked for, the form, filing and report
dates, the 8-K items it reports and links to the document and its index page.
"""

import argparse
from datetime import date, timedelta

from quanticdata_financial_data_api import Finance, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tickers", nargs="+")
    parser.add_argument("--forms", default="10-K,10-Q,8-K", help="comma-separated form types")
    parser.add_argument("--since", default=(date.today() - timedelta(days=30)).isoformat(),
                        help="earliest filing date, YYYY-MM-DD (default: 30 days ago)")
    parser.add_argument("--per-company", type=int, default=50, help="filings per company (max 100)")
    parser.add_argument("--out", default="new_filings.csv")
    args = parser.parse_args()

    finance = Finance()
    rows = []
    for ticker in args.tickers:
        run = finance.sec(ticker=ticker, forms=args.forms, date_from=args.since, max_results=args.per_company)
        rows.extend({"requested_ticker": ticker, **filing} for filing in run)
        print(f"{ticker}: {len(run)} filings since {args.since}")

    write(rows, args.out)
    print(f"{len(rows)} filings written to {args.out}")


if __name__ == "__main__":
    main()
