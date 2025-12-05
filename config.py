"""Application configuration."""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    
    # Application settings
    APP_NAME = 'Coffee Roasting Operations'
    APP_VERSION = '1.0.0'


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # In production, these should be set via environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
