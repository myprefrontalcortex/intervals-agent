import pandas as pd

output_file = "C:/intervals-agent/race_analysis.csv"

try:
    df = pd.read_csv(output_file)

    # Define activities to exclude by Activity ID (e.g., due to puncture)
    excluded_activity_ids = ['i83150165'] # Only exclude the puncture race

    # Filter out excluded activities
    df_filtered = df[~df['Activity ID'].isin(excluded_activity_ids)].copy()

    if not df_filtered.empty:
        # Ensure Performance Score is calculated consistently (it should be in race_analysis.csv now)
        # If not, this section would recalculate it, but it should be loaded directly.
        # For safety, let's ensure the column exists and is numeric.
        if 'Performance Score' not in df_filtered.columns:
            print("Error: 'Performance Score' column not found. Please ensure main.py calculates it.")
            exit()
        df_filtered['Performance Score'] = pd.to_numeric(df_filtered['Performance Score'], errors='coerce')

        # Define metrics to calculate correlation for
        metrics_for_correlation = [
            'Fitness (CTL, day pre-race)',
            'Fatigue (ATL, day pre-race)',
            'Form (Ramp Rate, day pre-race)',
            'Avg Resting HR (7-day pre-race)',
            'Avg HRV (7-day pre-race)',
            'Avg Sleep (hours, 7-day pre-race)',
            'Power/Weight (W/kg)'
        ]

        print("\n--- Pearson Correlation Coefficients with Performance Score ---")
        for metric in metrics_for_correlation:
            # Drop rows with NaN in either metric or Performance Score for correlation calculation
            temp_df = df_filtered[[metric, 'Performance Score']].dropna()
            if not temp_df.empty and len(temp_df) > 1: # Need at least 2 points for correlation
                correlation = temp_df[metric].corr(temp_df['Performance Score'])
                print(f"{metric:<40}: {correlation:.4f}")
            else:
                print(f"{metric:<40}: Not enough data for correlation (or all NaN)")

    else:
        print("No races found for correlation analysis after exclusion.")

except FileNotFoundError:
    print(f"Error: The file {output_file} was not found. Please ensure it has been generated.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")