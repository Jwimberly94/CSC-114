"""Plot generation for model outputs."""

from __future__ import annotations

import os

import matplotlib
import numpy as np

from .config import (
    MAJOR_COUNTIES,
    UTILITY_BASE_MONTHLY,
    UTILITY_RATE_PER_SQFT,
    canonical_county_name,
)

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_training_history(history, cwd: str) -> str:
    plot_path = os.path.join(cwd, "training_history.png")
    epochs = range(1, len(history.history["loss"]) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle("Training history (model trained with data through 2026)")

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
    plt.close(fig)
    return plot_path


def plot_actual_vs_predicted(test_months, actual_dollars, predicted_dollars, cwd: str) -> str:
    unique_test_months = np.sort(np.unique(test_months))
    monthly_actual = []
    monthly_predicted = []

    for month_value in unique_test_months:
        month_mask = test_months == month_value
        monthly_actual.append(float(actual_dollars[month_mask].mean()))
        monthly_predicted.append(float(predicted_dollars[month_mask].mean()))

    trend_plot_path = os.path.join(cwd, "actual_vs_predicted_prices.png")
    fig, ax = plt.subplots(figsize=(10, 4.5))

    month_positions = np.arange(len(unique_test_months))
    ax.plot(month_positions, monthly_actual, marker="o", label="Actual monthly mean price")
    ax.plot(month_positions, monthly_predicted, marker="o", label="Predicted monthly mean price")

    years = unique_test_months // 100
    year_tick_positions = []
    year_tick_labels = []
    for pos, year in enumerate(years):
        if pos == 0 or year != years[pos - 1]:
            year_tick_positions.append(pos)
            year_tick_labels.append(str(int(year)))

    ax.set_xticks(year_tick_positions)
    ax.set_xticklabels(year_tick_labels)
    ax.set_xlabel("Year")
    ax.set_ylabel("Median listing price ($)")
    ax.set_title("Held-out period (2025-2026): actual vs predicted prices")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend()

    fig.tight_layout()
    fig.savefig(trend_plot_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return trend_plot_path


def plot_major_county_prices(test_county_names, actual_dollars, predicted_dollars, cwd: str) -> str:
    major_counties_set = {canonical_county_name(county) for county in MAJOR_COUNTIES}
    major_actual_sums = {}
    major_predicted_sums = {}
    major_row_counts = {}

    for county, actual_price, predicted_price in zip(
        test_county_names,
        actual_dollars,
        predicted_dollars,
    ):
        county_key = canonical_county_name(str(county))
        if county_key not in major_counties_set:
            continue

        major_actual_sums[county_key] = major_actual_sums.get(county_key, 0.0) + float(actual_price)
        major_predicted_sums[county_key] = major_predicted_sums.get(county_key, 0.0) + float(predicted_price)
        major_row_counts[county_key] = major_row_counts.get(county_key, 0) + 1

    major_county_rows = []
    for county in MAJOR_COUNTIES:
        county_key = canonical_county_name(county)
        if county_key not in major_row_counts:
            continue

        count = major_row_counts[county_key]
        display_name = county_key.title() + " County"
        major_county_rows.append(
            (
                display_name,
                major_actual_sums[county_key] / count,
                major_predicted_sums[county_key] / count,
            )
        )

    major_county_rows.sort(key=lambda row: row[1])

    locations_plot_path = os.path.join(cwd, "best_price_locations.png")
    fig, ax = plt.subplots(figsize=(10, 5))

    if not major_county_rows:
        ax.text(
            0.5,
            0.5,
            "No major county rows matched in test period.",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        ax.set_axis_off()
    else:
        county_labels = [item[0] for item in major_county_rows]
        actual_values = [item[1] for item in major_county_rows]
        predicted_values = [item[2] for item in major_county_rows]

        bar_positions = np.arange(len(county_labels))
        bar_height = 0.38
        ax.barh(
            bar_positions - bar_height / 2,
            actual_values,
            height=bar_height,
            color="#2b8cbe",
            label="Actual avg price",
        )
        ax.barh(
            bar_positions + bar_height / 2,
            predicted_values,
            height=bar_height,
            color="#f39c34",
            label="Predicted avg price",
        )

        ax.set_yticks(bar_positions)
        ax.set_yticklabels(county_labels)
        ax.invert_yaxis()
        ax.set_xlabel("Average median listing price on held-out period ($)")
        ax.set_ylabel("County")
        ax.set_title("Major Alabama counties: actual vs predicted avg prices (2025-2026)")
        ax.grid(axis="x", linestyle="--", alpha=0.35)
        ax.legend()

    fig.tight_layout()
    fig.savefig(locations_plot_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return locations_plot_path


def plot_estimated_utilities(test_county_names, test_sqft, cwd: str) -> str:
    county_sqft_sums = {}
    county_counts = {}
    for county, sqft in zip(test_county_names, test_sqft):
        county_key = str(county)
        county_sqft_sums[county_key] = county_sqft_sums.get(county_key, 0.0) + float(sqft)
        county_counts[county_key] = county_counts.get(county_key, 0) + 1

    county_utility_estimates = []
    for county_key, sqft_sum in county_sqft_sums.items():
        avg_sqft = sqft_sum / county_counts[county_key]
        est_monthly_utilities = UTILITY_BASE_MONTHLY + (UTILITY_RATE_PER_SQFT * avg_sqft)
        county_utility_estimates.append((county_key, est_monthly_utilities))

    county_utility_estimates.sort(key=lambda item: item[1])

    utilities_plot_path = os.path.join(cwd, "estimated_utilities_by_county.png")
    fig, ax = plt.subplots(figsize=(12, 18))
    utility_labels = [item[0] for item in county_utility_estimates]
    utility_values = [item[1] for item in county_utility_estimates]

    ax.barh(utility_labels, utility_values, color="#6baed6")
    ax.set_xlabel("Estimated monthly utilities ($)")
    ax.set_ylabel("County")
    ax.set_title("Estimated monthly utilities by county (size-based proxy, 2025-2026)")
    ax.grid(axis="x", linestyle="--", alpha=0.35)

    fig.tight_layout()
    fig.savefig(utilities_plot_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return utilities_plot_path
