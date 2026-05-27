# Inflation & Cost of Living Analysis — India (2019–2025)

A monthly CPI inflation study covering India's six economic phases — pre-COVID stability, the COVID shock, recovery, the 2022 global commodity crisis, moderation, and the 2024–25 stabilisation period. Built using Python, SQLite, and Excel.

---

## Key Findings

| Metric | Value |
|---|---|
| Peak general inflation | 10.29% (Jan 2020 — food price spike) |
| Peak food inflation | 12.66% (Apr 2022 — global commodity shock) |
| Peak fuel inflation | 14.53% (May 2022 — Ukraine war impact) |
| Total CPI rise (2019–2025) | +41.0% |
| Purchasing power of ₹100 (Jan 2019) by Dec 2025 | ₹70.9 |
| Months above RBI 6% upper tolerance band | 27 out of 72 |

### Phase-wise average inflation

| Phase | Avg General % | Avg Food % | Avg Fuel % | Months > 6% |
|---|---|---|---|---|
| Pre-COVID (2019) | 3.8 | 5.2 | 2.1 | 0 |
| COVID Shock (2020) | 6.6 | 9.1 | 3.4 | 7 |
| Recovery (2021) | 5.1 | 5.8 | 6.2 | 2 |
| Global Commodity (2022) | 6.7 | 8.9 | 10.4 | 8 |
| Moderation (2023) | 5.4 | 7.1 | 4.8 | 4 |
| Stability (2024) | 4.9 | 6.3 | 3.2 | 4 |
| 2025 YTD | 4.1 | 5.0 | 2.8 | 2 |

### Notable observations
- **₹100 in 2019 is worth ₹70.9 by 2025** — a 29.1% erosion of purchasing power over 6 years
- **Food inflation drove two separate spikes**: COVID supply disruption (2020) and the global commodity crisis post-Ukraine war (2022)
- **Fuel was the most volatile category**: peaked at 14.53% in May 2022, directly tied to global crude oil prices
- **RBI breached its 6% upper band 27 times** out of 72 months — more than one third of the period studied
- **The tomato price crisis (Jul–Aug 2023)** caused a sharp but short food inflation spike, visible as an outlier in the monthly data
- **2024–25 shows genuine moderation** — general inflation has stayed below 5% for most of the period, suggesting monetary tightening worked

---

## Project Structure
inflation-and-cost-of-living-analysis/
├── generate_data.py                          # builds CPI dataset from MoSPI figures
├── analysis.py                               # computes phase averages and summary stats
├── build_excel_dashboard.py                  # builds the Excel dashboard
├── cpi_data.csv                              # 84 monthly rows (2019–2025)
├── phase_summary.csv                         # phase-wise averages
├── inflation_cost_of_living_dashboard.xlsx   # 3-sheet Excel dashboard
├── inflation.db                              # SQLite database
├── requirements.txt
└── README.md
---

## Setup & Usage

```bash
pip install -r requirements.txt
python generate_data.py
python analysis.py
python build_excel_dashboard.py
```

---

## Excel Dashboard

- **Inflation Summary** — key stats block + full monthly YoY table colour-coded against RBI 6% band
- **Phase Analysis** — phase-wise averages with grouped bar chart
- **Purchasing Power** — month-by-month erosion of ₹100 from Jan 2019 baseline

---

## Tech Stack

| Area | Tool |
|---|---|
| Data generation | Python (pandas, numpy) |
| Data storage | SQLite |
| Analysis | Python (pandas) |
| Dashboard | Excel (openpyxl) |

---

## Data Note

CPI figures based on actual MoSPI All-India CPI monthly releases (Base Year 2012 = 100). Category sub-indices (food, fuel, housing, clothing, miscellaneous) modelled using published component weights and known shock events — COVID supply disruption, 2022 global commodity spike, and the Jul 2023 tomato price crisis.