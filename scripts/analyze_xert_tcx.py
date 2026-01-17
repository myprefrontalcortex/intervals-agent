"""
Xert TCX File Analyzer

Description:
    This script parses a directory of .tcx files (Training Center XML) exported from Xert.
    It extracts key physiological metrics including:
    - Max and Average Power (Watts)
    - Max and Average Heart Rate (BPM)
    - Duration

    It uses multiprocessing to handle large numbers of files efficiently.

Usage:
    python scripts/analyze_xert_tcx.py

Output:
    Saves 'xert_metrics.csv' in the project root.
"""

import os
import glob
import time
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

# --- Configuration ---
TCX_DIR = 'Xert'
OUTPUT_FILE = 'xert_metrics.csv'
NAMESPACE = {
    'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
    'ext': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
}

def parse_tcx(file_path):
    """
    Parses a single TCX file to extract power, HR, and duration metrics.
    Returns a dictionary of metrics or None if parsing fails.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        activity = root.find('.//ns:Activity', NAMESPACE)
        if activity is None:
            return None
            
        activity_id = activity.find('ns:Id', NAMESPACE).text
        # Convert ID to date string (assuming it's ISO format like 2023-01-01T12:00:00Z)
        activity_date = activity_id.split('T')[0]
        
        watts_list = []
        heart_rates = []
        
        # Iterate through all Trackpoints
        for tp in root.findall('.//ns:Trackpoint', NAMESPACE):
            # Extract Watts
            watts_elem = tp.find('.//ext:Watts', NAMESPACE)
            if watts_elem is not None:
                watts_list.append(float(watts_elem.text))
            
            # Extract Heart Rate
            hr_elem = tp.find('.//ns:HeartRateBpm/ns:Value', NAMESPACE)
            if hr_elem is not None:
                heart_rates.append(float(hr_elem.text))

        if not watts_list:
            return None

        # Calculate Statistics
        avg_power = sum(watts_list) / len(watts_list)
        max_power = max(watts_list)
        avg_hr = sum(heart_rates) / len(heart_rates) if heart_rates else None
        max_hr = max(heart_rates) if heart_rates else None
        
        # Calculate duration from first and last timestamp
        times = [tp.find('ns:Time', NAMESPACE).text for tp in root.findall('.//ns:Trackpoint', NAMESPACE) if tp.find('ns:Time', NAMESPACE) is not None]
        duration_min = 0
        if len(times) > 1:
            try:
                t1 = datetime.fromisoformat(times[0].replace('Z', '+00:00'))
                t2 = datetime.fromisoformat(times[-1].replace('Z', '+00:00'))
                duration_min = (t2 - t1).total_seconds() / 60
            except ValueError:
                pass # Date parsing failed

        return {
            'Date': activity_date,
            'Xert_Max_Power': round(max_power, 1),
            'Xert_Avg_Power': round(avg_power, 1),
            'Xert_Max_HR': max_hr,
            'Xert_Avg_HR': round(avg_hr, 1) if avg_hr else None,
            'Xert_Duration_Min': round(duration_min, 1),
            'Xert_Filename': os.path.basename(file_path)
        }
    except Exception:
        # In production, logging errors to a file would be better than silence
        return None

def main():
    # Verify directory exists
    if not os.path.exists(TCX_DIR):
        print(f"Error: Directory '{TCX_DIR}' not found.")
        return

    tcx_files = glob.glob(os.path.join(TCX_DIR, '*.tcx'))
    total_files = len(tcx_files)
    print(f"Found {total_files} TCX files in '{TCX_DIR}' directory.")
    
    start_time = time.time()
    
    print("Starting processing with multiprocessing...")
    # Use ProcessPoolExecutor to utilize multiple CPU cores
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(parse_tcx, tcx_files))
        
    data = [r for r in results if r is not None]
            
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by='Date')
        
        df.to_csv(OUTPUT_FILE, index=False)
        
        end_time = time.time()
        print(f"Successfully processed {len(data)} files in {end_time - start_time:.2f} seconds.")
        print(f"Saved metrics to {OUTPUT_FILE}")
        print(df.head())
    else:
        print("No valid data found in TCX files.")

if __name__ == "__main__":
    main()
