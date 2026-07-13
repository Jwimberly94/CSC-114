"""
My first California Housing regression model.
A minimal build -> compile -> fit -> predict pipeline. We'll improve it later.
"""

import os

# Keras 3 can run on JAX, TensorFlow, or PyTorch. Pick JAX to match requirements.txt.
os.environ.setdefault("KERAS_BACKEND", "jax")

import keras
from keras import layers
from keras.datasets import california_housing


# ---- 1. LOAD THE DATA ----
# Each row describes a California neighborhood (median income, house age, etc.);
# the target is that neighborhood's median house price.
(train_data, train_targets), (test_data, test_targets) = (
    california_housing.load_data(version="small")
)
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
model.fit(x_train, y_train, epochs=20, batch_size=16, verbose=1)


# ---- 5. EVALUATE & PREDICT ----
# Check performance on data the model never trained on.
test_loss, test_mae = model.evaluate(x_test, y_test, verbose=0)
print("\nTest MAE:", round(float(test_mae), 3), "(x $100,000)")

# Predict prices for the first 5 test neighborhoods and compare to the truth.
predictions = model.predict(x_test[:5])
for i in range(5):
    print(f"Predicted: {predictions[i][0]:.2f}   Actual: {y_test[i]:.2f}")
