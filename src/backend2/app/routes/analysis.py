from flask import render_template, jsonify
from app import app, street_data, logger

@app.route('/analysis')
def analysis():
    try:
        df = street_data.df
        stats = {
            'total_streets': len(df['st_name'].unique()),
            'total_districts': len(df['dist_name'].unique()),
            'total_miles': round(df['miles'].sum(), 2),
            'most_common_day': get_most_common_day(df)
        }
        
        return render_template('analysis.html', **stats)
                             
    except Exception as e:
        logger.error(f"Error rendering analysis page: {str(e)}")
        return "An error occurred loading the analysis page", 500

@app.route('/api/analysis-data')
def analysis_data():
    try:
        df = street_data.df
        
        # Get district statistics
        district_stats = df.groupby('dist_name').size().reset_index()
        district_stats.columns = ['name', 'count']
        districts = district_stats.to_dict('records')
        
        # Get schedule distribution
        schedule_distribution = [
            len(df[df[f'week_{week}'] == 't'])
            for week in range(1, 6)
        ]
        
        return jsonify({
            'districts': districts,
            'schedule_distribution': schedule_distribution
        })
        
    except Exception as e:
        logger.error(f"Error getting analysis data: {str(e)}")
        return jsonify({'error': str(e)}), 500

def get_most_common_day(df):
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_counts = {day: df[day].value_counts().get('t', 0) for day in days}
    return max(day_counts.items(), key=lambda x: x[1])[0].title()