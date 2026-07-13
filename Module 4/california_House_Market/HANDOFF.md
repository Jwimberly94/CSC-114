# Handoff notes — Alabama Housing regression

Context for anyone (human or AI assistant) picking up this work.

## What exists

- `my_housing_model.py` — a **minimal** Keras regression baseline, now trained
  on real Alabama county-level housing market data (`alabama_housing.csv`).
  Pipeline: load CSV → chronological split (train: 2016-2024, test: 2025-2026)
  → normalize features → scale target → build (1 hidden layer, 64 ReLU units)
  → compile (Adam / MSE, MAE metric) → fit (20 epochs) → evaluate on the
  test set → print predictions.
  Intentionally simple; meant to be improved one change at a time.
- `alabama_housing.csv` — 6,902 rows (67 Alabama counties × ~103 months,
  2016-07 to 2026-06), derived from realtor.com's public Housing Market
  research data (county-level CSV at
  https://www.realtor.com/research/data/, "Inventory Core Metrics - County").
  Columns: `month_date_yyyymm`, `county_fips`, `county_name`, 8 numeric
  features (`active_listing_count`, `median_days_on_market`,
  `new_listing_count`, `price_increased_count`, `price_reduced_count`,
  `pending_listing_count`, `median_square_feet`, `total_listing_count`), and
  the target `median_listing_price`. Rows with missing values in any of
  those columns were dropped when building the file.
- `example_03_california_housing_regression.py` — the fuller book example
  (K-fold cross-validation, MAE plots), still using the original California
  dataset. Reference, not the working file.

## Environment

- Python 3.12, Keras 3.15 on the **JAX** CPU backend (`KERAS_BACKEND=jax`).
- Install with: `pip install -r requirements.txt`
  (installs keras, jax[cpu], matplotlib, numpy — **not** tensorflow or
  scikit-learn; the scripts don't need them). CSV parsing uses the
  standard-library `csv` module, no pandas required.

## How to run

```bash
python my_housing_model.py
```

Current baseline result (chronological split): Test MAE ≈ 0.58 (× $100,000),
i.e. off by about $58,000 on average.

## Completed step

Swapped the dataset from **California to Alabama** (see commit history).
Keras has no built-in Alabama dataset, so it was replaced with a real,
sourced CSV of Alabama county housing-market metrics, loaded manually in
`my_housing_model.py` step 1 (feature/target column lists, CSV read via
`csv.DictReader`, chronological split using `month_date_yyyymm` to reduce
time leakage).

Note: unlike California's per-block-group demographic features (income,
rooms, population, lat/long), the Alabama features are market-activity
indicators (inventory counts, days on market, price change counts, etc.) at
county-month granularity — the closest real, freely available substitute.

## Possible next steps (not yet started)

- Try more/fewer epochs, hidden units, or additional hidden layers.
- Add K-fold cross-validation (see `example_03_california_housing_regression.py`
  for the pattern) since the dataset is bigger now (~6,900 rows).
- Investigate feature importance / try dropping weaker features.
- Consider adding `county_name` as a one-hot/embedded categorical feature.
