# 23CSE301 Machine Learning : Capstone Project

End-to-end pipelines for **Regression**, **Classification**, and **Clustering** (B.Tech CSE, Academic Year 2026–27).

---
# Regression

## What the regression path does

The notebook answers one question:

> Given pickup time, pickup location, dropoff location, passenger count, vendor, and the store-and-forward flag, **how many seconds will an NYC yellow-cab trip last?**

It does **not** use `dropoff_datetime`. Duration is dropoff time minus pickup time, so that column would leak the answer. It also drops `id`, which is only a trip label.

The same cleaned, encoded, scaled table is sent to **all ten required algorithms**. They are scored on the **same test trips**. Results are compared in one table (R², RMSE, MAE). The two best official models get 5-fold cross-validated R². A manual tester lets you type in a trip. A final cluster writes **`results/regression_report.pdf`** with the plots and metrics.

---

## Repository layout

```
.
├── README.md
├── requirements.txt
├── data/
│   └── nyc_taxi_trip_duration.csv    # 352,000 rows, 45 MiB (downsized from 160MB and 1.5 million rows to comply with GitHub filesize limits)
├── notebooks/
│   └── regression.ipynb              # Review 1 regression track
├── results/                          # created on first notebook run
│   ├── figures/                      # PNG copies of every plot
│   └── regression_report.pdf         # packed report
├── models/                           # optional saved .pkl files later
└── app/                              # optional GUI (Review 2 bonus) (not implemented yet)
```

---

## Dataset

| | |
|---|---|
| File | `data/nyc_taxi_trip_duration.csv` |
| Rows | **352,000** (reproducible random sample of the original 1,458,644-row Kaggle NYC taxi table, `random_state=42`, sized to **45 MiB** so GitHub accepts it under the 50 MiB warning and 100 MiB hard limit) |
| Period | 1 January 2016 – 30 June 2016 |
| Target | `trip_duration` (seconds) |
| Raw columns | `id`, `vendor_id`, `pickup_datetime`, `dropoff_datetime`, `passenger_count`, `pickup_longitude`, `pickup_latitude`, `dropoff_longitude`, `dropoff_latitude`, `store_and_fwd_flag`, `trip_duration` |

There are **no missing values**. The problems are impossible durations, out-of-city GPS points, and passenger counts of 0 or 7+.

---

## Environment setup

Python 3.9+ on macOS (Apple Silicon). From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

| Package | Role |
|---|---|
| pandas, numpy | Tables and arrays |
| matplotlib, seaborn | Plots (colorblind palette) |
| scikit-learn | Split, encode, scale, all 10 models, GridSearch, CV |
| joblib | Optional model save |

---

## How the notebook is clustered

Run the clusters **in order**. Each one consumes the table from the one above.

### Cluster A : Setup
Imports, `random_state=42`, paths, and `FAST_DEV`. Creates `results/` and `results/figures/`.

**Switch you may change**

```python
FAST_DEV = False          # True = 120k-row practice run (~2 min)
WORKING_SAMPLE_SIZE = 120_000
```

Leave `FAST_DEV = False` for the submitted run so linear / tree / boosting models see every cleaned training row.

### Cluster B : Problem and data audit
Loads **only** `data/nyc_taxi_trip_duration.csv`. Prints shape, dtypes, missing counts, duplicate checks, vendor / passenger / flag counts, and the target distribution (rubric A1).

### Cluster C : EDA
Plots a 25,000-row sample of the **raw** table so drawing stays fast; printed statistics still use all 352,000 rows.

You get:

- Target histogram (raw seconds and log1p)
- Passenger / vendor / hour / day-of-week counts
- Pickup and dropoff maps
- Distance vs duration and hour vs duration
- Correlation heatmap of raw numerics

Each figure is followed by a short “how to read this” note (rubric A2 + A3). Every figure is also saved under `results/figures/`.

### Cluster D : Data cleaning
Rule-based, with a before/after row table (rubric B1):

| Rule | Reason |
|---|---|
| Drop duplicates | Safety (none in this file) |
| Drop `id` | Not a predictor |
| Drop `dropoff_datetime` | Target leakage |
| NYC box on pickup **and** dropoff | GPS errors |
| `passenger_count` in 1–6 | Invalid occupancy |
| `trip_duration` in 60–7200 s | Cancelled / multi-hour junk |

IQR trimming is **not** applied on top of the 2-hour cap, so real airport runs stay in.

### Cluster E : Feature engineering
Built only from information available at pickup (rubric B3):

| Feature | Why |
|---|---|
| `trip_distance_km` (haversine) | Main physical driver |
| `manhattan_distance_km` | NYC street grid |
| `bearing_deg` | Direction (airports vs downtown) |
| `pickup_hour`, `dayofweek`, `month` | Congestion calendar |
| `is_weekend`, `is_rush_hour` | Same distance, worse time in peak |

`speed = distance / duration` is **never** created (that uses the target). After this cluster, distance correlates ~0.7+ with duration.

### Cluster F : Split, encode, scale
- 80/20 split, `random_state=42`
- Target binned into 10 quantiles and used to **stratify** the split
- One-hot: `vendor_id`, `store_and_fwd_flag`
- `StandardScaler` on numerics
- **Fit on train only**, transform train and test (rubric B2)
- Shared evaluation set capped at 50,000 test rows so SVR/KNN prediction stays tractable — **the same 50k for every model**

### Cluster G : Ten models (each fitted separately)

| # | Algorithm | Notes |
|---|---|---|
| 1 | Linear Regression | Baseline; interpret scaled coefficients |
| 2 | Ridge Regression | L2; handles collinear distances |
| 3 | Lasso Regression | L1; watch how many weights become 0 |
| 4 | ElasticNet Regression | L1 + L2 |
| 5 | Polynomial Regression | `PolynomialFeatures` degree 1 vs 2, then linear |
| 6 | Decision Tree Regression | Depth cap + feature importance |
| 7 | Random Forest Regression | Ensemble of trees |
| 8 | Gradient Boosting Regression | sklearn `HistGradientBoostingRegressor` (same family, runnable at this scale) |
| 9 | SVR Regression | RBF + scaled target; trained on 12k rows |
| 10 | KNN Regression | k = 15; trained on 40k rows |

A mean baseline (always predict the training average) is stored first so R² = 0 has a face.

### Cluster H : Compare, tune, check
- One ranked table of R² / RMSE / MAE (rubric C2)
- `GridSearchCV` on Ridge `alpha`
- `RandomizedSearchCV` on Random Forest, then refit on full train (rubric C3)
- Predicted vs actual + residuals for the best model; forest feature importance (rubric C4)
- 5-fold CV R² for the two best **official** models (training data only)

### Cluster I : Manual tester
Edit the `manual_trip` dictionary in that cell (coordinates, timestamp, passenger count, vendor, flag), then re-run **that cell**. The trip goes through the same `engineer_features` → already-fitted `preprocess.transform` path as the CSV. You get seconds and minutes from the best model, plus a comparison across every fitted model.

Starter values are real-looking Manhattan coordinates, not zeros. A weekday 17:00 trip should predict **longer** than a similar-distance Sunday 01:00 trip.

### Cluster J — PDF report
Writes **`results/regression_report.pdf`**, including:

- Cover page (row counts, best model, FAST_DEV flag)
- Cleaning table
- Full metrics table
- 5-fold CV table
- Manual-tester predictions
- Every plot saved during EDA / models / diagnostics

---

## Metrics 

| Metric | Meaning here |
|---|---|
| **R²** | Fraction of duration variance explained. 0 = no better than predicting the mean. |
| **RMSE** | Typical size of the error, in seconds, extra-punishing large misses. Divide by 60 to talk in minutes. |
| **MAE** | Average absolute miss in seconds; calmer about the remaining long trips. |
| **5-fold CV R²** | Stability on the training split for the two best official models. |

---

## What we already measured on a 120k-row dry run

These numbers will move a little on the full cleaned table (`FAST_DEV = False`), but the **order** should stay similar:

| Model | Test R² (approx.) |
|---|---|
| Gradient Boosting | 0.79 |
| Random Forest | 0.78 |
| Decision Tree | 0.74 |
| Polynomial (degree 2) | 0.70 |
| KNN (subset) | 0.70 |
| Linear / Ridge / Lasso | 0.62 |
| Mean baseline | 0.00 |

Distance was the top feature. Linear models split credit between haversine and Manhattan distance (collinearity). That is expected.

---

## Leakage and fairness

- **`dropoff_datetime` is out.** Using it is equivalent to giving the model the answer.
- **Scaler fit on train only.** Fitting on the full file is a mark deduction.
- **SVR and KNN see fewer training rows.** The leaderboard has a `Train rows` column so you do not pretend otherwise.
- **Same test trips** for every algorithm.

---

## Classification and clustering

Those tracks are Review 2 (`notebooks/classification.ipynb`, `notebooks/clustering.ipynb`). They are not in this folder yet.

---

## Academic note

Course guidelines allow generative AI for scaffolding, not for invented interpretation. AI agents were employed to document the code **only**.
> Cursor agent was used in commit `3082033` to fix git pipeline errors.