"""Validate and visualize the supplied synthetic order sample."""
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sample_orders.csv"
CHARTS = ROOT / "charts"
STAMP = "SYNTHETIC EXAMPLE  |  NOT BUSINESS HISTORY"
COLORS = {"new": "#167d8d", "familiar": "#e49c42"}


def load_and_validate():
    df = pd.read_csv(DATA)
    expected = ["order_id", "month", "customer_familiarity", "acquisition_channel", "units"]
    if list(df.columns) != expected:
        raise ValueError(f"Expected columns {expected}; found {list(df.columns)}")
    if df.empty or df.isna().any().any() or not df.order_id.is_unique:
        raise ValueError("Data must have rows, no missing values and unique order IDs")
    if not df.customer_familiarity.isin(["new", "familiar"]).all():
        raise ValueError("Unexpected familiarity label")
    if not df.acquisition_channel.isin(["tiktok_creator", "search", "referral", "repeat_purchase"]).all():
        raise ValueError("Unexpected source label")
    if not df.month.map(lambda x: isinstance(x, str) and bool(re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", x))).all():
        raise ValueError("Invalid month format")
    if not pd.api.types.is_integer_dtype(df.units) or (df.units <= 0).any():
        raise ValueError("Units must be positive integers")
    return df


def finish(fig, ax, filename):
    ax.text(1, 1.10, STAMP, transform=ax.transAxes, fontsize=8,
            color="#9a3741", fontweight="bold", ha="right", va="bottom")
    fig.savefig(CHARTS / filename, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    df = load_and_validate()
    CHARTS.mkdir(exist_ok=True)
    mix = df.customer_familiarity.value_counts().reindex(["new", "familiar"])
    crosstab = pd.crosstab(df.customer_familiarity, df.acquisition_channel)
    share = crosstab.div(crosstab.sum(axis=1), axis=0).mul(100)
    trend = df.groupby("month", sort=True).agg(orders=("order_id", "count"), units=("units", "sum"))
    print(f"Synthetic orders: {len(df):,}; synthetic units: {df.units.sum():,}")
    print("\nOrders by constructed familiarity:\n", mix.to_string())
    print("\nSource labels within constructed familiarity (%):\n", share.round(1).to_string())
    print("\nSynthetic monthly trend (not business history):\n", trend.to_string())

    fig, ax = plt.subplots(figsize=(7.5, 4.5), layout="constrained")
    bars = ax.bar(["New label", "Familiar label"], mix, color=[COLORS["new"], COLORS["familiar"]], width=0.58)
    ax.bar_label(bars, labels=[f"{v:,}  ({v/len(df):.1%})" for v in mix], padding=4)
    ax.set_ylim(0, mix.max() * 1.25)
    ax.set_ylabel("Synthetic orders (not people)")
    ax.set_title("Constructed familiarity mix", loc="left", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, ax, "customer_mix.png")

    ordered = ["tiktok_creator", "search", "referral", "repeat_purchase"]
    fig, ax = plt.subplots(figsize=(8.5, 4.9), layout="constrained")
    left = pd.Series(0.0, index=["new", "familiar"])
    colors = ["#167d8d", "#4a6387", "#e49c42", "#a16870"]
    for category, color in zip(ordered, colors):
        vals = share.reindex(["new", "familiar"])[category]
        ax.barh(["New label", "Familiar label"], vals, left=left.to_numpy(), label=category.replace("_", " "), color=color)
        left += vals.to_numpy()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of synthetic orders within each group (%)")
    ax.set_title("Constructed source label by familiarity", loc="left", fontweight="bold")
    ax.legend(ncol=2, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.20))
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, ax, "channel_mix.png")



if __name__ == "__main__":
    main()
