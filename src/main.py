import json
from discover import discover_book_urls
from extract import extract_book
from fetch import fetch
from store import validate_and_store

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