"""
Xert Correlation Analyzer

Description:
    This script calculates the Pearson correlation coefficient between the custom
    'Performance Score' and various Xert metrics. It prints the correlation matrix
    and saves a heatmap visualization.

Usage:
    python scripts/calculate_xert_correlations.py

Output:
    Saves 'figures/Xert_Correlations.png' (if directory exists, otherwise local).
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Configuration ---
INPUT_FILE = 'race_analysis_with_xert.csv'
OUTPUT_DIR = 'figures'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please run merge_xert_data.py first.")
        return

    try:
        df = pd.read_csv(INPUT_FILE)
        
        # Filter for rows that have both Performance Score and Xert data
        df_analyzable = df.dropna(subset=['Performance Score', 'Xert_Max_Power'])
        
        if df_analyzable.empty:
            print("No matching data found for correlation analysis.")
            return

        print(f"Calculating correlations for {len(df_analyzable)} races with Xert data...")

        # Define metrics to correlate
        metrics = [
            'Performance Score',
            'Xert_Max_Power',
            'Xert_Avg_Power',
            'Xert_Max_HR',
            'Xert_Avg_HR',
            'Xert_Duration_Min'
        ]
        
        # Calculate correlation matrix
        corr_matrix = df_analyzable[metrics].corr()
        
        # Extract correlations with Performance Score
        perf_correlations = corr_matrix['Performance Score'].sort_values(ascending=False)
        
        print("\n--- Correlations with Performance Score ---")
        print(perf_correlations)
        
        # Generate a heatmap plot
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Correlation Matrix: Performance vs Xert Metrics')
        plt.tight_layout()
        
        # Determine output path
        output_path = 'Xert_Correlations.png'
        if os.path.exists(OUTPUT_DIR):
            output_path = os.path.join(OUTPUT_DIR, output_path)
            
        plt.savefig(output_path)
        print(f"\nSaved correlation heatmap to '{output_path}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
