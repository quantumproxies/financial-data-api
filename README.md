# SEC EDGAR filings API — examples

SEC filings — full-text search across all filings, or one company's filing history.

**Live page, full schema & pricing → [quanticdata.io/collectors/sec-edgar-api/](https://quanticdata.io/collectors/sec-edgar-api/)**

Reads the US SEC's EDGAR system. Search the full text of every filing (10-K, 8-K, S-1…) by keyword, or pass a ticker/CIK to get a company's recent filings with the document URL already built. Each row: company, CIK, form type, filing date, description and a direct link. EDGAR's official endpoints impose a per-second cap tied to a descriptive User-Agent and a CIK zero-padding ritual — handled for you.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/sec_filings/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence risk factors", "forms": "10-K", "max_results": 20}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `query` (string) — Full-text search across all filings. Use this OR ticker/cik.
- `ticker` (string) — Company ticker — resolved to its CIK. Use with company mode.
- `cik` (string) — SEC Central Index Key (numeric). Alternative to ticker.
- `forms` (string) — Filter to a form type, e.g. 10-K, 8-K, S-1.
- `max_results` (integer) — How many filings to deliver at most (1–100). You pay only for delivered filings.

## Output — one row per filing

| field | type | description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `company` | string | Filer name. |
| `cik` | string | SEC CIK. |
| `form` | string | Form type (10-K, 8-K…). |
| `filed_date` | string | Filing date. |
| `report_date` | string | Period of report (company mode). |
| `file_type` | string | Document type (search mode). |
| `description` | string | Document description (search mode). |
| `accession` | string | Accession number. |
| `is_xbrl` | boolean | Whether the filing has XBRL data (company mode). |
| `url` | string | Direct link to the filing document. |

## Pricing

**$0.0005 per delivered filing** ($0.5 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 4,000 filings — no card required.

## Links

- This collector: https://quanticdata.io/collectors/sec-edgar-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
