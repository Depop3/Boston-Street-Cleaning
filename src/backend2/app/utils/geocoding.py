import requests
import logging

logger = logging.getLogger(__name__)

def geocode_address(address, district=None):
    """
    Geocode an address using Nominatim
    """
    try:
        # Add Boston, MA to the address if not already present
        if 'boston' not in address.lower():
            address = f"{address}, Boston, MA"
        
        # Add district if provided
        if district:
            address = f"{address}, {district}"

        # Use Nominatim geocoding service
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }
        
        headers = {
            'User-Agent': 'BostonStreetCleaning/1.0'
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        results = response.json()
        
        if results:
            return {
                'lat': float(results[0]['lat']),
                'lng': float(results[0]['lon'])
            }
        return None

    except Exception as e:
        logger.error(f"Geocoding error for {address}: {str(e)}")
        return None

# Make sure to export the function
__all__ = ['geocode_address']