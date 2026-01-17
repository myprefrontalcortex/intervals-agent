import pandas as pd

output_file = "C:/intervals-agent/race_analysis.csv"

try:
    df = pd.read_csv(output_file)

    # Define the Activity IDs for good and bad pooled races
    good_pooled_ids = ['i20311937', 'i18041365', 'i50308973']
    bad_pooled_ids = ['i20340229']

    # Filter the DataFrame for these specific races
    selected_pooled_races = df[df['Activity ID'].isin(good_pooled_ids + bad_pooled_ids)].copy()

    if not selected_pooled_races.empty:
        print("\n--- Pre-Race Wellness and PMC Data for Selected Pooled Races ---")

        # Display relevant columns for comparison
        display_cols = [
            'Date', 'Name', 'Average Speed (km/h)', 'Kilojoules/Hour', 'Efficiency Factor', 'Performance Score',
            'Avg Resting HR (7-day pre-race)', 'Avg HRV (7-day pre-race)', 'Avg Sleep (hours, 7-day pre-race)',
            'Avg Resting HR (14-day pre-race)', 'Avg HRV (14-day pre-race)', 'Avg Sleep (hours, 14-day pre-race)',
            'Fitness (CTL, day pre-race)', 'Fatigue (ATL, day pre-race)', 'Form (Ramp Rate, day pre-race)',
            'Max HR (in-race)', 'Variability', 'Power/HR', 'Power/Weight (W/kg)',
            'Peak Core Temp (C)', 'Time Over 38C (s)'
        ]

        # Filter out columns that don't exist in the DataFrame
        existing_display_cols = [col for col in display_cols if col in selected_pooled_races.columns]

        # Sort by date for easier comparison
        selected_pooled_races_sorted = selected_pooled_races.sort_values(by='Date', ascending=True)

        print(selected_pooled_races_sorted[existing_display_cols].to_string())

    else:
        print("No selected pooled races found in the data.")

except FileNotFoundError:
    print(f"Error: The file {output_file} was not found. Please ensure it has been generated.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
