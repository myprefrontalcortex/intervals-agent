# 🚴 Intervals Agent
Cycling Race Performance Analysis & Wellness Correlation

This project bridges the gap between your daily wellness metrics and your actual race day performance. By aggregating data from Intervals.icu and Xert, this agent explores how physiological markers like HRV, sleep, and training load impact your race outcomes.

🚀 Features
- **Multi-Source Data Ingestion**: Seamlessly imports wellness metrics and race results from CSV exports.
- **Correlation Analysis**: Calculates the relationship between pre-race variables (Fitness, Fatigue, Form, Resting HR, HRV, Sleep) and race outcomes.
- **Xert Integration**: Includes specialized parsers for `.tcx` files to extract advanced power metrics and merge them with physiological data.
- **Outlier Identification**: Automatically flags "negative outliers" to help you analyze why certain races didn't go according to plan.
- **Visual Dashboards**: Generates publication-ready scatter plots and correlation heatmaps.

---

## ⚙️ How It Works

The project analyzes your performance by following a three-stage pipeline, turning raw data into actionable insights.

### Stage 1: Defining "Race Performance" with a Score

Instead of using a subjective metric like finishing place, the analysis starts by calculating a **"Performance Score"** for each race. This score normalizes your results, allowing for a more objective, apples-to-apples comparison between different events and courses.

### Stage 2: The Analysis Pipeline

The agent processes your data in a sequence to ensure everything is correctly aligned and analyzed.

1.  **Data Input**: The process begins by reading from two key CSV files:
    *   `race_analysis.csv`: Contains wellness and training load metrics (e.g., Resting HR, HRV, Sleep, Fitness/CTL, Fatigue/ATL).
    *   `race_analysis_with_xert.csv`: An enhanced version of the above, merged with detailed in-race power data extracted from Xert `.tcx` files.

2.  **Correlation Analysis**: This is the core of the project, where two different sets of data are correlated against your `Performance Score`:
    *   **Wellness & Training Metrics**: The scripts analyze metrics from the days leading up to a race. This includes values like `Fitness (CTL)`, `Fatigue (ATL)`, and, importantly, the **7-day average** for metrics like `Resting HR`, `HRV`, and `Sleep`. This averaging approach smooths out daily fluctuations to provide a more stable picture of your pre-race condition.
    *   **In-Race Power Metrics**: The agent also analyzes power data from *during* the race (e.g., `Xert_Avg_Power`, `Xert_Max_HR`) to see how those physical outputs correlate with the final performance score.

3.  **Outlier Identification**: A key feature is the ability to automatically flag races where you significantly underperformed based on the data. This provides a starting point to investigate what went wrong on those specific days—was it poor sleep, high fatigue, or something else?

### Stage 3: The Output (Visualizations)

The final step is to translate the numerical analysis into clear, easy-to-interpret visuals. The scripts generate the figures you've seen, which help tell the story of your data:
*   **Scatter Plots**: Show the raw relationship between a single metric (like 7-day average sleep) and your performance.
*   **Heatmap & Dashboard**: Provide a high-level summary of which factors have the strongest positive or negative correlation with your race results.

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+
- Pip (Python package manager)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/myprefrontalcortex/intervals-agent.git
    cd intervals-agent
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🤝 Contributing
If you find ways to improve the correlation algorithms or add support for more platforms (like TrainingPeaks or Strava), feel free to open a Pull Request.
