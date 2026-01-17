1 # Intervals Agent: Cycling Race Performance Analysis
    2
    3 This project analyzes cycling race data to find correlations between pre-race wellness metrics and race performanc
      It uses data from `intervals.icu` and `Xert` to explore how factors like sleep, resting heart rate, and training
      load impact race outcomes.
    4
    5 ## Features
    6
    7 -   **Data Ingestion:** Imports race data and wellness metrics from CSV files.
    8 -   **Correlation Analysis:** Calculates and visualizes the correlation between various pre-race metrics (e.g.,
      Fitness, Fatigue, Form, Resting HR, HRV, Sleep) and a calculated "Performance Score".
    9 -   **Outlier Identification:** Identifies negative performance outliers to help pinpoint races where performance
      was significantly worse than expected.
   10 -   **Xert Integration:** Includes scripts to parse `.tcx` files from Xert, extract key metrics, and merge them wi
      the main race data for deeper analysis.
   11 -   **Visualization:** Generates correlation dashboards and scatter plots to visually represent the findings.
   12
   13 ## Getting Started
   14
   15 ### Prerequisites
   16
   17 -   Python 3.x
   18 -   Pip for package management
   19
   20 ### Installation
   21
   22 1.  Clone the repository (or download the source).
   23 2.  Install the required Python packages:
      pip install -r requirements.txt