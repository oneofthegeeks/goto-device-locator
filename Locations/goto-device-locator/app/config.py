"""
Configuration module for the GoTo Device Location Manager.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Session configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # GoTo Connect API settings
    GOTO_CLIENT_ID = os.getenv('GOTO_CLIENT_ID')
    GOTO_CLIENT_SECRET = os.getenv('GOTO_CLIENT_SECRET')
    GOTO_REDIRECT_URI = os.getenv('GOTO_REDIRECT_URI', 'http://localhost:5000/auth/callback')
    GOTO_AUTH_URL = os.getenv('GOTO_AUTH_URL', 'https://authentication.logmeininc.com/oauth/authorize')
    GOTO_TOKEN_URL = os.getenv('GOTO_TOKEN_URL', 'https://authentication.logmeininc.com/oauth/token')
    
    # Application settings
    APP_TITLE = os.getenv('APP_TITLE', 'GoTo Device Location Manager')
    PORT = int(os.getenv('PORT', 5000))
    
    # API Base URLs
    GOTO_API_BASE = 'https://api.goto.com'
    GOTO_VOICE_ADMIN_API = f'{GOTO_API_BASE}/voice-admin/v1'
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        required_vars = ['GOTO_CLIENT_ID', 'GOTO_CLIENT_SECRET']
        missing = [var for var in required_vars if not getattr(cls, var)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True