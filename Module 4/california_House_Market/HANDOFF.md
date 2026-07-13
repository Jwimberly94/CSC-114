# Handoff notes — California Housing regression

Context for anyone (human or AI assistant) picking up this work.

## What exists

- `my_housing_model.py` — a **minimal** Keras regression baseline on the
  built-in California Housing dataset. Pipeline: load → normalize features →
  scale target → build (1 hidden layer, 64 ReLU units) → compile (Adam / MSE,
  MAE metric) → fit (20 epochs) → evaluate on the test set → print predictions.
  Intentionally simple; meant to be improved one change at a time.
- `example_03_california_housing_regression.py` — the fuller book example
  (K-fold cross-validation, MAE plots). Reference, not the working file.

## Environment

- Python 3.12, Keras 3.15 on the **JAX** CPU backend (`KERAS_BACKEND=jax`).
- Install with: `pip install -r requirements.txt`
  (installs keras, jax[cpu], matplotlib, numpy — **not** tensorflow or
  scikit-learn; the scripts don't need them).

## How to run

```bash
python my_housing_model.py
```

## Next planned step (not yet started)

Swap the dataset from **California to Alabama**.

- Data loads today via `keras.datasets.california_housing.load_data()`
  (see `my_housing_model.py`, step 1). Keras has **no built-in Alabama
  dataset**, so this can't be a one-line swap.
- Need to supply an Alabama dataset (likely a CSV) and load it manually into:
  a 2-D feature array, a 1-D price target, and a train/test split.
- Watch for column differences vs. California's 8 census-block features
  (MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Lat, Long):
  per-listing vs per-neighborhood data, non-numeric columns (city/zip/type)
  that must be dropped or encoded, missing values, and a different target
  column/units (the current `/ 100000` target scaling may need to change).
- **Blocker:** we still need to obtain the Alabama dataset file.
