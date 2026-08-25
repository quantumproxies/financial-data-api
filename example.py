"""Minimal SEC EDGAR filings API call — one typed row per filing.

Docs & schema: https://quanticdata.io/collectors/sec-edgar-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/sec_filings/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "query": "artificial intelligence risk factors",
        "forms": "10-K",
        "max_results": 20
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("company"), row.get("cik"), row.get("form"))
print(f"{len(data['results'])} filings, cost ${data['cost']}")
