from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fetch import fetch

CATALOGUE_START = "https://books.toscrape.com/catalogue/page-1.html"


def discover_book_urls() -> list[tuple[str, str]]:
    page_url = CATALOGUE_START
    all_pairs: list[tuple[str, str]] = []
    pages_visited = 0

    while page_url:
        html = fetch(page_url)
        soup = BeautifulSoup(html, "html.parser")
        pages_visited += 1

        for article in soup.select("article.product_pod"):
            href = article.select_one("h3 a")["href"]
            absolute_url = urljoin(page_url, href)
            all_pairs.append((absolute_url, page_url))

        next_link = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_link["href"]) if next_link else None

    seen = set()
    unique_pairs = []
    for url, source in all_pairs:
        if url not in seen:
            seen.add(url)
            unique_pairs.append((url, source))

    print(f"catalogue_pages={pages_visited} discovered={len(all_pairs)} unique_urls={len(unique_pairs)}")
    return unique_pairs