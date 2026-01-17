import pandas as pd

output_file = "C:/intervals-agent/race_analysis.csv"

try:
    df = pd.read_csv(output_file)

    # Filter for Chichibu races
    chichibu_races = df[df['Name'].str.contains('Chichibu', na=False)].copy()

    if not chichibu_races.empty:
        print("\n--- Chichibu Races Analysis ---")
        print(f"Found {len(chichibu_races)} Chichibu races.\n")

        # Display overall race metrics for Chichibu races
        display_cols = [
            'Date', 'Name', 'Average Speed (km/h)', 'Kilojoules', 'Kilojoules/Hour',
            'Max HR (in-race)', 'Variability', 'Power/HR', 'Efficiency Factor',
            'Power/Weight (W/kg)', 'Peak Core Temp (C)', 'Time Over 38C (s)'
        ]

        # Filter out columns that don't exist in the DataFrame
        existing_display_cols = [col for col in display_cols if col in chichibu_races.columns]

        print(chichibu_races[existing_display_cols].to_string())

        print("\nSince lap data is not available, we will analyze overall race metrics for Chichibu.")
        print("Please review the metrics above and let me know how you would define 'good' and 'bad' performances for these races.")

    else:
        print("No Chichibu races found in the data.")

except FileNotFoundError:
    print(f"Error: The file {output_file} was not found. Please ensure it has been generated.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")