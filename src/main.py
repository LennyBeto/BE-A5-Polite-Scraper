import json
from datetime import datetime, timezone
from discover import discover_book_urls
from extract import extract_book
from fetch import fetch
from store import validate_and_store
from report import write_report
from fetch import get_and_reset_counts

def main():
    html = fetch("https://books.toscrape.com/catalogue/page-1.html")
    print(f"Fetched {len(html)} characters")

if __name__ == "__main__":
    main()

def main():
    pairs = discover_book_urls()
    print(f"First: {pairs[0] if pairs else 'none found'}")

if __name__ == "__main__":
    main()

def main():
    pairs = discover_book_urls()
    records = [extract_book(url, source_page=source) for url, source in pairs]
    print(json.dumps(records[0], indent=2))
    print(f"detail_pages={len(records)}")

if __name__ == "__main__":
    main()

def main():
    pairs = discover_book_urls()
    records = [extract_book(url, source_page=source) for url, source in pairs]
    valid_count, invalid_count = validate_and_store(records)
    print(f"valid_records={valid_count} invalid_records={invalid_count}")

if __name__ == "__main__":
    main()

def main():
    start_time = datetime.now(timezone.utc)
    pairs = discover_book_urls()

    records = []
    failed_pages = 0

    for url, source in pairs:
        try:
            records.append(extract_book(url, source_page=source))
        except Exception as e:
            print(f"SKIPPED {url} -> {e}")
            failed_pages += 1

    valid_count, invalid_count = validate_and_store(records)
    fetch_count, cache_hit_count = get_and_reset_counts()

    write_report(
        start_time=start_time,
        pages_fetched=fetch_count,
        cache_hits=cache_hit_count,
        valid_records=valid_count,
        invalid_records=invalid_count,
        failed_pages=failed_pages,
    )

if __name__ == "__main__":
    main()