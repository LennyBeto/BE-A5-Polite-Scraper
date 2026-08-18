import json
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def write_report(start_time, pages_fetched, cache_hits, valid_records, invalid_records, failed_pages):
    end_time = datetime.now(timezone.utc)
    report = {
        "start_time": start_time.isoformat(),
        "duration_seconds": round((end_time - start_time).total_seconds(), 2),
        "pages_fetched": pages_fetched,
        "cache_hits": cache_hits,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "failed_pages": failed_pages,
    }
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "run-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))