 # Import all route modules
from .main import *
from .street import *
from .geocoding import *
from .reports import *
from .analysis import *
from .nearby import *

# List all routes that should be imported
__all__ = [
    # Main routes
    'home',
    
    # Street routes
    'street_details',
    
    # Geocoding routes
    'geocode_intersection',
    
    # Report routes
    'submit_report',
    
    # Analysis routes
    'analysis',
    'analysis_data',
    
    # Nearby routes
    'get_nearby_streets'
]