"""
GoTo Connect API service for device and location management.
"""
import logging
import sys
import os
import requests
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import Config
from services.auth_service import AuthService

logger = logging.getLogger(__name__)

class GoToAPIService:
    """Service for interacting with GoTo Connect APIs."""
    
    def __init__(self, auth_service: AuthService):
        """
        Initialize the API service.
        
        Args:
            auth_service: Authentication service instance
        """
        self.auth_service = auth_service
        self.base_url = Config.GOTO_VOICE_ADMIN_API
    
    def _make_authenticated_request(self, method: str, endpoint: str, access_token: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Make an authenticated request to the GoTo API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            access_token: OAuth access token
            **kwargs: Additional request parameters
            
        Returns:
            Optional[Dict[str, Any]]: Response data or None if error
        """
        if not access_token:
            logger.error("No access token provided - cannot make API request")
            return None
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        
        try:
            response = requests.request(method.upper(), url, headers=headers, **kwargs)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.error("Authentication failed - token may be expired")
                return None
            else:
                logger.error(f"API request failed with status {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error making API request: {e}")
            return None
    
    def get_account_info(self, account_key: str, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get account information.
        
        Args:
            account_key: The account key
            access_token: OAuth access token
            
        Returns:
            Optional[Dict[str, Any]]: Account information
        """
        logger.info(f"Getting account info for account: {account_key}")
        return self._make_authenticated_request('GET', f'accounts/{account_key}', access_token)
    
    def get_locations(self, account_key: str, access_token: str, page_size: int = 50, page_marker: str = None) -> Optional[Dict[str, Any]]:
        """
        Get locations for an account.
        
        Args:
            account_key: The account key
            page_size: Number of items per page
            page_marker: Page marker for pagination
            
        Returns:
            Optional[Dict[str, Any]]: Locations data
        """
        logger.info(f"Getting locations for account: {account_key}")
        
        params = {
            'accountKey': account_key,
            'pageSize': page_size
        }
        
        if page_marker:
            params['pageMarker'] = page_marker
        
        return self._make_authenticated_request('GET', 'locations', access_token, params=params)
    
    def get_devices(self, account_key: str, access_token: str, page_size: int = 50, page_marker: str = None) -> Optional[Dict[str, Any]]:
        """
        Get devices for an account.
        
        Args:
            account_key: The account key
            page_size: Number of items per page
            page_marker: Page marker for pagination
            
        Returns:
            Optional[Dict[str, Any]]: Devices data
        """
        logger.info(f"Getting devices for account: {account_key}")
        
        params = {
            'accountKey': account_key,
            'pageSize': page_size
        }
        
        if page_marker:
            params['pageMarker'] = page_marker
        
        return self._make_authenticated_request('GET', 'devices', access_token, params=params)
    
    def get_device_details(self, device_id: str, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific device.
        
        Args:
            device_id: The device ID
            
        Returns:
            Optional[Dict[str, Any]]: Device details
        """
        logger.info(f"Getting device details for device: {device_id}")
        return self._make_authenticated_request('GET', f'devices/{device_id}', access_token)
    
    def get_location_devices(self, location_id: str, page_size: int = 50, page_marker: str = None) -> Optional[Dict[str, Any]]:
        """
        Get devices assigned to a specific location.
        
        Args:
            location_id: The location ID
            page_size: Number of items per page
            page_marker: Page marker for pagination
            
        Returns:
            Optional[Dict[str, Any]]: Devices assigned to the location
        """
        logger.info(f"Getting devices for location: {location_id}")
        
        params = {
            'pageSize': page_size
        }
        
        if page_marker:
            params['pageMarker'] = page_marker
        
        return self._make_authenticated_request('GET', f'locations/{location_id}/devices', params=params)
    
    def get_location_users(self, location_id: str, page_size: int = 50, page_marker: str = None) -> Optional[Dict[str, Any]]:
        """
        Get users assigned to a specific location.
        
        Args:
            location_id: The location ID
            page_size: Number of items per page
            page_marker: Page marker for pagination
            
        Returns:
            Optional[Dict[str, Any]]: Users assigned to the location
        """
        logger.info(f"Getting users for location: {location_id}")
        
        params = {
            'pageSize': page_size
        }
        
        if page_marker:
            params['pageMarker'] = page_marker
        
        return self._make_authenticated_request('GET', f'locations/{location_id}/users', params=params)
    
    def get_extensions(self, account_key: str, access_token: str, page_size: int = 50, page_marker: str = None) -> Optional[Dict[str, Any]]:
        """
        Get all extensions for an account.
        
        Args:
            account_key: The account key
            access_token: OAuth access token
            page_size: Number of extensions per page (default: 50)
            page_marker: Pagination marker for next page
            
        Returns:
            Optional[Dict[str, Any]]: Extensions data or None if error
        """
        logger.info(f"Getting extensions for account: {account_key}")
        
        params = {
            'accountKey': account_key,
            'pageSize': page_size
        }
        
        if page_marker:
            params['pageMarker'] = page_marker
        
        return self._make_authenticated_request('GET', 'extensions', access_token, params=params)
    
    def search_devices_by_location(self, account_key: str, access_token: str) -> List[Dict[str, Any]]:
        """
        Get all devices grouped by their locations.
        
        Args:
            account_key: The account key
            access_token: OAuth access token
            
        Returns:
            List[Dict[str, Any]]: Devices grouped by location
        """
        logger.info(f"Searching devices by location for account: {account_key}")
        
        # Get all locations
        locations_response = self.get_locations(account_key, access_token, page_size=100)
        if not locations_response or 'items' not in locations_response:
            logger.error("Failed to get locations")
            return []
        
        locations = locations_response['items']
        device_location_data = []
        
        for location in locations:
            location_id = location.get('id')
            location_name = location.get('name', 'Unknown Location')
            
            # Get devices for this location
            devices_response = self.get_location_devices(location_id, page_size=100)
            
            if devices_response and 'items' in devices_response:
                devices = devices_response['items']
                
                for device in devices:
                    device_info = {
                        'device_id': device.get('id'),
                        'device_status': device.get('status'),
                        'license_key': device.get('licenseKey'),
                        'location_id': location_id,
                        'location_name': location_name,
                        'location_address': location.get('address', {}),
                        'used_for_emergency': location.get('usedForEmergencyServices', False)
                    }
                    device_location_data.append(device_info)
        
        logger.info(f"Found {len(device_location_data)} devices across {len(locations)} locations")
        return device_location_data

    def get_phone_numbers(self, account_key: str, access_token: str, page_size: int = 50, page_marker: str = None) -> Optional[Dict[str, Any]]:
        """
        Get all phone numbers for the account.
        
        Args:
            account_key: The account key
            access_token: OAuth access token
            page_size: Number of items per page
            page_marker: Page marker for pagination
            
        Returns:
            Optional[Dict[str, Any]]: Phone numbers data
        """
        logger.info(f"Getting phone numbers for account: {account_key}")
        
        params = {
            'accountKey': account_key,
            'pageSize': page_size
        }
        
        if page_marker:
            params['pageMarker'] = page_marker
        
        return self._make_authenticated_request('GET', 'phone-numbers', access_token, params=params)

    def get_phone_number_details(self, phone_number_id: str, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific phone number.
        
        Args:
            phone_number_id: The phone number ID
            access_token: OAuth access token
            
        Returns:
            Optional[Dict[str, Any]]: Phone number details
        """
        logger.info(f"Getting phone number details for: {phone_number_id}")
        return self._make_authenticated_request('GET', f'phone-numbers/{phone_number_id}', access_token)

    def get_device_models(self, access_token: str, page_size: int = 50, page_marker: str = None) -> Optional[Dict[str, Any]]:
        """
        Get all available device models.
        
        Args:
            access_token: OAuth access token
            page_size: Number of items per page
            page_marker: Page marker for pagination
            
        Returns:
            Optional[Dict[str, Any]]: Device models data
        """
        logger.info("Getting device models")
        
        params = {
            'pageSize': page_size
        }
        
        if page_marker:
            params['pageMarker'] = page_marker
        
        return self._make_authenticated_request('GET', 'device-models', access_token, params=params)

    def get_device_button_configuration(self, device_id: str, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get button configuration for a specific device.
        
        Args:
            device_id: The device ID
            access_token: OAuth access token
            
        Returns:
            Optional[Dict[str, Any]]: Device button configuration
        """
        logger.info(f"Getting button configuration for device: {device_id}")
        return self._make_authenticated_request('GET', f'devices/{device_id}/buttons-configuration', access_token)

    def reboot_device(self, device_id: str, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Reboot a specific device.
        
        Args:
            device_id: The device ID
            access_token: OAuth access token
            
        Returns:
            Optional[Dict[str, Any]]: Operation result
        """
        logger.info(f"Rebooting device: {device_id}")
        return self._make_authenticated_request('POST', f'devices/{device_id}/reboot', access_token)

    def resync_device(self, device_id: str, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Resync a specific device.
        
        Args:
            device_id: The device ID
            access_token: OAuth access token
            
        Returns:
            Optional[Dict[str, Any]]: Operation result
        """
        logger.info(f"Resyncing device: {device_id}")
        return self._make_authenticated_request('POST', f'devices/{device_id}/resync', access_token)

    def get_extension_details(self, extension_id: str, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific extension.
        
        Args:
            extension_id: The extension ID
            access_token: OAuth access token
            
        Returns:
            Optional[Dict[str, Any]]: Extension details
        """
        logger.info(f"Getting extension details for: {extension_id}")
        return self._make_authenticated_request('GET', f'extensions/{extension_id}', access_token)