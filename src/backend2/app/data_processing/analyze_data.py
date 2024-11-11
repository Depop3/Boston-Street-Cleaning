import pandas as pd

def analyze_cleaning_patterns():
    df = pd.read_csv('data.csv')
    
    # Analyze districts
    district_counts = df['dist_name'].value_counts()
    print("\n=== Streets per District ===")
    print(district_counts)
    
    # Analyze cleaning times
    print("\n=== Common Cleaning Times ===")
    time_patterns = df.groupby(['start_time', 'end_time']).size()
    print(time_patterns)
    
    # Analyze which days are most common
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    day_counts = {day: df[day].sum() for day in days}
    print("\n=== Cleaning Days Distribution ===")
    for day, count in day_counts.items():
        print(f"{day.capitalize()}: {count} streets")

if __name__ == "__main__":
    analyze_cleaning_patterns() 