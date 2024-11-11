import json
import time
import requests
from pathlib import Path
from app import logger

class GeocodingService:
    # District centers as fallback coordinates
    DISTRICT_CENTERS = {
        'North Dorchester': {'lat': 42.3097, 'lng': -71.0686},
        'South Dorchester': {'lat': 42.2844, 'lng': -71.0661},
        'Roxbury': {'lat': 42.3152, 'lng': -71.0914},
        'South End': {'lat': 42.3388, 'lng': -71.0765},
        'Back Bay': {'lat': 42.3503, 'lng': -71.0810},
        'Beacon Hill': {'lat': 42.3588, 'lng': -71.0707},
        'Charlestown': {'lat': 42.3782, 'lng': -71.0602},
        'East Boston': {'lat': 42.3702, 'lng': -71.0389},
        'South Boston': {'lat': 42.3381, 'lng': -71.0476},
        'West Roxbury': {'lat': 42.2798, 'lng': -71.1411},
        'Jamaica Plain': {'lat': 42.3097, 'lng': -71.1151},
        'Brighton': {'lat': 42.3464, 'lng': -71.1627},
        'Allston': {'lat': 42.3539, 'lng': -71.1337},
        'Hyde Park': {'lat': 42.2565, 'lng': -71.1241},
        'Roslindale': {'lat': 42.2875, 'lng': -71.1276}
    }

    def __init__(self):
        self.cache_file = Path('geocode_cache.json')
        self.cache = self._load_cache()
        self.last_request_time = 0
        self.min_delay = 1.0

    def get_coordinates(self, street, district):
        """Get coordinates with fallback to district center"""
        if not street or not district:
            logger.warning(f"Missing street or district: {street}, {district}")
            return self.DISTRICT_CENTERS.get(district)

        # Try different address formats
        attempts = [
            f"{street}, {district}, MA",
            f"{street}, Dorchester, MA" if 'Dorchester' in district else None,
            f"{street}, Boston, MA"
        ]

        for address in [a for a in attempts if a]:
            coords = self._try_geocode(address)
            if coords:
                return coords

        # Fallback to district center
        logger.info(f"Using district center for {district}")
        return self.DISTRICT_CENTERS.get(district)

    def _try_geocode(self, address):
        """Try to geocode a single address format"""
        cache_key = address.lower()
        
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            current_time = time.time()
            if current_time - self.last_request_time < self.min_delay:
                time.sleep(self.min_delay)

            response = requests.get(
                'https://nominatim.openstreetmap.org/search',
                params={
                    'q': address,
                    'format': 'json',
                    'limit': 1,
                    'countrycodes': 'us'
                },
                headers={'User-Agent': 'BostonStreetCleaning/1.0'},
                timeout=5
            )
            self.last_request_time = time.time()

            if response.status_code == 200:
                results = response.json()
                if results:
                    coords = {
                        'lat': float(results[0]['lat']),
                        'lng': float(results[0]['lon'])
                    }
                    self.cache[cache_key] = coords
                    self._save_cache()
                    return coords

        except Exception as e:
            logger.error(f"Geocoding error for {address}: {e}")

        return None

    def _load_cache(self):
        """Load the geocoding cache from file"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
        return {}

    def _save_cache(self):
        """Save the geocoding cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
        except Exception as e:
            logger.error(f"Error saving cache: {e}")

geocoding_service = GeocodingService()
# Export the service
__all__ = ['geocoding_service']