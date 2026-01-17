"""
Intervals.icu Race Analysis Agent - Main Data Fetcher

Description:
    This script connects to the Intervals.icu API to fetch an athlete's activity history.
    It filters for race activities, fetches associated wellness data (Sleep, HRV, Resting HR)
    and Training Load metrics (Fitness, Fatigue, Form), and calculates a custom
    'Performance Score' for each race.

    The output is saved to 'race_analysis.csv'.

Usage:
    python main.py

Dependencies:
    - requests
    - pandas
    - python-dotenv

Configuration:
    Requires a .env file with:
    - INTERVALS_API_KEY
    - INTERVALS_ATHLETE_ID
"""

import os
import requests
import csv
import pandas as pd
import io
from dotenv import load_dotenv
from datetime import date, timedelta, datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("INTERVALS_API_KEY")
ATHLETE_ID = os.getenv("INTERVALS_ATHLETE_ID")

if not API_KEY or not ATHLETE_ID:
    raise ValueError("Missing API_KEY or ATHLETE_ID in .env file.")

# --- Constants ---
OUTPUT_FILE = "race_analysis.csv"
BASE_URL = "https://intervals.icu/api/v1"

def get_auth():
    """Returns the authentication tuple for requests."""
    return ("API_KEY", API_KEY)

def fetch_activities(oldest_date, newest_date):
    """Fetches all activities within the specified date range."""
    url = f"{BASE_URL}/athlete/{ATHLETE_ID}/activities?oldest={oldest_date}&newest={newest_date}"
    print("Fetching all activities...")
    response = requests.get(url, auth=get_auth())
    response.raise_for_status()
    return response.json()

def fetch_wellness(oldest_date, newest_date):
    """Fetches wellness data for a specific date range."""
    url = f"{BASE_URL}/athlete/{ATHLETE_ID}/wellness?oldest={oldest_date}&newest={newest_date}"
    try:
        response = requests.get(url, auth=get_auth())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []

def get_weight_for_date(target_date, api_key, athlete_id):
    """
    Attempts to find the athlete's weight on the target date.
    Falls back to a +/- 30 day window if exact date is missing.
    """
    # Try exact date
    wellness = fetch_wellness(target_date.isoformat(), target_date.isoformat())
    if wellness and wellness[0].get('weight'):
        return wellness[0]['weight']

    # Fallback: Search +/- 30 days
    start_date = target_date - timedelta(days=30)
    end_date = target_date + timedelta(days=30)
    wellness_data = fetch_wellness(start_date.isoformat(), end_date.isoformat())
    
    if wellness_data:
        # Sort by proximity to target_date
        wellness_data.sort(key=lambda x: abs((datetime.strptime(x['id'], '%Y-%m-%d').date() - target_date).days))
        for entry in wellness_data:
            if entry.get('weight'):
                return entry['weight']
    return None

def process_races(activities):
    """Filters activities for races and aggregates metrics."""
    race_analysis_data = []
    
    print(f"Processing {len(activities)} activities. Filtering for races...")
    
    for activity in sorted(activities, key=lambda x: x['id']):
        # Only process activities flagged as 'race'
        if activity.get('race') is True:
            race_date_str = activity['start_date_local'].split('T')[0]
            race_date = datetime.strptime(race_date_str, '%Y-%m-%d').date()

            # Basic Race Data
            race_entry = {
                'Activity ID': activity['id'],
                'Date': race_date_str,
                'Name': activity['name'],
                'Type': activity['type'],
                'Average Speed (km/h)': round(activity.get('average_speed', 0) * 3.6, 2),
                'Kilojoules': activity.get('icu_joules'),
                'Distance (km)': round(activity.get('distance', 0) / 1000, 2),
                'Moving Time (minutes)': round(activity.get('moving_time', 0) / 60, 2),
                'Kilojoules/Hour': round(activity.get('icu_joules', 0) / (activity.get('moving_time', 1) / 3600), 2) if activity.get('moving_time', 1) > 0 else 0,
                'Max HR (in-race)': activity.get('max_heartrate'),
                'Variability': activity.get('icu_variability_index'),
                'Power/HR': activity.get('icu_power_hr'),
                'Efficiency Factor': activity.get('icu_efficiency_factor'),
                'Incident': None, 
            }

            # Weight & Power/Weight
            weight = get_weight_for_date(race_date, API_KEY, ATHLETE_ID)
            if activity.get('icu_weighted_avg_watts') and weight:
                race_entry['Power/Weight (W/kg)'] = round(activity['icu_weighted_avg_watts'] / weight, 2)
            else:
                race_entry['Power/Weight (W/kg)'] = None

            # --- Pre-Race Wellness (7 & 14 days) ---
            for days in [7, 14]:
                start_date = race_date - timedelta(days=days)
                wellness_data = fetch_wellness(start_date.isoformat(), race_date.isoformat())
                
                # Extract valid values
                resting_hrs = [e['restingHR'] for e in wellness_data if e.get('restingHR')]
                hrvs = [e['hrv'] for e in wellness_data if e.get('hrv')]
                sleeps = [e['sleepSecs'] for e in wellness_data if e.get('sleepSecs')]

                race_entry[f'Avg Resting HR ({days}-day pre-race)'] = round(sum(resting_hrs) / len(resting_hrs), 2) if resting_hrs else None
                race_entry[f'Avg HRV ({days}-day pre-race)'] = round(sum(hrvs) / len(hrvs), 2) if hrvs else None
                race_entry[f'Avg Sleep (hours, {days}-day pre-race)'] = round(sum(sleeps) / len(sleeps) / 3600, 2) if sleeps else None

            # --- PMC Data (Fitness/Fatigue) ---
            day_before = race_date - timedelta(days=1)
            pmc_data = fetch_wellness(day_before.isoformat(), day_before.isoformat())
            if pmc_data:
                race_entry['Fitness (CTL, day pre-race)'] = pmc_data[0].get('ctl')
                race_entry['Fatigue (ATL, day pre-race)'] = pmc_data[0].get('atl')
                race_entry['Form (Ramp Rate, day pre-race)'] = pmc_data[0].get('rampRate')

            race_analysis_data.append(race_entry)
            
    return race_analysis_data

def calculate_performance_score(df):
    """Calculates a normalized Performance Score based on key metrics."""
    if df.empty:
        return df
    
    # Helper to normalize series to 0-1 range
    def normalize(series):
        if series.max() == series.min(): return 0
        return (series - series.min()) / (series.max() - series.min())

    # 1. Speed (Higher is better)
    df['Normalized Speed'] = normalize(df['Average Speed (km/h)'])
    
    # 2. Efficiency Factor (Higher is better)
    df['Normalized Efficiency Factor'] = normalize(df['Efficiency Factor'])
    
    # 3. Kilojoules/Hour (Lower is often better for efficiency, inverted)
    # Note: This assumption depends on race type. For fixed distance, lower energy/time might mean better drafting?
    # Or simply normalizing the effort cost.
    if df['Kilojoules/Hour'].max() != df['Kilojoules/Hour'].min():
         df['Normalized Kilojoules/Hour'] = 1 - normalize(df['Kilojoules/Hour'])
    else:
         df['Normalized Kilojoules/Hour'] = 0

    # 4. Power/Weight (Higher is better)
    df['Normalized Power/Weight'] = normalize(df['Power/Weight (W/kg)'].fillna(0))

    # Sum normalized metrics
    df['Performance Score'] = (
        df['Normalized Speed'] + 
        df['Normalized Efficiency Factor'] + 
        df['Normalized Kilojoules/Hour'] + 
        df['Normalized Power/Weight']
    )
    return df

def main():
    try:
        # Define date range
        oldest_date = date(2000, 1, 1).isoformat()
        today = date.today().isoformat()

        # Fetch and Process
        activities = fetch_activities(oldest_date, today)
        race_data = process_races(activities)

        if race_data:
            df = pd.DataFrame(race_data)
            df = calculate_performance_score(df)
            
            df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
            print(f"Successfully saved race analysis data to {OUTPUT_FILE}")
        else:
            print("No races found.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()