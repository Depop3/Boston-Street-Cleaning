import pandas as pd
from config import Config
from app import logger

class StreetData:
    def __init__(self):
        self.df = None
        self.load_data()

    def load_data(self):
        """Load and prepare street cleaning data"""
        try:
            logger.info("Loading data from CSV...")
            self.df = pd.read_csv(Config.DATA_PATH)
            self.df['st_name'] = self.df['st_name'].str.strip()
            self.df['dist_name'] = self.df['dist_name'].fillna('').str.strip()
            logger.info(f"Loaded {len(self.df)} street cleaning records")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def get_all_streets(self):
        """Return sorted list of unique street names"""
        return sorted(self.df['st_name'].unique())

    def get_street_data(self, street_name):
        """Get data for a specific street"""
        return self.df[self.df['st_name'].str.lower() == street_name.lower()]