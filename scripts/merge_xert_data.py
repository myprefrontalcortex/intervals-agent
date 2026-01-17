"""
Xert Data Merger

Description:
    This script merges the processed Xert metrics ('xert_metrics.csv') into the main
    race analysis dataset ('race_analysis.csv').

    It handles data aggregation for days with multiple Xert files (taking Max Power,
    Sum Duration, etc.) and performs a left join on the 'Date' column.

Usage:
    python scripts/merge_xert_data.py

Output:
    Saves 'race_analysis_with_xert.csv' in the project root.
"""

import pandas as pd
import os

# --- Configuration ---
RACE_FILE = 'race_analysis.csv'
XERT_FILE = 'xert_metrics.csv'
OUTPUT_FILE = 'race_analysis_with_xert.csv'

def main():
    if not os.path.exists(RACE_FILE):
        print(f"Error: {RACE_FILE} not found. Please run main.py first.")
        return
    if not os.path.exists(XERT_FILE):
        print(f"Error: {XERT_FILE} not found. Please run analyze_xert_tcx.py first.")
        return

    print("Reading files...")
    df_race = pd.read_csv(RACE_FILE)
    df_xert = pd.read_csv(XERT_FILE)

    # Ensure Date columns are string type for reliable merging
    df_race['Date'] = df_race['Date'].astype(str)
    df_xert['Date'] = df_xert['Date'].astype(str)

    print("Aggregating Xert data by Date...")
    # Aggregation Strategy:
    # - Max Power/HR: Take the peak value seen in any file that day.
    # - Avg Power/HR: Take the mean of averages (approximation).
    # - Duration: Sum of all durations.
    df_xert_daily = df_xert.groupby('Date').agg({
        'Xert_Max_Power': 'max',
        'Xert_Avg_Power': 'mean',
        'Xert_Max_HR': 'max',
        'Xert_Avg_HR': 'mean',
        'Xert_Duration_Min': 'sum'
    }).reset_index()

    print("Merging data...")
    # Left join ensures we keep all races from the main analysis, adding Xert data only where available.
    df_merged = pd.merge(df_race, df_xert_daily, on='Date', how='left')

    # Save the merged file
    df_merged.to_csv(OUTPUT_FILE, index=False)
    
    # Validation stats
    total_races = len(df_race)
    matched_races = df_merged['Xert_Max_Power'].notna().sum()
    
    print(f"Successfully saved merged data to {OUTPUT_FILE}")
    print(f"Total Races: {total_races}")
    print(f"Races with matching Xert data: {matched_races}")
    
    if matched_races > 0:
        print("\nFirst 5 rows with matching Xert data:")
        print(df_merged[df_merged['Xert_Max_Power'].notna()].head()[['Date', 'Name', 'Performance Score', 'Xert_Max_Power', 'Xert_Duration_Min']])

if __name__ == "__main__":
    main()
