import pandas as pd
from datetime import datetime
import os

print("Script is starting...")

def format_time(time_str):
    """Convert 24hr time to 12hr format"""
    time = datetime.strptime(time_str, '%H:%M')
    return time.strftime('%I:%M %p')

def search_street_schedule(street_name):
    try:
        print(f"\nSearching for: {street_name}")
        df = pd.read_csv('data.csv')
        
        # Case-insensitive search
        matches = df[df['st_name'].str.lower().str.contains(street_name.lower())]
        
        if len(matches) == 0:
            print("No streets found matching that name.")
            return
        
        for _, street in matches.iterrows():
            start_time = format_time(street['start_time'])
            end_time = format_time(street['end_time'])
            
            print(f"\n=== {street['st_name']} ===")
            print(f"District: {street['dist_name']}")
            print(f"Schedule: {start_time} - {end_time}")
            print(f"Side: {street['side']}")
            print(f"Location: From {street['from']} to {street['to']}")
            
            # Show which weeks
            weeks = []
            if street['week_1']: weeks.append('1st')
            if street['week_2']: weeks.append('2nd')
            if street['week_3']: weeks.append('3rd')
            if street['week_4']: weeks.append('4th')
            if street['week_5']: weeks.append('5th')
            print(f"Weeks of month: {', '.join(weeks)}")
            
            # Show which days
            days = []
            if street['monday']: days.append('Monday')
            if street['tuesday']: days.append('Tuesday')
            if street['wednesday']: days.append('Wednesday')
            if street['thursday']: days.append('Thursday')
            if street['friday']: days.append('Friday')
            if street['saturday']: days.append('Saturday')
            if street['sunday']: days.append('Sunday')
            print(f"Days: {', '.join(days)}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("\n=== Boston Street Cleaning Schedule Search ===")
    print("Type a street name to search (or 'quit' to exit)")
    print("Example searches: 'Beacon', 'Washington', 'Commonwealth'")
    
    while True:
        try:
            search_term = input("\nEnter street name: ")
            if search_term.lower() == 'quit':
                print("Goodbye!")
                break
            search_street_schedule(search_term)
        except Exception as e:
            print(f"Error in main loop: {str(e)}")