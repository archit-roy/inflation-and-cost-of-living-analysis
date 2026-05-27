import pandas as pd
import numpy as np
import sqlite3

np.random.seed(7)

ACTUAL_CPI = {
    "2019-01": 139.0, "2019-02": 138.8, "2019-03": 139.7, "2019-04": 140.9,
    "2019-05": 141.0, "2019-06": 142.4, "2019-07": 143.2, "2019-08": 143.7,
    "2019-09": 144.2, "2019-10": 146.2, "2019-11": 148.2, "2019-12": 150.7,
    "2020-01": 153.3, "2020-02": 152.7, "2020-03": 151.7, "2020-04": 152.5,
    "2020-05": 152.3, "2020-06": 153.8, "2020-07": 155.1, "2020-08": 156.1,
    "2020-09": 156.9, "2020-10": 157.7, "2020-11": 157.3, "2020-12": 158.5,
    "2021-01": 157.8, "2021-02": 157.0, "2021-03": 157.6, "2021-04": 159.4,
    "2021-05": 160.5, "2021-06": 161.8, "2021-07": 162.0, "2021-08": 162.9,
    "2021-09": 163.6, "2021-10": 163.8, "2021-11": 164.5, "2021-12": 166.7,
    "2022-01": 167.2, "2022-02": 167.7, "2022-03": 170.1, "2022-04": 173.9,
    "2022-05": 176.4, "2022-06": 176.8, "2022-07": 176.5, "2022-08": 176.5,
    "2022-09": 177.6, "2022-10": 178.2, "2022-11": 179.6, "2022-12": 179.9,
    "2023-01": 180.5, "2023-02": 181.6, "2023-03": 181.4, "2023-04": 183.5,
    "2023-05": 183.5, "2023-06": 183.5, "2023-07": 188.4, "2023-08": 188.0,
    "2023-09": 186.8, "2023-10": 185.6, "2023-11": 186.1, "2023-12": 184.4,
    "2024-01": 186.7, "2024-02": 186.9, "2024-03": 186.2, "2024-04": 187.7,
    "2024-05": 186.4, "2024-06": 186.1, "2024-07": 189.4, "2024-08": 188.3,
    "2024-09": 185.6, "2024-10": 189.7, "2024-11": 191.0, "2024-12": 189.5,
    "2025-01": 191.2, "2025-02": 190.8, "2025-03": 191.5, "2025-04": 193.1,
    "2025-05": 192.8, "2025-06": 193.4, "2025-07": 195.2, "2025-08": 194.9,
    "2025-09": 193.8, "2025-10": 194.5, "2025-11": 195.3, "2025-12": 196.0,
}

def build_data():
    series = pd.Series(ACTUAL_CPI)
    series.index = pd.to_datetime(series.index)
    series = series.sort_index()

    rows = []
    for date, gen_val in series.items():
        yr = date.year; mo = date.month
        food_shock = 0
        if yr == 2020 and mo in [4,5,6]: food_shock = 3.5
        if yr == 2022 and mo in [4,5,6,7]: food_shock = 4.2
        if yr == 2023 and mo == 7: food_shock = 9.0
        if yr == 2023 and mo == 8: food_shock = 7.5
        fuel_shock = 0
        if yr == 2021 and mo >= 6: fuel_shock = 2.5
        if yr == 2022 and mo in [4,5,6,7,8,9]: fuel_shock = 7.0
        if yr == 2022 and mo >= 10: fuel_shock = 3.0

        rows.append({
            "date": date,
            "cpi_general": round(gen_val, 1),
            "cpi_food": round(gen_val * 1.02 + food_shock + np.random.normal(0, 0.4), 1),
            "cpi_fuel": round(gen_val * 0.98 + fuel_shock + np.random.normal(0, 0.6), 1),
            "cpi_housing": round(gen_val * 0.95 + np.random.normal(0, 0.3), 1),
            "cpi_clothing": round(gen_val * 0.92 + np.random.normal(0, 0.2), 1),
            "cpi_misc": round(gen_val * 1.01 + np.random.normal(0, 0.5), 1),
        })

    df = pd.DataFrame(rows)

    for col in ["cpi_general","cpi_food","cpi_fuel","cpi_housing","cpi_clothing","cpi_misc"]:
        lag = df[col].shift(12)
        df[f"{col}_yoy_pct"] = ((df[col] - lag) / lag * 100).round(2)

    base = df[df["date"] == pd.Timestamp("2019-01-01")]["cpi_general"].values[0]
    df["purchasing_power_100"] = (base / df["cpi_general"] * 100).round(2)
    df["real_erosion_pct"] = ((df["cpi_general"] - base) / base * 100).round(2)

    df.to_csv("cpi_data.csv", index=False)
    conn = sqlite3.connect("inflation.db")
    df.to_sql("cpi_monthly", conn, if_exists="replace", index=False)
    conn.close()

    df_full = df.dropna(subset=["cpi_general_yoy_pct"])
    print(f"Generated {len(df)} monthly rows (2019–2025)")
    print(f"\n=== KEY FINDINGS ===")
    print(f"Peak general inflation : {df_full['cpi_general_yoy_pct'].max():.2f}% ({df_full.loc[df_full['cpi_general_yoy_pct'].idxmax(),'date'].strftime('%b %Y')})")
    print(f"Peak food inflation    : {df_full['cpi_food_yoy_pct'].max():.2f}% ({df_full.loc[df_full['cpi_food_yoy_pct'].idxmax(),'date'].strftime('%b %Y')})")
    print(f"Peak fuel inflation    : {df_full['cpi_fuel_yoy_pct'].max():.2f}% ({df_full.loc[df_full['cpi_fuel_yoy_pct'].idxmax(),'date'].strftime('%b %Y')})")
    print(f"Total CPI rise         : +{df['real_erosion_pct'].iloc[-1]:.1f}% (Jan 2019 – Dec 2025)")
    print(f"Purchasing power of ₹100 (Jan 2019) by Dec 2025: ₹{df['purchasing_power_100'].iloc[-1]:.1f}")
    print(f"Months above RBI 6% band: {(df_full['cpi_general_yoy_pct'] > 6).sum()}")
    return df

if __name__ == "__main__":
    build_data()