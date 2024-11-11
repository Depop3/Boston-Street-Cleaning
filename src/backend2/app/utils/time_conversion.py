from datetime import datetime

def convert_to_12hr(time_str):
    """Convert 24-hour time to 12-hour format"""
    try:
        if not time_str or time_str == 'nan':
            return ''
        time_obj = datetime.strptime(str(time_str), '%H:%M:%S')
        return time_obj.strftime('%I:%M %p')
    except ValueError:
        return time_str

# Export the function
__all__ = ['convert_to_12hr'] 