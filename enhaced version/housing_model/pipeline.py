"""Pipeline entrypoint for running the full model workflow."""

from __future__ import annotations

import os

from .config import UTILITY_BASE_MONTHLY, UTILITY_RATE_PER_SQFT
from .data import load_data, prepare_split
from .modeling import build_model, evaluate_and_predict, train_model
from .plotting import (
    plot_actual_vs_predicted,
    plot_estimated_utilities,
    plot_major_county_prices,
    plot_training_history,
)


def run_pipeline() -> None:
    cwd = os.getcwd()
    data_bundle = load_data(cwd)
    split = prepare_split(data_bundle)

    print("Train features:", split.train_data_shape, " Test features:", split.test_data_shape)

    model = build_model()
    history = train_model(model, split.x_train, split.y_train)

    test_mae, test_predictions = evaluate_and_predict(model, split.x_test, split.y_test)
    print("\nTest MAE:", round(test_mae, 3), "(x $100,000)")

    preview_predictions = test_predictions[:5]
    for idx in range(5):
        print(f"Predicted: {preview_predictions[idx]:.2f}   Actual: {split.y_test[idx]:.2f}")

    training_plot_path = plot_training_history(history, cwd)
    print(f"\nSaved training plot to {training_plot_path}")

    actual_dollars = split.y_test * 100000
    predicted_dollars = test_predictions * 100000

    trend_plot_path = plot_actual_vs_predicted(
        split.test_months,
        actual_dollars,
        predicted_dollars,
        cwd,
    )
    print(f"Saved trend plot to {trend_plot_path}")

    locations_plot_path = plot_major_county_prices(
        split.test_county_names,
        actual_dollars,
        predicted_dollars,
        cwd,
    )
    print(f"Saved locations plot to {locations_plot_path}")

    utilities_plot_path = plot_estimated_utilities(
        split.test_county_names,
        split.test_sqft,
        cwd,
    )
    print(
        f"Saved utilities estimate plot to {utilities_plot_path} "
        f"(base=${UTILITY_BASE_MONTHLY:.0f} + ${UTILITY_RATE_PER_SQFT:.2f}/sqft)"
    )


if __name__ == "__main__":
    run_pipeline()
