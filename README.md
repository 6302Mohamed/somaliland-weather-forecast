# 🌤️ Somaliland Weather Forecasting (V1)

**Daily Maximum Temperature Forecasting for Hargeisa using Walk-Forward Time Series Evaluation**

This repository presents a disciplined, baseline-first approach to time-series weather forecasting for **Hargeisa, Somaliland**.  
The project emphasizes **data integrity, proper evaluation, and honest conclusions**, rather than model complexity or hype.

An interactive Streamlit dashboard allows inspection of historical forecasts exactly as they would have been produced at the time.

🔗 **Live Dashboard:**  
https://somaliland-weather-forecast-mgjhspkx32dyiqbyzwkhmy.streamlit.app/

---

## 🎯 Project Motivation

Many forecasting and ML portfolio projects:

- rely on a single prediction  
- ignore proper time-aware backtesting  
- overuse complex models without checking if the data supports them  

This project intentionally takes a different path:

> **Start simple, evaluate rigorously, and only add complexity if it clearly improves performance.**

Hargeisa is an ideal case study due to its **stable semi-arid climate**, where daily maximum temperature changes are often gradual and highly persistent.

---

## 📊 Dataset

### Source
- **Open-Meteo Weather API**
- Daily **observed / archive** weather data (not forecast output)

### Coverage
- **Location:** Hargeisa, Somaliland  
- **Time range:** 2021 → 2025  
- **Frequency:** Daily  

### Variables
- `temp_max` — daily maximum temperature (°C)  
- `temp_min`  
- `precipitation`  
- `wind_speed_max`  

The dataset was rebuilt programmatically using the Open-Meteo **archive endpoint**, ensuring:

- reproducibility  
- continuous daily indexing  
- explicit handling of missing observations  

---

## 🧠 Forecasting Task (V1)

**Objective:**  
Predict **tomorrow’s maximum temperature** using only information available **up to today**.

- **Horizon:** 1 day ahead  
- **Target variable:** `temp_max`  
- **Evaluation style:** Walk-forward (rolling) forecasting  

This setup simulates **real-world deployment**, not a one-off prediction.

---

## 🧪 Methodology

### Baseline-First Philosophy

The primary model is a **naive persistence baseline**:

This baseline establishes the minimum performance bar that any statistical or machine-learning model must beat to justify its complexity.

---

### Walk-Forward Evaluation (2025)

Instead of forecasting once, the system:

- steps through **each day of 2025**
- treats that day as “today”
- predicts the next day
- compares the prediction with the actual observed value

This produces **364 real forecasts**, forming a complete forecast history and avoiding:

- data leakage  
- hindsight bias  
- misleading evaluation  

---

## 📈 Results

### Naive Walk-Forward Performance (2025)

| Metric | Value |
|------|------:|
| MAE | **≈ 0.98 °C** |
| RMSE | **≈ 1.26 °C** |
| Days evaluated | 364 |

### Key Observations
- Most daily errors are **below ~1°C**
- Larger errors occur during **abrupt weather transitions**
- Errors are **unbiased and unsystematic**

More complex statistical and ML approaches were explored, but for this specific task they did **not** consistently outperform the naive baseline.

---

## 🌍 Interpretation

Hargeisa’s climate exhibits:

- strong day-to-day temperature persistence  
- low short-term volatility  
- smooth seasonal transitions  

In such regimes, **yesterday’s temperature is often the strongest predictor of tomorrow’s**, and additional model complexity does not necessarily add predictive signal.

This is a **data-driven conclusion**, not a tooling limitation.

---

## 🖥️ Interactive Dashboard (V1)

The deployed Streamlit dashboard allows **as-of inspection** of historical forecasts:

- Select any date in **2025**
- View the forecast that would have been produced on that day
- Compare it against the actual observed temperature
- Inspect the forecast error and recent 14-day context

This design enables transparent, auditable evaluation of forecasting performance.

🔗 **Live Dashboard:**  
https://somaliland-weather-forecast-mgjhspkx32dyiqbyzwkhmy.streamlit.app/

---

## 🧭 Future Work

Planned extensions focus on **where forecasting models are more likely to add value**:

### V2 — Hourly Forecasting
- Higher-frequency (hourly) data
- 24–72 hour horizons
- Stronger temporal patterns and seasonality
- Statistical and ML models evaluated against robust baselines

### V3 — Multi-City Somaliland Forecasting
- Extend beyond Hargeisa (e.g. Berbera, Borama, Erigavo)
- Shared models across cities
- City-level comparison and uncertainty analysis

These extensions target richer regimes where complexity can be justified by improved performance.

---

## 🧠 Key Takeaway

> **In time-series forecasting, correctness beats complexity.  
> The best model is the one the data can support.**


