"""
Authentication service for GoTo Connect API integration.
"""
import logging
import os
import sys
import requests
from requests_oauthlib import OAuth2Session
from urllib.parse import urlencode
import json
from typing import Optional, Dict, Any

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import Config

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling GoTo Connect authentication."""
    
    def __init__(self):
        """Initialize the authentication service."""
        self.client_id = Config.GOTO_CLIENT_ID
        self.client_secret = Config.GOTO_CLIENT_SECRET
        self.redirect_uri = Config.GOTO_REDIRECT_URI
        self.auth_url = Config.GOTO_AUTH_URL
        self.token_url = Config.GOTO_TOKEN_URL
        self.scope = ['voice-admin.v1.read', 'voice-admin.v1.write']
    
    def get_authorization_url(self, state: str = None) -> tuple[str, str]:
        """
        Get the authorization URL for GoTo Connect OAuth flow.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            Tuple of (authorization_url, state)
        """
        try:
            oauth = OAuth2Session(
                self.client_id,
                scope=self.scope,
                redirect_uri=self.redirect_uri,
                state=state
            )
            
            authorization_url, state = oauth.authorization_url(self.auth_url)
            logger.info("Generated authorization URL")
            return authorization_url, state
            
        except Exception as e:
            logger.error(f"Error generating authorization URL: {e}")
            raise AuthenticationError(f"Failed to generate authorization URL: {e}")
    
    def exchange_code_for_token(self, authorization_code: str, state: str = None) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            authorization_code: Authorization code from callback
            state: State parameter for verification
            
        Returns:
            Token dictionary containing access_token, refresh_token, etc.
        """
        try:
            oauth = OAuth2Session(
                self.client_id,
                redirect_uri=self.redirect_uri,
                state=state
            )
            
            token = oauth.fetch_token(
                self.token_url,
                authorization_response=None,
                code=authorization_code,
                client_secret=self.client_secret
            )
            
            logger.info("Successfully exchanged authorization code for token")
            return token
            
        except Exception as e:
            logger.error(f"Error exchanging code for token: {e}")
            raise AuthenticationError(f"Failed to exchange code for token: {e}")
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an expired access token.
        
        Args:
            refresh_token: The refresh token
            
        Returns:
            New token dictionary
        """
        try:
            oauth = OAuth2Session(self.client_id)
            
            token = oauth.refresh_token(
                self.token_url,
                refresh_token=refresh_token,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            logger.info("Successfully refreshed access token")
            return token
            
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            raise AuthenticationError(f"Failed to refresh token: {e}")
    
    def is_token_valid(self, token: Dict[str, Any]) -> bool:
        """
        Check if a token is still valid.
        
        Args:
            token: Token dictionary to validate
            
        Returns:
            True if token is valid, False otherwise
        """
        if not token or 'access_token' not in token:
            return False
            
        # Simple validation - in production, you might want to check expiration
        try:
            # Make a simple API call to test the token
            headers = {'Authorization': f"Bearer {token['access_token']}"}
            response = requests.get(
                'https://api.jive.com/voice-admin/v1/accounts',
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.warning(f"Token validation failed: {e}")
            return False


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


class ConfigurationError(Exception):
    """Custom exception for configuration errors."""
    pass