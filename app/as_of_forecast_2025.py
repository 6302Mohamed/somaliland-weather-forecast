import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Page config MUST be first
# -----------------------------
st.set_page_config(
    page_title="As-Of Weather Forecast (2025)",
    layout="wide"
)

CSV_PATH = Path("reports/naive_walk_forward_2025.csv")

st.title("As-Of Weather Forecast — Hargeisa (2025)")
st.caption(
    "Historical walk-forward forecasting • "
    "Each forecast uses only information available on that day"
)

st.markdown(
    "_A disciplined baseline-first forecasting system evaluated using walk-forward testing._"
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_forecasts():
    df = pd.read_csv(CSV_PATH, parse_dates=["forecast_date"])
    df = df.sort_values("forecast_date").reset_index(drop=True)
    return df

if not CSV_PATH.exists():
    st.error(f"Missing file: {CSV_PATH}")
    st.stop()

df = load_forecasts()

# -----------------------------
# Performance summary
# -----------------------------
mean_mae = df["abs_error"].mean()
p90_error = df["abs_error"].quantile(0.90)

st.markdown(
    f"""
**2025 Performance Summary**
- Mean Absolute Error: **{mean_mae:.2f} °C**
- 90% of days error ≤ **{p90_error:.2f} °C**
"""
)

# -----------------------------
# Date selector
# -----------------------------
st.sidebar.header("Select forecast date")

available_dates = df["forecast_date"].dt.date.unique()

selected_date = st.sidebar.slider(
    "Forecasted day (tomorrow)",
    min_value=available_dates[0],
    max_value=available_dates[-1],
    value=available_dates[30],
    format="YYYY-MM-DD"
)

row = df[df["forecast_date"].dt.date == selected_date].iloc[0]

forecast_value = row["forecast"]
actual_value = row["actual"]
error_value = row["error"]

# -----------------------------
# Metrics
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Forecasted date",
    selected_date.strftime("%Y-%m-%d")
)

c2.metric(
    "Predicted max temp",
    f"{forecast_value:.1f} °C"
)

c3.metric(
    "Actual max temp",
    f"{actual_value:.1f} °C"
)

delta_color = "normal" if abs(error_value) < 1.0 else "inverse"

c4.metric(
    "Error (Actual − Predicted)",
    f"{error_value:+.1f} °C",
    delta="Good" if abs(error_value) < 1.0 else "Large",
    delta_color=delta_color
)

st.info(
    "This forecast was generated using a **naive persistence baseline**:\n\n"
    "`Tomorrow ≈ Today`\n\n"
    "The value shown is exactly what the system would have produced on that day."
)

# -----------------------------
# Context plot (last 14 days)
# -----------------------------
st.subheader("Forecast Context (Last 14 Days)")

end_idx = df.index[df["forecast_date"].dt.date == selected_date][0]
start_idx = max(0, end_idx - 14)

context = df.iloc[start_idx:end_idx + 1]

fig, ax = plt.subplots(figsize=(12, 4))

ax.plot(
    context["forecast_date"],
    context["actual"],
    label="Actual",
    linewidth=1
)

ax.plot(
    context["forecast_date"],
    context["forecast"],
    label="Naive forecast",
    linewidth=1
)

ax.scatter(
    selected_date,
    actual_value,
    s=80,
    label="Selected day",
    zorder=3
)

ax.set_title("Actual vs Naive Forecast (14-day context)")
ax.set_xlabel("Date")
ax.set_ylabel("Max Temperature (°C)")
ax.grid(True)
ax.legend()
fig.tight_layout()

st.pyplot(fig)

# -----------------------------
# Raw row (optional transparency)
# -----------------------------
with st.expander("Show raw forecast record"):
    st.dataframe(
        row.to_frame(name="value"),
        use_container_width=True
    )

st.caption(
    "Dataset: Open-Meteo archive (2021–2025) • "
    "Evaluation: walk-forward forecasting over 2025"
)
