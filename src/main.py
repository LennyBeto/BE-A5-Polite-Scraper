from fetch import fetch

def main():
    html = fetch("https://books.toscrape.com/catalogue/page-1.html")
    print(f"Fetched {len(html)} characters")

if __name__ == "__main__":
    main()