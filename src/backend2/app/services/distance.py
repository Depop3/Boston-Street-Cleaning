from math import radians, sin, cos, sqrt, atan2

def calculate_distance(coord1, coord2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Radius of earth in miles
    R = 3959.87433
    
    # Calculate distance
    distance = R * c
    return distance

# Make sure to export the function
__all__ = ['calculate_distance']