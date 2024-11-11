from flask import Flask
from config import Config
import logging

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize after app creation
from app.models.street_data import StreetData
street_data = StreetData()

# Import routes after app creation
from app.routes import main, street, geocoding, reports, analysis, nearby

# Make sure app is available for import
__all__ = ['app'] 