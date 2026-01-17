import pandas as pd

output_file = "C:/intervals-agent/race_analysis.csv"

try:
    df = pd.read_csv(output_file)

    # Define activities to exclude by Activity ID (e.g., due to puncture)
    excluded_activity_ids = ['i83150165'] # Exclude the 2025-06-15 Kawasaki race due to puncture

    # Filter out excluded activities
    df_filtered = df[~df['Activity ID'].isin(excluded_activity_ids)].copy()

    if not df_filtered.empty:
        # Calculate Performance Score for all filtered races
        # Normalize speed and kilojoules for scoring
        # Avoid division by zero if all values are the same
        df_filtered['Normalized Speed'] = (df_filtered['Average Speed (km/h)'] - df_filtered['Average Speed (km/h)'].min()) / (df_filtered['Average Speed (km/h)'].max() - df_filtered['Average Speed (km/h)'].min()) if df_filtered['Average Speed (km/h)'].max() != df_filtered['Average Speed (km/h)'].min() else 0
        df_filtered['Normalized Efficiency Factor'] = (df_filtered['Efficiency Factor'] - df_filtered['Efficiency Factor'].min()) / (df_filtered['Efficiency Factor'].max() - df_filtered['Efficiency Factor'].min()) if df_filtered['Efficiency Factor'].max() != df_filtered['Efficiency Factor'].min() else 0

        # For Kilojoules/Hour, lower is better, so we invert the normalization
        df_filtered['Normalized Kilojoules/Hour'] = 1 - ((df_filtered['Kilojoules/Hour'] - df_filtered['Kilojoules/Hour'].min()) / (df_filtered['Kilojoules/Hour'].max() - df_filtered['Kilojoules/Hour'].min())) if df_filtered['Kilojoules/Hour'].max() != df_filtered['Kilojoules/Hour'].min() else 0

        # Normalize Power/Weight (W/kg) - higher is better
        # Fill NaN with 0 before normalization to ensure it doesn't affect min/max and score
        pw_min = df_filtered['Power/Weight (W/kg)'].min()
        pw_max = df_filtered['Power/Weight (W/kg)'].max()
        df_filtered['Normalized Power/Weight'] = (df_filtered['Power/Weight (W/kg)'].fillna(0) - pw_min) / (pw_max - pw_min) if pw_max != pw_min else 0

        # Simple performance score: sum of normalized metrics
        df_filtered['Performance Score'] = df_filtered['Normalized Speed'] + df_filtered['Normalized Efficiency Factor'] + df_filtered['Normalized Kilojoules/Hour'] + df_filtered['Normalized Power/Weight']

        # Filter for negative performance scores
        negative_performance_races = df_filtered[df_filtered['Performance Score'] < 0].copy()

        if not negative_performance_races.empty:
            print("\n--- Races with Negative Performance Scores ---")
            # Display relevant columns for outlier identification
            display_cols = [
                'Activity ID', 'Date', 'Name', 'Performance Score',
                'Avg Resting HR (7-day pre-race)', 'Avg HRV (7-day pre-race)', 'Avg Sleep (hours, 7-day pre-race)',
                'Fitness (CTL, day pre-race)', 'Fatigue (ATL, day pre-race)', 'Form (Ramp Rate, day pre-race)',
                'Power/Weight (W/kg)'
            ]

            # Filter out columns that don't exist in the DataFrame
            existing_display_cols = [col for col in display_cols if col in negative_performance_races.columns]

            # Sort by Performance Score (lowest first)
            negative_performance_races_sorted = negative_performance_races.sort_values(by='Performance Score', ascending=True)

            print(negative_performance_races_sorted[existing_display_cols].to_string())

        else:
            print("No races found with negative performance scores.")

    else:
        print("No races found for analysis after initial exclusion.")

except FileNotFoundError:
    print(f"Error: The file {output_file} was not found. Please ensure it has been generated.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")