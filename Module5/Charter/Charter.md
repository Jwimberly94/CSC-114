Project Charter: Alabama Housing Market (Tabular Reskin)

What we're building (one sentence)

A regression model that predicts a county's median home listing price for a given month, using Alabama county-level real estate market data.

Cohort

Tabular

The data or tools we'll use


alabama_housing.csv — county-month real estate snapshots for Alabama, ~67 counties, spanning 201607–202606 (6,902 rows total)
Features: active_listing_count, median_days_on_market, new_listing_count, price_increased_count, price_reduced_count, pending_listing_count, median_square_feet, total_listing_count
(county_fips / county_name identify the row and are not used as model inputs this round)
Target: median_listing_price
Keras 3 on the JAX backend, following the same build → compile → fit → predict pattern used in the California Housing example
Evaluation protocol: time-based split, not random — train on month_date_yyyymm ≤ 202412, test on ≥ 202501, to avoid leaking a county's own near-future price into training


Definition of "good enough"

Before we build, we agree this project is good enough when:


Test MAE (on the confirmed held-out set: 1,191 rows, months 202501–202606) beats a naive baseline — e.g., "predict last known price for that county" or "predict the training-set mean"
Split confirmed and healthy — no fallback needed:

Train: 5,711 rows, months ≤ 202412 (~82.7%)
Test: 1,191 rows, months 202501–202606, 18 full months, 65–67 counties per month (~17.3%)





What we are NOT doing (scope guard)


Not using a random train/test split — date-based split only, since random splitting would leak a county's own future prices into training
Not modeling per-county trends explicitly (e.g., no county as a categorical feature/embedding) this round — treating counties as pooled rows for the first pass
No feature engineering beyond normalization (mean/std scaling of numeric features), consistent with the earlier Housing example
No deployment or productionization


Team & roles

Solo — Captain Wimberly. Self-review documented in P