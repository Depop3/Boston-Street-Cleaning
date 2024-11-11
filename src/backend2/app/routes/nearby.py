from flask import jsonify
from app import app, street_data, logger
from app.services.geocoding import GeocodingService
from app.services.distance import calculate_distance

geocoding_service = GeocodingService()

@app.route('/api/nearby/<street_name>')
def get_nearby_streets(street_name):
    try:
        street_name = street_name.strip()
        street_data_df = street_data.get_street_data(street_name)
        
        if street_data_df.empty:
            return jsonify({'error': 'Street not found'}), 404
            
        # Get coordinates for the source street
        street_row = street_data_df.iloc[0]
        street_coords = geocoding_service.get_coordinates(
            street_name, 
            district=street_row['dist_name']
        )
        
        if not street_coords:
            return jsonify({'error': 'Could not locate street'}), 404
            
        nearby = []
        seen_streets = set()
        
        # Find nearby streets
        for _, row in street_data.df.iterrows():
            if row['st_name'] == street_name or row['st_name'] in seen_streets:
                continue
                
            try:
                coords = geocoding_service.get_coordinates(
                    row['st_name'], 
                    district=row['dist_name']
                )
                
                if coords:
                    distance = calculate_distance(
                        (street_coords['lat'], street_coords['lng']),
                        (coords['lat'], coords['lng'])
                    )
                    
                    if distance <= 0.5:  # Within 0.5 miles
                        nearby.append({
                            'name': row['st_name'],
                            'district': row['dist_name'],
                            'distance': round(distance, 2)
                        })
                        seen_streets.add(row['st_name'])
                        
            except Exception as e:
                logger.error(f"Error processing nearby street {row['st_name']}: {str(e)}")
                continue

        # Sort by distance and return top 10
        nearby.sort(key=lambda x: x['distance'])
        return jsonify(nearby[:10])

    except Exception as e:
        logger.error(f"Error finding nearby streets: {str(e)}")
        return jsonify({'error': str(e)}), 500