import pandas as pd

output_file = "C:/intervals-agent/race_analysis.csv"

try:
    df = pd.read_csv(output_file)

    # Define the Activity IDs for good and bad races from both locations
    selected_race_ids = [
        'i52845545', # Good Kawasaki 2024-10-20
        'i42300375', # Good Kawasaki 2024-06-16
        'i19386996', # Bad Kawasaki 2022-06-19
        'i49131928', # Good Chichibu 2024-09-08
        'i23157401'  # Bad Chichibu 2023-09-03
    ]

    # Filter the DataFrame for these specific races
    selected_races = df[df['Activity ID'].isin(selected_race_ids)].copy()

    if not selected_races.empty:
        print("\n--- Pre-Race Wellness and PMC Data for Selected Good/Bad Races ---")

        # Display relevant columns for comparison, including 14-day data
        display_cols = [
            'Date', 'Name', 'Average Speed (km/h)', 'Kilojoules/Hour', 'Efficiency Factor',
            'Avg Resting HR (7-day pre-race)', 'Avg HRV (7-day pre-race)', 'Avg Sleep (hours, 7-day pre-race)',
            'Avg Resting HR (14-day pre-race)', 'Avg HRV (14-day pre-race)', 'Avg Sleep (hours, 14-day pre-race)',
            'Fitness (CTL, day pre-race)', 'Fatigue (ATL, day pre-race)', 'Form (Ramp Rate, day pre-race)',
            'Max HR (in-race)', 'Variability', 'Power/HR', 'Power/Weight (W/kg)',
            'Peak Core Temp (C)', 'Time Over 38C (s)'
        ]

        # Filter out columns that don't exist in the DataFrame
        existing_display_cols = [col for col in display_cols if col in selected_races.columns]

        # Sort by date for easier comparison
        selected_races_sorted = selected_races.sort_values(by='Date', ascending=True)

        print(selected_races_sorted[existing_display_cols].to_string())

    else:
        print("No selected races found in the data.")

except FileNotFoundError:
    print(f"Error: The file {output_file} was not found. Please ensure it has been generated.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
