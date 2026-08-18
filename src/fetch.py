import time
from pathlib import Path
import requests

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/LennyBeto/BE-A5-Polite-Scraper)"
TIMEOUT_SECONDS = 10
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
_cache_hit_count = 0
_fetch_count = 0


def get_and_reset_counts() -> tuple[int, int]:
    global _cache_hit_count, _fetch_count
    counts = (_fetch_count, _cache_hit_count)
    _fetch_count = 0
    _cache_hit_count = 0
    return counts


def fetch(url: str, _retry: bool = True) -> str:
    CACHE_DIR.mkdir(exist_ok=True)
    path = _cache_path(url)

    if path.exists():
        html = path.read_text(encoding="utf-8")
        print(f"CACHE HIT {url} ({len(html)} bytes)")
        global _cache_hit_count
        _cache_hit_count += 1
        return html

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        if _retry:
            print(f"TIMEOUT {url} -> retrying once")
            time.sleep(1)
            return fetch(url, _retry=False)
        raise RuntimeError(f"FETCH FAILED {url} -> timeout (after retry)")

    if response.status_code in (404, 403):
        raise RuntimeError(f"FETCH FAILED {url} -> status {response.status_code} (not retried)")

    if response.status_code >= 500 and _retry:
        print(f"SERVER ERROR {response.status_code} {url} -> retrying once")
        time.sleep(1)
        return fetch(url, _retry=False)

    if response.status_code != 200:
        raise RuntimeError(f"FETCH FAILED {url} -> status {response.status_code}")

    html = response.text
    path.write_text(html, encoding="utf-8")
    print(f"FETCH {url} ({len(html)} bytes)")
    global _fetch_count
    _fetch_count += 1
    time.sleep(0.5)

    return html