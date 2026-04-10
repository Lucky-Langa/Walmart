<div align="center">
  <img src="https://retailinsider.b-cdn.net/wp-content/uploads/2022/10/Walmart_Canada_Corp__Canada_s_newest_Walmart_Supercentre_opens_i.jpeg" alt="Walmart Supercentre" width="600" style="border-radius:12px; box-shadow:0 4px 30px rgba(0,0,0,0.5); backdrop-filter:blur(10px);"/>
</div>

<div align="center">

# 🛒 Walmart Sales Forecasting
### *A Comprehensive Time Series Analysis*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14-4B8BBE?style=for-the-badge)](https://www.statsmodels.org)
[![Tableau](https://img.shields.io/badge/Tableau-Dashboard-E97627?style=for-the-badge&logo=tableau&logoColor=white)](https://tableau.com)
[![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting)

*Decomposing the truth behind retail growth claims — one week at a time.*

</div>

---

<div align="center" style="background:rgba(255,255,255,0.05); border-radius:16px; box-shadow:0 4px 30px rgba(0,0,0,0.3); backdrop-filter:blur(12px); padding:20px;">



---

```
╔══════════════════════════════════════════════════════════════════╗
║                    PROJECT NAVIGATION                            ║
║                                                                  ║
║   01 · ASK ────────── Define the problem                         ║
║   02 · PREPARE ─────── Understand the data                       ║
║   03 · PROCESS ─────── Clean and engineer features               ║
║   04 · ANALYZE ─────── Decompose, test, and interpret            ║
║   05 · SHARE ───────── Communicate findings                      ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## `01` · ASK
> *Before touching the data, define exactly what you are trying to solve.*

### 🏢 Who Are the Stakeholders?

| Stakeholder | Role | What They Need |
|---|---|---|
| **Regional VP** | Claimed 18% sales growth | Validation or challenge of that claim |
| **Finance Director** | Oversees growth targets | Accurate baseline for financial planning |
| **Supply Chain Director** | Manages inventory | Reliable demand forecasts to prevent stockouts |
| **Forecasting Manager** | Owns prediction models | A defensible, production-ready forecasting methodology |

---

### 🎯 Business Objectives

- Determine whether Walmart's reported **18% sales growth** reflects genuine business performance or is inflated by seasonal effects
- Identify which **external factors** — fuel prices, unemployment, CPI, temperature — meaningfully influence weekly sales
- Build a **time series forecasting model** accurate enough to support quarterly inventory and staffing decisions
- Quantify **holiday demand surges** to enable data-driven safety stock planning

---

### 🔥 The Core Problem

Walmart's Regional VP presented an **18% sales growth** figure to the board. The Finance Director challenged it — arguing the number may be comparing seasonal peaks to seasonal troughs rather than measuring genuine business expansion.

At stake: if growth targets are set against an inflated baseline, procurement, staffing, and capital allocation decisions across **45 stores** will be built on a false foundation.

**The central questions this project answers:**

```
❶  Is the 18% growth figure real, or is seasonality doing the work?
❷  Which external economic signals genuinely move weekly sales?
❸  How accurately can we forecast the next 12 weeks of sales?
❹  How large are holiday demand surges, and are they consistent across store types?
```

---

## `02` · PREPARE
> *Know your data before you trust it.*

### 📍 Where Is the Data Located?

The dataset originates from the **Walmart Store Sales Forecasting** competition on Kaggle.

```
🔗 https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting
```

Three source files were combined into a single working dataset:

```
walmart-data/
│
├── train.csv        ← Weekly sales per store per department (421,570 rows)
├── features.csv     ← External features per store per week (temperature, fuel, CPI, unemployment, markdowns)
└── stores.csv       ← Store metadata (type: A/B/C, size in sq ft)
```

---

### 🗂️ How Is the Data Organised?

| File | Grain | Key Columns |
|---|---|---|
| `train.csv` | Store × Department × Week | Store, Dept, Date, Weekly_Sales, IsHoliday |
| `features.csv` | Store × Week | Temperature, Fuel_Price, CPI, Unemployment, MarkDown1-5 |
| `stores.csv` | Store | Type (A/B/C), Size |

**Date range:** February 2010 → October 2012 **(143 weeks)**
**Scope:** 45 stores · up to 99 departments per store · weekly frequency

Files were merged on `Store` and `Date` to create one unified analytical dataset:

```python
walmart_df = train.merge(features, on=['Store', 'Date'], how='left')
walmart_df = walmart_df.merge(stores, on='Store', how='left')
```

---

### ✅ Does the Data ROCCC?

| Criterion | Assessment |
|---|---|
| **R**eliable | ✅ Sourced directly from Walmart's internal transaction systems via a Kaggle competition |
| **O**riginal | ✅ Primary source data — not aggregated or reprocessed by a third party |
| **C**omprehensive | ⚠️ Covers 45 stores only — not a full national picture. MarkDown data absent pre-Nov 2011 |
| **C**urrent | ⚠️ Historical data from 2010–2012. Patterns may not reflect post-pandemic retail behaviour |
| **C**ited | ✅ Publicly documented Kaggle competition with known provenance |

---

### 🔐 Licensing, Privacy & Accessibility

- Dataset is publicly available under **Kaggle competition terms** for educational and portfolio use
- No personally identifiable information (PII) is present — data is aggregated at store-department-week level
- All analysis conducted in a local Python environment with no external data transmission

---

### 🔍 Data Integrity Verification

Missing values identified before any transformations:

```
MarkDown1       270,892 missing   ← Structural absence (pre-Nov 2011 promotions)
MarkDown2       310,793 missing   ← Structural absence
MarkDown3       284,667 missing   ← Structural absence
MarkDown4       286,859 missing   ← Structural absence
MarkDown5       270,138 missing   ← Structural absence
CPI                 585 missing   ← Recording gaps
Unemployment        585 missing   ← Recording gaps
Dept              1,755 missing   ← Co-missing with Weekly_Sales (useless rows)
Weekly_Sales      1,755 missing   ← Co-missing with Dept (useless rows)
IsHoliday               0 missing ✅
Temperature             0 missing ✅
Fuel_Price              0 missing ✅
```

---

## `03` · PROCESS
> *Clean data is not an accident — it is a series of deliberate decisions.*

### 🛠️ Tools & Why

| Tool | Purpose |
|---|---|
| **Python 3.11** | Core analysis language |
| **pandas** | Data manipulation and feature engineering |
| **statsmodels** | ADF/KPSS stationarity tests, seasonal decomposition, SARIMA |
| **seaborn / matplotlib** | Statistical visualisations |
| **Tableau** | Interactive business dashboard |
| **Jupyter Notebook** | Reproducible analytical workflow |

---

### 🧹 Cleaning Decisions

**Step 1 — Drop useless rows**
```python
# 1,755 rows where both Dept and Weekly_Sales are missing simultaneously
# These carry zero analytical value — dropping is correct
walmart_df = walmart_df.dropna(subset=['Dept', 'Weekly_Sales'])
```

**Step 2 — Fill MarkDowns with zero**
```python
# Absence of a markdown means no promotion occurred — not a recording error
# Filling with median would imply a promotion happened when it did not
markdown_cols = ["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]
walmart_df[markdown_cols] = walmart_df[markdown_cols].fillna(0)
```

**Step 3 — Fill continuous features with median per store**
```python
# Median is preferred over mean to resist outlier distortion
# Grouped by Store because regional baselines differ significantly
continuous_cols = ["CPI", "Unemployment"]
walmart_df[continuous_cols] = walmart_df.groupby("Store")[continuous_cols].transform(
    lambda x: x.fillna(x.median())
)
```

**Step 4 — Fill IsHoliday with mode per store**
```python
walmart_df["IsHoliday"] = walmart_df.groupby("Store")["IsHoliday"].transform(
    lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else x)
)
```

---

### ⚙️ Feature Engineering

**Rolling averages — grouped by Store AND Department**
```python
# Windows: 5w (momentum), 10w (quarter), 20w (half-year), 52w (same-week-last-year)
# Grouped to prevent cross-store contamination of rolling calculations
for window in [5, 10, 20, 52]:
    df[f'rolling_mean_{window}'] = (
        df.groupby(['Store', 'Dept'])['Weekly_Sales']
        .transform(lambda x: x.rolling(window=window).mean())
    )
```

**Date features extracted**
```
month · day · year · ISO week number · quarter · day of week (numeric)
```

> ⚠️ **Key design decision:** Two separate dataframes were maintained after feature engineering —
> `walmart_df_clean` (full date range, for decomposition and stationarity testing) and
> `walmart_df_model` (post-dropna, for machine learning). This prevents rolling window NaN
> removal from corrupting the decomposition analysis.

---

## `04` · ANALYZE
> *Let the data speak — then translate what it says.*

### 📉 Seasonal Decomposition — Multiplicative Model (Period = 52)

A multiplicative decomposition was chosen because seasonal fluctuations in retail data grow proportionally with the trend level — a store doing $2M per week will have proportionally larger holiday spikes than a store doing $500K.

---

#### 🔵 Observed
The raw aggregated weekly sales across all 45 stores sit consistently between **$47M and $50M** per week. Two dramatic spikes are visible — the **Thanksgiving and Christmas** periods of November 2010 and November 2011 — confirming that holiday seasons do not merely lift sales, they transform them entirely.

---

#### 🟡 Trend
After removing seasonal effects, the true underlying direction of the business emerges:

```
Feb 2010 → Early 2011  ──  📉 Declining  (masked by holiday spikes in raw data)
Early 2011 → Mid 2011  ──  ➡️  Flat
Mid 2011 → Oct 2012    ──  📈 Steadily rising
```

> The raw data masked the mid-2010 weakness entirely. Genuine underlying growth
> from start to finish is approximately **2–3%** — not 18%.

---

#### 🟢 Seasonality
The seasonal component revolves around **1.0** in a multiplicative model:

```
~1.6  →  Thanksgiving / Christmas weeks  →  sales 60% ABOVE trend
~1.0  →  Normal weeks                    →  no seasonal effect
~0.8  →  Post-holiday January weeks      →  sales 20% BELOW trend
```

This pattern repeats with **near-identical magnitude in both 2010 and 2011.** If genuine 18% growth had occurred, the 2011 spike would be noticeably larger than the 2010 spike. It is not — the calendar is producing the same effect on repeat.

---

#### 🔴 Residual
Residuals oscillate tightly between **0.95 and 1.05** — meaning the decomposition accounts for almost all variation in the data. Sharp spikes in mid-2010 through early 2011 represent weeks where something unexpected occurred that neither trend nor seasonality can explain, possibly one-off promotions or external disruptions. The relatively flat mid-2011 period indicates the business performed almost exactly as predicted with no unexplained surprises.

---

### 🧪 Stationarity Testing — ADF & KPSS

Both tests were run to cross-validate the stationarity conclusion:

| Test | Null Hypothesis | Result | Conclusion |
|---|---|---|---|
| **ADF** | Series is NOT stationary | p ≤ 0.05 → Reject H₀ | Evidence of stationarity |
| **KPSS** | Series IS stationary | p ≥ 0.05 → Fail to reject H₀ | Evidence of stationarity |

> ✅ Both tests agree — the aggregated weekly sales series is stationary after seasonal adjustment.

---

### 💡 Key Findings

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Raw Sales Growth Claimed    →   ~18%                          │
│   True Trend Growth Found     →   ~2–3%                         │
│   Explained by Seasonality    →   ~15 percentage points         │
│                                                                 │
│   Holiday Seasonal Multiplier →   ~1.6x (60% above trend)       │
│   Post-Holiday Suppression    →   ~0.8x (20% below trend)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## `05` · SHARE
> *A finding that cannot be communicated is a finding that cannot drive decisions.*
### 📊 Tableau Dashboard

The interactive dashboard covers six analytical lenses:

| # | Panel | Question Answered |
|---|---|---|
| 01 | **Total Weekly Sales Over Time** | What does the full sales timeline look like across all stores and all weeks? |
| 02 | **Average Sales by Week of Year** | Which weeks of the annual cycle consistently generate the most sales? |
| 03 | **Monthly Sales Distribution** | Which months drive the highest cumulative revenue? |
| 04 | **Total Revenue Per Year** | What is the true year-on-year revenue trajectory? |
| 05 | **CPI vs Unemployment Rate Over Time** | How did macroeconomic conditions evolve alongside sales during the analysis period? |
| 06 | **Sales by Store** | Which individual stores generate the most revenue and how do they compare? |

<div align="center">
  <img src="dashboard/WALMART DASHBOARD.png" alt="Walmart Sales Tableau Dashboard" width="900" style="border-radius:10px; box-shadow:0 4px 20px rgba(0,0,0,0.4);"/>
  <p><i>Interactive Tableau dashboard — Walmart Weekly Sales Analysis</i></p>
  <a href="https://public.tableau.com/app/profile/lucky.tshepiso.langa/viz/WalmartDashboard_17757664261780/WALMARTDASHBOARD">
    <img src="https://img.shields.io/badge/View%20Live%20Dashboard-Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white"/>
  </a>
</div>
--------------------------------------------------------

### 👥 Audience & Communication Approach

| Audience | Communication Style |
|---|---|
| **Board / Finance Director** | Business memo — plain language, lead with conclusion, quantify the claim |
| **Supply Chain Director** | Holiday uplift table — safety stock multipliers per store type per holiday |
| **Forecasting Manager** | Technical notebook — model diagnostics, residual analysis, MAPE comparisons |
| **Recruiters / Reviewers** | This README + annotated Jupyter notebooks on GitHub |

---

### 📁 Repository Structure

```
walmart-timeseries/
│
├── 📓 notebooks/
│   ├── task_01.ipynb
│
│── Scripts/
│   ├──  data_merging.py
├
├── 📊 dashboard/
|   └── walmartDashboard.png
│   └── walmart_sales_dashboard.twbx
│
├── 📄 data/
│   ├── train/ train.csv
│   ├── features/ features.csv
│   ├── stores.csv
│   └── walmart_combined.csv
│
├── 📝 reports/
│   └── business_memo.md
│
└── README.md
```

### 🔗 Live Links

| Resource | Link |
|---|---|
| **GitHub Repository** | [Lucky-Langa/Walmart](https://github.com/Lucky-Langa/Walmart) |
| **Tableau Dashboard** | [View Live Dashboard](https://public.tableau.com/app/profile/lucky.tshepiso.langa/viz/WalmartDashboard_17757664261780/WALMARTDASHBOARD) |

---

### 🚀 How to Reproduce This Analysis

```bash
# 1. Clone the repository
git clone https://github.com/Lucky-Langa/walmart-timeseries.git
cd walmart-timeseries

# 2. Activate virtual environment
.\env\Scripts\Activate.ps1      # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter
jupyter notebook
```

---

<div align="center">

---

*Built as part of an end-to-end Data Science portfolio.*
*Walmart Sales Dataset — Kaggle Competition*

**[⬆ Back to Top](#-walmart-sales-forecasting)**

</div>
