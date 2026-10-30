"""Add the Legal Entity Identifier of each name in a list, from GLEIF.

    python lei_lookup.py names.txt --country US --out lei.csv

names.txt holds one legal name per line. Each output row keeps the name you
gave next to GLEIF's best match: LEI, legal name, entity and registration
status, legal country, headquarters city and next renewal date. A name with no
match keeps its row with empty fields, so the output lines up with the input.
"""

import argparse

from quanticdata_financial_data_api import Finance, write

FIELDS = ["lei", "legal_name", "status", "registration_status", "legal_country", "hq_city", "next_renewal"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", help="file with one legal name per line")
    parser.add_argument("--country", help="only entities with a legal address in this country (ISO code, e.g. US)")
    parser.add_argument("--out", default="lei.csv")
    args = parser.parse_args()

    with open(args.names, encoding="utf-8") as fh:
        names = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    finance = Finance()
    rows = []
    for name in names:
        run = finance.lei(name, country=args.country, max_results=1)
        best = run.rows[0] if run.rows else {}
        rows.append({"input_name": name, **{field: best.get(field) for field in FIELDS}})
        print(f"{name}: {best.get('lei') or 'no match'}")

    write(rows, args.out)
    print(f"{len(rows)} rows written to {args.out}")


if __name__ == "__main__":
    main()
