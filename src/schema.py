import re
from pydantic import BaseModel, field_validator

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class Book(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str | None
    rating_value: int | None
    description: str | None
    source_page: str
    fetched_at: str

    @field_validator("product_url")
    @classmethod
    def must_be_https(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError("product_url must be an absolute https:// URL")
        return v

    @field_validator("price_gbp")
    @classmethod
    def must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("price_gbp must be a positive number")
        return v


def normalize_record(raw: dict) -> dict:
    price_match = re.search(r"[\d.]+", raw["price_text"])
    price_gbp = float(price_match.group()) if price_match else None
    rating_value = RATING_WORDS.get(raw.get("rating_text"))
    return {**raw, "price_gbp": price_gbp, "rating_value": rating_value}