# 🚴 Intervals Agent
Cycling Race Performance Analysis & Wellness Correlation
This project bridges the gap between your daily wellness metrics and your actual race day performance. By aggregating data from Intervals.icu and Xert, we can explore how physiological markers like HRV, sleep, and training load (CTL/TSB) impact your "Performance Score."

🚀 Features
Multi-Source Data Ingestion Seamlessly imports wellness metrics and race results from CSV exports.

Correlation Analysis Calculates the relationship between pre-race variables (Fitness, Fatigue, Form, Resting HR, HRV, Sleep) and race outcomes.

Xert Integration Includes specialized parsers for .tcx files to extract advanced power metrics and merge them with physiological data.

Outlier Identification Automatically flags "negative outliers" to help you analyze why certain races didn't go according to plan.

Visual Dashboards Generates publication-ready scatter plots and correlation heatmaps.

🛠️ Getting Started
Prerequisites
Python 3.10+

Pip (Python package manager)

Installation
Clone the repository

Bash

git clone https://github.com/your-username/intervals-agent.git
cd intervals-agent
Install dependencies

Bash

pip install -r requirements.txt
📊 Data Workflow
The analysis follows a three-step process to ensure data integrity:

Parsing: Extracting metrics from Intervals.icu (wellness) and Xert (performance).

Merging: Aligning timestamps to match pre-race metrics with specific event dates.

Scoring: Normalizing race results into a "Performance Score" for objective comparison.

🤝 Contributing
If we find ways to improve the correlation algorithms or add support for more platforms (like TrainingPeaks or Strava), feel free to open a Pull Request.