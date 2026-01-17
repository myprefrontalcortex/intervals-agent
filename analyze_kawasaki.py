import pandas as pd

output_file = "C:/intervals-agent/race_analysis.csv"

try:
    df = pd.read_csv(output_file)

    # Define activities to exclude by Activity ID (e.g., due to puncture)
    # This list will be maintained by the agent based on user input.
    excluded_activity_ids = ['i83150165'] # Exclude the 2025-06-15 Kawasaki race due to puncture

    kawasaki_races = df[df['Name'].str.contains('Kawasaki', na=False) & ~df['Activity ID'].isin(excluded_activity_ids)].copy()

    if not kawasaki_races.empty:
        print("\n--- Kawasaki Races Analysis (Excluding specified activities) ---")
        print(f"Found {len(kawasaki_races)} Kawasaki races for analysis.\n")

        # Normalize speed and kilojoules for scoring
        # Avoid division by zero if all values are the same
        kawasaki_races['Normalized Speed'] = (kawasaki_races['Average Speed (km/h)'] - kawasaki_races['Average Speed (km/h)'].min()) / (kawasaki_races['Average Speed (km/h)'].max() - kawasaki_races['Average Speed (km/h)'].min()) if kawasaki_races['Average Speed (km/h)'].max() != kawasaki_races['Average Speed (km/h)'].min() else 0
        kawasaki_races['Normalized Kilojoules'] = (kawasaki_races['Kilojoules'] - kawasaki_races['Kilojoules'].min()) / (kawasaki_races['Kilojoules'].max() - kawasaki_races['Kilojoules'].min()) if kawasaki_races['Kilojoules'].max() != kawasaki_races['Kilojoules'].min() else 0

        # Simple performance score: sum of normalized speed and kilojoules
        kawasaki_races['Performance Score'] = kawasaki_races['Normalized Speed'] + kawasaki_races['Normalized Kilojoules']

        # Sort by performance score (highest first)
        kawasaki_races_sorted = kawasaki_races.sort_values(by='Performance Score', ascending=False)

        # Display relevant columns for analysis
        display_cols = [
            'Date', 'Name', 'Average Speed (km/h)', 'Kilojoules', 'Kilojoules/Hour', 'Performance Score',
            'Avg Resting HR (7-day pre-race)', 'Avg HRV (7-day pre-race)', 'Avg Sleep (hours, 7-day pre-race)',
            'Fitness (CTL, day pre-race)', 'Fatigue (ATL, day pre-race)', 'Form (Ramp Rate, day pre-race)',
            'Max HR (in-race)', 'Variability', 'Power/HR', 'Efficiency Factor', 'Power/Weight (W/kg)',
            'Peak Core Temp (C)', 'Time Over 38C (s)'
        ]

        # Filter out columns that don't exist in the DataFrame
        existing_display_cols = [col for col in display_cols if col in kawasaki_races_sorted.columns]

        print(kawasaki_races_sorted[existing_display_cols].to_string())

    else:
        print("No Kawasaki races found for analysis after exclusion.")

except FileNotFoundError:
    print(f"Error: The file {output_file} was not found. Please ensure it has been generated.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
