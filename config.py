"""
Configuration file for the project
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# Model directories
MODELS_DIR = BASE_DIR / 'models'
CHECKPOINTS_DIR = MODELS_DIR / 'checkpoints'

# Upload directory
UPLOAD_DIR = BASE_DIR / 'uploads'

# Roast levels configuration
ROAST_LEVELS = {
    'light': 0,
    'light_medium': 1,
    'medium': 2,
    'medium_dark': 3,
    'dark': 4,
    'very_dark': 5
}

# Model configuration
MODEL_NAME = 'google/vit-base-patch16-224'
IMAGE_SIZE = 224
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
NUM_EPOCHS = 15

# API configuration
API_HOST = '0.0.0.0'
API_PORT = 5000
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB