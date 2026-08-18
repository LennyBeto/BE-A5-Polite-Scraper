from fetch import fetch
from discover import discover_book_urls

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