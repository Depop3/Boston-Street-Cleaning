from flask import render_template
from app import app, street_data

@app.route('/')
def home():
    streets = street_data.get_all_streets()
    return render_template('index.html', streets=streets)