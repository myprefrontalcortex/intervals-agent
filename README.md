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

## 🧬 Data Provenance: How the CSVs are Made

For this analysis to be reproducible, it's critical to understand how the foundational datasets are created. This happens in a three-stage pipeline:

### **Step 1: Parsing Raw Power Data (`xert_metrics.csv`)**
*   **Script**: `scripts/analyze_xert_tcx.py`
*   **Input**: Raw `.tcx` files located in the `Xert/` directory.
*   **Process**:
    1.  The script scans the `Xert/` directory for all `.tcx` files.
    2.  It parses the XML structure of each file to extract every recorded power and heart rate data point.
    3.  For each file, it calculates summary statistics: Max/Average Power, Max/Average HR, and total duration.
*   **Output**: A new file, `xert_metrics.csv`, containing a clean summary of the power data for each individual ride file, organized by date.

### **Step 2: Fetching Race & Wellness Data (`race_analysis.csv`)**
*   **Script**: `main.py`
*   **Input**: A live connection to the **Intervals.icu API** (using credentials from your `.env` file).
*   **Process**:
    1.  It fetches your entire activity history and filters it, keeping only the activities flagged as a "Race".
    2.  For each race, it queries the API again to get your wellness data (calculating the **7-day and 14-day averages** for Sleep, HRV, and Resting HR) and your fitness data (CTL, ATL for the day before the race).
    3.  It calculates the custom **`Performance Score`** by normalizing and combining several in-race metrics (e.g., average speed, power-to-weight).
*   **Output**: The script saves `race_analysis.csv`, a file containing *only* your race events, now enriched with pre-race wellness data and the crucial `Performance Score`.

### **Step 3: Merging for the Final Dataset (`race_analysis_with_xert.csv`)**
*   **Script**: `scripts/merge_xert_data.py`
*   **Input**: The two files created above: `xert_metrics.csv` and `race_analysis.csv`.
*   **Process**:
    1.  It reads both files.
    2.  It intelligently merges them by matching the `Date` column, attaching the detailed power data from Xert to the corresponding race events from Intervals.icu.
*   **Output**: The script saves `race_analysis_with_xert.csv`. This is the final, master dataset that all plotting and analysis scripts use to generate the figures.

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