import pandas as pd
import numpy as np
import sqlite3

def load_data():
    conn = sqlite3.connect("inflation.db")
    df = pd.read_sql("SELECT * FROM cpi_monthly", conn)
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df

def compute_summary(df):
    df_full = df.dropna(subset=["cpi_general_yoy_pct"])

    summary = {
        "peak_general_inflation_pct": df_full["cpi_general_yoy_pct"].max().round(2),
        "peak_general_inflation_date": df_full.loc[df_full["cpi_general_yoy_pct"].idxmax(), "date"].strftime("%b %Y"),
        "peak_food_inflation_pct": df_full["cpi_food_yoy_pct"].max().round(2),
        "peak_food_inflation_date": df_full.loc[df_full["cpi_food_yoy_pct"].idxmax(), "date"].strftime("%b %Y"),
        "peak_fuel_inflation_pct": df_full["cpi_fuel_yoy_pct"].max().round(2),
        "peak_fuel_inflation_date": df_full.loc[df_full["cpi_fuel_yoy_pct"].idxmax(), "date"].strftime("%b %Y"),
        "total_cpi_rise_pct": df["real_erosion_pct"].iloc[-1].round(2),
        "purchasing_power_dec2025": df["purchasing_power_100"].iloc[-1].round(2),
        "months_above_6pct": int((df_full["cpi_general_yoy_pct"] > 6).sum()),
        "months_above_4pct": int((df_full["cpi_general_yoy_pct"] > 4).sum()),
    }
    return summary

def compute_phase_averages(df):
    phases = [
        ("Pre-COVID (2019)",        "2019-01-01", "2019-12-01"),
        ("COVID Shock (2020)",      "2020-01-01", "2020-12-01"),
        ("Recovery (2021)",         "2021-01-01", "2021-12-01"),
        ("Global Commodity (2022)", "2022-01-01", "2022-12-01"),
        ("Moderation (2023)",       "2023-01-01", "2023-12-01"),
        ("Stability (2024)",        "2024-01-01", "2024-12-01"),
        ("2025 YTD",                "2025-01-01", "2025-12-01"),
    ]
    rows = []
    for phase, start, end in phases:
        mask = (df["date"] >= start) & (df["date"] <= end)
        sub = df[mask].dropna(subset=["cpi_general_yoy_pct"])
        if len(sub) == 0:
            continue
        rows.append({
            "phase": phase,
            "avg_general_inflation": sub["cpi_general_yoy_pct"].mean().round(2),
            "avg_food_inflation": sub["cpi_food_yoy_pct"].mean().round(2),
            "avg_fuel_inflation": sub["cpi_fuel_yoy_pct"].mean().round(2),
            "months_above_6pct": int((sub["cpi_general_yoy_pct"] > 6).sum()),
        })
    return pd.DataFrame(rows)

def save_to_db(df, phases):
    conn = sqlite3.connect("inflation.db")
    df.to_sql("cpi_monthly", conn, if_exists="replace", index=False)
    phases.to_sql("phase_summary", conn, if_exists="replace", index=False)
    conn.close()

if __name__ == "__main__":
    df = load_data()
    summary = compute_summary(df)
    phases = compute_phase_averages(df)
    save_to_db(df, phases)

    print("\n=== INFLATION SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    print("\n=== PHASE AVERAGES ===")
    print(phases.to_string(index=False))

    phases.to_csv("phase_summary.csv", index=False)
    print("\nSaved phase_summary.csv")