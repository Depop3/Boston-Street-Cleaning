from flask import request, jsonify
from app import app, logger
from datetime import datetime
import json
import uuid

@app.route('/api/report', methods=['POST'])
def submit_report():
    try:
        report_data = request.json
        report_data.update({
            'timestamp': datetime.now().isoformat(),
            'id': str(uuid.uuid4())
        })
        
        # Load existing reports
        try:
            with open(app.config['REPORTS_PATH'], 'r') as f:
                reports = json.load(f)
        except FileNotFoundError:
            reports = []
        
        # Add new report
        reports.append(report_data)
        
        # Save updated reports
        with open(app.config['REPORTS_PATH'], 'w') as f:
            json.dump(reports, f, indent=2)
            
        logger.info(f"New report submitted for {report_data['street']}")
        
        return jsonify({
            'status': 'success', 
            'message': 'Report submitted successfully',
            'report_id': report_data['id']
        })
        
    except Exception as e:
        logger.error(f"Error submitting report: {str(e)}")
        return jsonify({'error': str(e)}), 500