# 🌤️ Somaliland Weather Forecasting (V1)

**Daily Maximum Temperature Forecasting for Hargeisa using Walk-Forward Time Series Evaluation**

This repository presents a disciplined, baseline-first approach to time-series weather forecasting for **Hargeisa, Somaliland**.  
The project emphasizes **data integrity, proper evaluation, and honest conclusions**, rather than model complexity or hype.

An interactive Streamlit dashboard allows inspection of historical forecasts exactly as they would have been produced in real time.

---

## 🎯 Project Motivation

Many forecasting and ML portfolio projects:
- rely on a single prediction
- ignore proper backtesting
- overuse complex models without checking if the data supports them

This project intentionally takes a different path:

> **Start simple, evaluate rigorously, and only add complexity if it clearly improves performance.**

Hargeisa is an ideal case study due to its **stable semi-arid climate**, where daily temperature changes tend to be gradual and predictable.

---

## 📊 Dataset

### Source
- **Open-Meteo Weather API**
- Daily **observed / archive** weather data (not forecasts)

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

## 🧠 Forecasting Task

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

