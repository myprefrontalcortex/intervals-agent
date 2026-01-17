import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

output_file = "C:/intervals-agent/race_analysis.csv"
output_dir = "figures"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    df = pd.read_csv(output_file)

    # Define activities to exclude by Activity ID (e.g., due to puncture)
    excluded_activity_ids = ['i83150165'] # Only exclude the puncture race

    # Filter out excluded activities
    df_filtered = df[~df['Activity ID'].isin(excluded_activity_ids)].copy()

    if not df_filtered.empty:
        print("\n--- Data points being plotted (Activity ID, Performance Score) ---")
        print(df_filtered[['Activity ID', 'Performance Score']].to_string())

        # Define metrics to plot against Performance Score
        metrics_to_plot = [
            'Fitness (CTL, day pre-race)',
            'Fatigue (ATL, day pre-race)',
            'Form (Ramp Rate, day pre-race)',
            'Avg Resting HR (7-day pre-race)',
            'Avg HRV (7-day pre-race)',
            'Avg Sleep (hours, 7-day pre-race)',
            'Power/Weight (W/kg)'
        ]

        for metric in metrics_to_plot:
            plt.figure(figsize=(10, 6))
            plt.scatter(df_filtered[metric], df_filtered['Performance Score'])

            # Add trend line and correlation coefficient
            temp_df = df_filtered[[metric, 'Performance Score']].dropna()
            if not temp_df.empty and len(temp_df) > 1:
                # Calculate trend line
                z = np.polyfit(temp_df[metric], temp_df['Performance Score'], 1)
                p = np.poly1d(z)
                plt.plot(temp_df[metric], p(temp_df[metric]), "r--")

                # Calculate Pearson correlation coefficient
                correlation = temp_df[metric].corr(temp_df['Performance Score'])
                plt.text(0.05, 0.95, f'Correlation: {correlation:.2f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))

            plt.title(f'{metric} vs. Performance Score')
            plt.xlabel(metric)
            plt.ylabel('Performance Score')
            plt.grid(True)
            plt.tight_layout()
            
            # Construct filename and save in the 'figures' directory
            base_filename = f"{metric.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')}_vs_Performance_Score.png"
            plot_filename = os.path.join(output_dir, base_filename)
            
            plt.savefig(plot_filename)
            plt.close()
            print(f"Saved plot: {plot_filename}")

    else:
        print("No races found for plotting after exclusion.")

except FileNotFoundError:
    print(f"Error: The file {output_file} was not found. Please ensure it has been generated.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")