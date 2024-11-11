import pandas as pd
import json
import os
from datetime import datetime

def explore_street_data():
    print("Current working directory:", os.getcwd())
    
    # Print list of files in current directory
    print("Files in directory:", os.listdir())
    
    # Read the CSV file
    df = pd.read_csv('data.csv')
    
    # Basic information about the dataset
    print("\n=== Dataset Overview ===")
    print(f"Total streets: {len(df)}")
    print(f"Total districts: {df['dist_name'].nunique()}")
    
    # Create schedule information
    df['cleaning_days'] = df.apply(
        lambda x: [day for day, value in 
                  {'Sunday': x['sunday'], 
                   'Monday': x['monday'],
                   'Tuesday': x['tuesday'],
                   'Wednesday': x['wednesday'],
                   'Thursday': x['thursday'],
                   'Friday': x['friday'],
                   'Saturday': x['saturday']}.items() 
                  if value],
        axis=1
    )
    
    # Create week frequency information
    df['week_frequency'] = df.apply(
        lambda x: [week for week, value in 
                  {'Week 1': x['week_1'],
                   'Week 2': x['week_2'],
                   'Week 3': x['week_3'],
                   'Week 4': x['week_4'],
                   'Week 5': x['week_5']}.items() 
                  if value],
        axis=1
    )
    
    print("\n=== Sample Street Schedule ===")
    sample = df.iloc[0]
    print(f"Street: {sample['st_name']}")
    print(f"District: {sample['dist_name']}")
    print(f"Time: {sample['start_time']} - {sample['end_time']}")
    print(f"Side: {sample['side']}")
    print(f"Cleaning days: {', '.join(sample['cleaning_days'])}")
    print(f"Weeks: {', '.join(sample['week_frequency'])}")

if __name__ == "__main__":
    explore_street_data() 