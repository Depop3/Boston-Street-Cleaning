from flask import jsonify
from app import app, street_data, logger
from app.services.geocoding import geocoding_service
from app.utils.time_conversion import convert_to_12hr

@app.route('/api/street-details/<street_name>')
def street_details(street_name):
    try:
        street_data_df = street_data.get_street_data(street_name)
        if street_data_df.empty:
            return jsonify({'error': 'Street not found'}), 404

        schedules = []
        coords_cache = {}
        
        for _, row in street_data_df.iterrows():
            # Safely handle string and numeric values
            district = str(row['dist_name']).strip() if isinstance(row['dist_name'], str) else str(row['dist_name'])
            cache_key = f"{street_name}_{district}"
            
            # Use cached coordinates if available
            if cache_key in coords_cache:
                coords = coords_cache[cache_key]
            else:
                coords = geocoding_service.get_coordinates(street_name, district)
                coords_cache[cache_key] = coords

            if not coords:
                logger.warning(f"Could not geocode {street_name} in {district}")
                continue

            # Safely handle string values
            schedule = {
                'street': str(row['st_name']).strip() if isinstance(row['st_name'], str) else str(row['st_name']),
                'district': district,
                'lat': coords['lat'],
                'lng': coords['lng'],
                'time': f"{convert_to_12hr(str(row['start_time']))} - {convert_to_12hr(str(row['end_time']))}",
                'weeks': [i for i in range(1, 6) if str(row.get(f'week_{i}', '')).lower() == 't'],
                'days': [day for day in ['monday', 'tuesday', 'wednesday', 'thursday', 
                                       'friday', 'saturday', 'sunday'] 
                        if str(row.get(day, '')).lower() == 't'],
                'side': str(row.get('side', 'Even' if len(schedules) % 2 == 0 else 'Odd'))
            }
            
            # Safely handle optional fields
            if 'from_st' in row:
                val = row['from_st']
                schedule['from_street'] = str(val).strip() if isinstance(val, str) else str(val)
            
            if 'to_st' in row:
                val = row['to_st']
                schedule['to_street'] = str(val).strip() if isinstance(val, str) else str(val)
            
            if 'section' in row:
                val = row['section']
                schedule['section'] = str(val).strip() if isinstance(val, str) else str(val)
            
            if 'miles' in row:
                try:
                    schedule['miles'] = float(row['miles'])
                except (ValueError, TypeError):
                    logger.warning(f"Invalid miles value for {street_name}: {row['miles']}")
                    schedule['miles'] = None

            schedules.append(schedule)

        if not schedules:
            logger.warning(f"No valid schedules found for {street_name}")
            return jsonify({'error': 'No valid schedules found'}), 404

        return jsonify(schedules)
    
    except Exception as e:
        logger.error(f"Error in street_details: {str(e)}")
        return jsonify({'error': str(e)}), 500