import time
from pathlib import Path
import requests

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/LennyBeto/BE-A5-Polite-Scraper)"
TIMEOUT_SECONDS = 10
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"


def _cache_path(url: str) -> Path:
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")
    return CACHE_DIR / f"{safe_name}.html"


def fetch(url: str) -> str:
    CACHE_DIR.mkdir(exist_ok=True)
    path = _cache_path(url)

    if path.exists():
        html = path.read_text(encoding="utf-8")
        print(f"CACHE HIT {url} ({len(html)} bytes)")
        return html

    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)

    if response.status_code != 200:
        raise RuntimeError(f"FETCH FAILED {url} -> status {response.status_code}")

    html = response.text
    path.write_text(html, encoding="utf-8")
    print(f"FETCH {url} ({len(html)} bytes)")
    time.sleep(0.5)  # politeness delay — only after a real request, never on a cache hit

    return html