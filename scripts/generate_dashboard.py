"""
Dashboard Generator

Description:
    This script generates a visual dashboard (bar chart) visualizing the correlations
    between Xert physiological metrics and the calculated Race Performance Score.
    
    It highlights:
    - Strong Positive Correlations (Green)
    - Strong Negative Correlations (Red)
    - Neutral/Weak Correlations (Gray)

Usage:
    python scripts/generate_dashboard.py

Output:
    Saves 'xert_correlation_dashboard.jpg' in the 'figures/' directory.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
INPUT_FILE = 'race_analysis_with_xert.csv'
OUTPUT_DIR = 'figures'
OUTPUT_FILENAME = 'xert_correlation_dashboard.jpg'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please run merge_xert_data.py first.")
        return

    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        df = pd.read_csv(INPUT_FILE)
        
        # Filter for rows that have both Performance Score and Xert data
        # We need at least 2 points for a correlation
        df_analyzable = df.dropna(subset=['Performance Score', 'Xert_Max_Power'])
        
        if len(df_analyzable) < 2:
            print("Not enough matching data to calculate correlations.")
            return

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
        
        # Extract correlations with Performance Score, drop the score itself
        perf_correlations = corr_matrix['Performance Score'].drop('Performance Score').sort_values(ascending=False)
        
        # --- Create Dashboard Figure (Bar Chart) ---
        plt.figure(figsize=(10, 6))
        
        # Color logic: Strong Positive (>0.3), Strong Negative (<-0.3), Neutral
        colors = ['#2ecc71' if x > 0.3 else '#e74c3c' if x < -0.3 else '#95a5a6' for x in perf_correlations.values]
        
        ax = perf_correlations.plot(kind='bar', color=colors)
        
        plt.title('Correlation with Race Performance Score (Xert Metrics)', fontsize=14, pad=20)
        plt.ylabel('Correlation Coefficient (r)', fontsize=12)
        plt.xlabel('Metric', fontsize=12)
        plt.axhline(0, color='black', linewidth=0.8)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.ylim(-1, 1)
        
        # Add numeric labels on top of bars
        for i, v in enumerate(perf_correlations):
            y_pos = v + (0.05 if v > 0 else -0.1)
            ax.text(i, y_pos, f"{v:.2f}", ha='center', fontweight='bold')
            
        plt.tight_layout()
        
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
        plt.savefig(output_path, dpi=300, format='jpg')
        print(f"Dashboard figure saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
