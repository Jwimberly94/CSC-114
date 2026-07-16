"""Model creation, training, and evaluation."""

from __future__ import annotations

import os

os.environ.setdefault("KERAS_BACKEND", "jax")

import keras
from keras import layers


def build_model() -> keras.Model:
    model = keras.Sequential(
        [
            layers.Dense(64, activation="relu"),
            layers.Dense(1),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mean_absolute_error"],
    )
    return model


def train_model(model: keras.Model, x_train, y_train):
    return model.fit(x_train, y_train, epochs=20, batch_size=16, verbose=1)


def evaluate_and_predict(model: keras.Model, x_test, y_test):
    _, test_mae = model.evaluate(x_test, y_test, verbose=0)
    test_predictions = model.predict(x_test, verbose=0).flatten()
    return float(test_mae), test_predictions
