import pandas as pd

output_file = "C:/intervals-agent/race_analysis.csv"

try:
    df = pd.read_csv(output_file)

    # Define the names of the races to pool
    pooled_race_names = [
        'Hitachinaka City Cycling',
        'Hitachinaka criterium',
        'Kohoku Ward Cycling',
        'Kohoku Ward Road Cycling',
        'Nissan criterium',
        'Shimotsuma City Cycling',
        'Sodegaura City Road Cycling'
    ]

    # Filter the DataFrame for these pooled races, excluding any incidents
    pooled_races = df[df['Name'].isin(pooled_race_names) & df['Incident'].isnull()].copy()

    if not pooled_races.empty:
        print("\n--- Pooled Races Analysis ---")
        print(f"Found {len(pooled_races)} pooled races for analysis.\n")

        # Normalize metrics for scoring
        # Handle cases where min/max might be the same to avoid division by zero
        pooled_races['Normalized Speed'] = (pooled_races['Average Speed (km/h)'] - pooled_races['Average Speed (km/h)'].min()) / (pooled_races['Average Speed (km/h)'].max() - pooled_races['Average Speed (km/h)'].min()) if pooled_races['Average Speed (km/h)'].max() != pooled_races['Average Speed (km/h)'].min() else 0
        pooled_races['Normalized Efficiency Factor'] = (pooled_races['Efficiency Factor'] - pooled_races['Efficiency Factor'].min()) / (pooled_races['Efficiency Factor'].max() - pooled_races['Efficiency Factor'].min()) if pooled_races['Efficiency Factor'].max() != pooled_races['Efficiency Factor'].min() else 0

        # For Kilojoules/Hour, lower is better, so we invert the normalization
        pooled_races['Normalized Kilojoules/Hour'] = 1 - ((pooled_races['Kilojoules/Hour'] - pooled_races['Kilojoules/Hour'].min()) / (pooled_races['Kilojoules/Hour'].max() - pooled_races['Kilojoules/Hour'].min())) if pooled_races['Kilojoules/Hour'].max() != pooled_races['Kilojoules/Hour'].min() else 0

        # Normalize Power/Weight (W/kg) - higher is better
        # Fill NaN with 0 before normalization to ensure it doesn't affect min/max and score
        pw_min = pooled_races['Power/Weight (W/kg)'].min()
        pw_max = pooled_races['Power/Weight (W/kg)'].max()
        pooled_races['Normalized Power/Weight'] = (pooled_races['Power/Weight (W/kg)'].fillna(0) - pw_min) / (pw_max - pw_min) if pw_max != pw_min else 0

        # Simple performance score: sum of normalized metrics
        pooled_races['Performance Score'] = pooled_races['Normalized Speed'] + pooled_races['Normalized Efficiency Factor'] + pooled_races['Normalized Kilojoules/Hour'] + pooled_races['Normalized Power/Weight']

        # Sort by performance score (highest first)
        pooled_races_sorted = pooled_races.sort_values(by='Performance Score', ascending=False)

        # Display relevant columns for analysis
        display_cols = [
            'Date', 'Name', 'Average Speed (km/h)', 'Kilojoules', 'Kilojoules/Hour', 'Efficiency Factor', 'Performance Score',
            'Avg Resting HR (7-day pre-race)', 'Avg HRV (7-day pre-race)', 'Avg Sleep (hours, 7-day pre-race)',
            'Avg Resting HR (14-day pre-race)', 'Avg HRV (14-day pre-race)', 'Avg Sleep (hours, 14-day pre-race)',
            'Fitness (CTL, day pre-race)', 'Fatigue (ATL, day pre-race)', 'Form (Ramp Rate, day pre-race)',
            'Max HR (in-race)', 'Variability', 'Power/HR', 'Power/Weight (W/kg)',
            'Peak Core Temp (C)', 'Time Over 38C (s)'
        ]

        # Filter out columns that don't exist in the DataFrame
        existing_display_cols = [col for col in display_cols if col in pooled_races_sorted.columns]

        print(pooled_races_sorted[existing_display_cols].to_string())

    else:
        print("No pooled races found in the data.")

except FileNotFoundError:
    print(f"Error: The file {output_file} was not found. Please ensure it has been generated.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")