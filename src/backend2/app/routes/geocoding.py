from flask import request, jsonify
from app import app, logger
from app.services.geocoding import geocoding_service

@app.route('/api/geocode')
def geocode_intersection():
    address = request.args.get('address')
    try:
        coords = geocoding_service.get_coordinates(address)
        if not coords:
            return jsonify({'error': 'Could not geocode address'}), 404
        return jsonify(coords)
    except Exception as e:
        logger.error(f"Error geocoding address {address}: {str(e)}")
        return jsonify({'error': str(e)}), 500