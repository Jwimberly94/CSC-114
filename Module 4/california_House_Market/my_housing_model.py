"""
My first Alabama Housing regression model.
A minimal build -> compile -> fit -> predict pipeline. We'll improve it later.
"""

import csv
import os

# Keras 3 can run on JAX, TensorFlow, or PyTorch. Pick JAX to match requirements.txt.
os.environ.setdefault("KERAS_BACKEND", "jax")

import keras
import matplotlib
import numpy as np
from keras import layers

# Codespaces are headless (no display), so save plots to PNG files instead of
# trying to open a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---- 1. LOAD THE DATA ----
# Each row is one Alabama county in one month (2016-2026); the target is that
# county's median home *listing* price for the month. Source: alabama_housing.csv,
# built from realtor.com's public county-level housing market research data
# (https://www.realtor.com/research/data/), filtered to Alabama counties.
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

data_path = os.path.join(os.path.dirname(__file__), "alabama_housing.csv")
features = []
targets = []
months = []
with open(data_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        months.append(int(row["month_date_yyyymm"]))
        features.append([float(row[c]) for c in FEATURE_COLUMNS])
        targets.append(float(row[TARGET_COLUMN]))

features = np.array(features, dtype="float32")
targets = np.array(targets, dtype="float32")
months = np.array(months, dtype="int32")

# Chronological split to avoid temporal leakage:
# train on 2016-2024, test on 2025-2026.
train_idx = np.where(months <= 202412)[0]
test_idx = np.where(months >= 202501)[0]

if len(train_idx) == 0 or len(test_idx) == 0:
    raise ValueError(
        "Chronological split failed: expected rows for train (<=202412) and "
        "test (>=202501)."
    )

train_data, test_data = features[train_idx], features[test_idx]
train_targets, test_targets = targets[train_idx], targets[test_idx]
print("Train features:", train_data.shape, " Test features:", test_data.shape)

# Normalize features: subtract the mean, divide by the standard deviation, using
# ONLY the training set's stats. This puts every feature on a comparable scale so
# no single large-numbered feature dominates learning.
mean = train_data.mean(axis=0)
std = train_data.std(axis=0)
x_train = (train_data - mean) / std
x_test = (test_data - mean) / std

# Scale targets from dollars down to "hundreds of thousands" so the numbers the
# network predicts stay small and easy to train on.
y_train = train_targets / 100000
y_test = test_targets / 100000


# ---- 2. BUILD THE MODEL ----
# A Sequential model is just a stack of layers, top to bottom.
# One hidden layer (64 neurons, ReLU) learns patterns; the final single neuron
# outputs one number -- the predicted price. No activation on the output because
# in regression we want the raw number, not a probability.
model = keras.Sequential(
    [
        layers.Dense(64, activation="relu"),
        layers.Dense(1),
    ]
)


# ---- 3. COMPILE THE MODEL ----
# Tell Keras HOW to train:
#   optimizer -> "adam" is a solid default that adjusts the weights.
#   loss -> mean_squared_error is what the model actively minimizes.
#   metrics -> mean_absolute_error is easier for us to read (avg error, same units
#              as the target: 0.5 == being off by ~$50,000).
model.compile(
    optimizer="adam",
    loss="mean_squared_error",
    metrics=["mean_absolute_error"],
)


# ---- 4. FIT (TRAIN) THE MODEL ----
# Show the data to the model repeatedly (epochs) in small groups (batch_size),
# nudging the weights each time to reduce the loss.
history = model.fit(x_train, y_train, epochs=20, batch_size=16, verbose=1)


# ---- 5. EVALUATE & PREDICT ----
# Check performance on data the model never trained on.
test_loss, test_mae = model.evaluate(x_test, y_test, verbose=0)
print("\nTest MAE:", round(float(test_mae), 3), "(x $100,000)")

# Predict prices for the first 5 test county/month rows and compare to the truth.
predictions = model.predict(x_test[:5])
for i in range(5):
    print(f"Predicted: {predictions[i][0]:.2f}   Actual: {y_test[i]:.2f}")


# ---- 6. PLOT TRAINING HISTORY ----
# Chart how the training loss (MSE) and MAE improved epoch by epoch, and save
# it next to this script so you don't need a display to see it.
plot_path = os.path.join(os.path.dirname(__file__), "training_history.png")
epochs = range(1, len(history.history["loss"]) + 1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.plot(epochs, history.history["loss"])
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Training loss (MSE)")
ax1.set_title("Loss per epoch")

ax2.plot(epochs, history.history["mean_absolute_error"])
ax2.set_xlabel("Epoch")
ax2.set_ylabel("Training MAE (x $100,000)")
ax2.set_title("MAE per epoch")

fig.tight_layout()
fig.savefig(plot_path, dpi=120, bbox_inches="tight")
print(f"\nSaved training plot to {plot_path}")
