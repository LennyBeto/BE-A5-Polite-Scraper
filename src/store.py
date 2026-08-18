import json
from pathlib import Path
from pydantic import ValidationError
from schema import Book, normalize_record

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def validate_and_store(raw_records: list[dict]) -> tuple[int, int]:
    OUTPUT_DIR.mkdir(exist_ok=True)
    valid_by_url: dict[str, dict] = {}
    errors: list[dict] = []

    for raw in raw_records:
        try:
            normalized = normalize_record(raw)
            book = Book(**normalized)
            valid_by_url[book.product_url] = book.model_dump()
        except ValidationError as e:
            errors.append({"record": raw, "reason": str(e)})

    valid_records = list(valid_by_url.values())
    (OUTPUT_DIR / "books.json").write_text(json.dumps(valid_records, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")

    return len(valid_records), len(errors)