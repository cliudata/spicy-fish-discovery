"""Illustrative inventory stress test; inputs and outputs are not business observations."""
from dataclasses import dataclass
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Assumptions:
    days: int = 21
    daily_demand: int = 10
    opening_stock: int = 120
    inbound_units: int = 100
    arrival_day: int = 9
    delay_days: int = 0


def simulate(a: Assumptions):
    """Ship demand from available stock; one known inbound batch arrives before day demand."""
    if min(a.days, a.daily_demand, a.opening_stock, a.inbound_units, a.arrival_day, a.delay_days) < 0 or a.days == 0 or a.arrival_day == 0:
        raise ValueError("Use nonnegative counts and positive horizon and arrival day")
    stock = a.opening_stock
    rows = []
    for day in range(1, a.days + 1):
        if day == a.arrival_day + a.delay_days:
            stock += a.inbound_units
        fulfilled = min(stock, a.daily_demand)
        stock -= fulfilled
        rows.append((day, fulfilled, a.daily_demand - fulfilled, stock))
    return rows


def main():
    baseline = Assumptions()
    delayed = Assumptions(delay_days=7)
    buffer = Assumptions(opening_stock=150, delay_days=7)
    cases = {"On-time delivery": baseline, "Seven-day delay": delayed, "Delay + 30-unit buffer": buffer}
    fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
    for label, assumptions in cases.items():
        rows = simulate(assumptions)
        cumulative = []
        running = 0
        for day, fulfilled, lost, stock in rows:
            running += fulfilled
            cumulative.append(running)
        loss = sum(r[2] for r in rows)
        print(f"{label}: fulfilled={running}; unfilled={loss}; ending_stock={rows[-1][-1]}")
        ax.plot(range(1, assumptions.days+1), cumulative, linewidth=2.7,
                label=f"{label}  |  {loss} unfilled units")
    ax.set(title="Inventory response to a hypothetical delivery delay", xlabel="Scenario day",
           ylabel="Cumulative units fulfilled in the model", xlim=(1, baseline.days), ylim=(0, 220))
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    ax.text(1, -0.22, "SCENARIO ONLY  |  NOT CHITARO MART DATA", transform=ax.transAxes,
            ha="right", va="top", color="#9a3741", fontsize=9, fontweight="bold")
    (ROOT / "charts").mkdir(exist_ok=True)
    fig.savefig(ROOT / "charts" / "disruption_scenario.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
