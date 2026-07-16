"""Configuration and shared constants for the Alabama housing model."""

FEATURE_COLUMNS = [
    "active_listing_count",
    "median_days_on_market",
    "new_listing_count",
    "price_increased_count",
    "price_reduced_count",
    "pending_listing_count",
    "median_square_feet",
    "total_listing_count",
]

TARGET_COLUMN = "median_listing_price"

MAJOR_COUNTIES = [
    "Jefferson",
    "Mobile",
    "Madison",
    "Montgomery",
    "Shelby",
    "Baldwin",
    "Tuscaloosa",
    "Lee",
    "Morgan",
    "Calhoun",
]

UTILITY_BASE_MONTHLY = 90.0
UTILITY_RATE_PER_SQFT = 0.12


def canonical_county_name(name: str) -> str:
    normalized = str(name).strip().lower()
    normalized = normalized.replace(", al", "")
    normalized = normalized.replace(" county", "")
    return normalized
