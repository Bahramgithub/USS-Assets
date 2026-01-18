import os
from flask import Flask, render_template, jsonify, send_from_directory
import json
from visual_tracker import VisualCarrierTracker

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'uss_carrier_map.html')

@app.route('/map')
def map_view():
    return send_from_directory('.', 'uss_carrier_map.html')

@app.route('/api/update')
def update_positions():
    """API endpoint to refresh carrier positions"""
    api_key = os.environ.get('MARINETRAFFIC_API_KEY')
    tracker = VisualCarrierTracker(api_key=api_key)
    report = tracker.generate_map_report()
    return jsonify(report)

@app.route('/api/status')
def get_status():
    """Get current carrier status"""
    try:
        with open('visual_carrier_report.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"error": "No data available"})

if __name__ == '__main__':
    # Generate initial map
    api_key = os.environ.get('MARINETRAFFIC_API_KEY')
    tracker = VisualCarrierTracker(api_key=api_key)
    tracker.generate_map_report()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)