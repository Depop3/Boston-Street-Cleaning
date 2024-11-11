import os

class Config:
    SECRET_KEY = 'boston-street-cleaning-2024'
    DATA_PATH = 'app/data_processing/data.csv'
    GEOCODE_CACHE_PATH = 'geocode_cache.json'
    REPORTS_PATH = 'reports.json'
    DEBUG = True 