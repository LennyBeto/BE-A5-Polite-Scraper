# The Polite Scraper

A small, polite scraping pipeline: downloads the first 3 catalogue pages of [Books to Scrape](https://books.toscrape.com), visits all 60 book detail pages, and turns the HTML into clean, schema-validated JSON — surviving a broken page without crashing, and reporting what happened at the end of every run.


## Target classification

- **Site:** books.toscrape.com
- **Why this site is appropriate to scrape:** it is an explicitly-built practice sandbox (see [toscrape.com](https://toscrape.com)) — its stated purpose is to give people a safe target to practice scraping on. This is not a real bookstore; no real business or user is affected.
- **Scope:** the first 3 catalogue pages only, and the 60 book detail pages linked from them. Nothing beyond that scope is fetched.
- **Data collected:** for each book — title, product URL, price, availability, star rating, description, source page, and fetch timestamp. All fields are already present in the server-rendered HTML; nothing is inferred or fabricated.
- **`robots.txt` result:** <!-- fill in with your actual curl result: either the file's content, or "no robots file found" -->
- **Why this is appropriate here:** the target is a purpose-built sandbox for this exact activity, the scope is narrow and fixed (not an unbounded crawl), and every request identifies itself honestly with a user-agent naming this project.

I will not reuse this code on another site without checking its rules and terms first.

## How to run it

```bash
pip install -r requirements.txt
cd src
python main.py
```

Produces `output/books.json`, `output/errors.json`, and `output/run-report.json`.

## Lane

Python 3.10+, using `requests` (HTTP), `beautifulsoup4` (HTML parsing), and `pydantic` (schema validation).

## Record schema

| Field | Type | Notes |
|---|---|---|
| `title` | string | |
| `product_url` | string | canonical identity — the URL used for de-duplication |
| `price_text` | string | raw text, e.g. `"£51.77"` |
| `price_gbp` | float | parsed numeric value |
| `availability_text` | string | raw text |
| `rating_text` | string \| null | e.g. `"Three"` |
| `rating_value` | int \| null | 1–5, parsed from `rating_text` |
| `description` | string \| null | `null` when genuinely absent — never invented |
| `source_page` | string | the catalogue page this book was discovered on |
| `fetched_at` | string | ISO 8601 UTC timestamp |

## Politeness rules followed

- **User-agent:** every request identifies itself as `FlyRankInternshipA9/1.0` with a link back to this repo.
- **Timeout:** every request gives up after 10 seconds rather than hanging indefinitely.
- **Delay:** at least 500ms between real (non-cached) requests to the site.
- **Status check:** only a `200` response is treated as a successful page; anything else is a failed fetch, not HTML to parse.
- **Cache:** every fetched page is saved to `cache/` and read from there on subsequent runs — the site is asked for each page only once during development.
- **Retry policy:** a timeout or `5xx` server error is retried once; a `404` or `403` is never retried.

## Sample run report

```json
<!-- paste your actual output/run-report.json contents here -->
```

## Why this assignment needed no browser

Books to Scrape renders its data directly into the HTML the server sends — the price, title, and description are all present in the raw response, with no JavaScript required to populate them. A headless browser would only add startup cost and memory overhead for data that's already there in the first response.

## Ethics note

I use this scraper only against a site explicitly built for scraping practice. On any other site, I would check for an official API first, never attempt to bypass a login, paywall, or block, and collect only the specific data needed for the task — not an unbounded crawl.
