"""
Main Flask application for GoTo Device Location Manager.
"""
import logging
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from config import Config
from services.auth_service import AuthService
from services.goto_api_service import GoToAPIService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    # Set the template and static folders to point to the app directory
    app = Flask(__name__, 
                template_folder='app/templates',
                static_folder='app/static')
    app.config.from_object(Config)
    
    # Initialize services
    auth_service = AuthService()
    api_service = GoToAPIService(auth_service)
    
    def is_authenticated():
        """Check if user is authenticated."""
        has_token = 'access_token' in session
        if has_token:
            token = session['access_token']
            # Simple check - just verify we have the basic token structure
            if isinstance(token, dict) and 'access_token' in token:
                logger.info("User is authenticated with valid token")
                return True
            else:
                logger.warning("Invalid token structure in session")
                return False
        else:
            logger.info("No access token in session")
            return False
    
    @app.route('/')
    def index():
        """Home page."""
        authenticated = is_authenticated()
        return render_template('index.html', 
                             is_authenticated=authenticated,
                             app_title=Config.APP_TITLE)
    
    @app.route('/authenticate')
    def authenticate():
        """Start OAuth authentication process."""
        try:
            # Generate a random state for CSRF protection
            import secrets
            state = secrets.token_urlsafe(32)
            
            authorization_url, returned_state = auth_service.get_authorization_url(state)
            session['oauth_state'] = returned_state
            
            logger.info(f"Starting OAuth flow with state: {returned_state}")
            return redirect(authorization_url)
        except Exception as e:
            logger.error(f"Authentication initiation failed: {e}")
            flash('Failed to start authentication. Please try again.', 'error')
            return redirect(url_for('index'))
    
    @app.route('/auth/callback')
    def auth_callback():
        """Handle OAuth callback."""
        try:
            code = request.args.get('code')
            state = request.args.get('state')
            error = request.args.get('error')
            
            logger.info(f"OAuth callback received - code: {'present' if code else 'missing'}, state: {state}")
            logger.info(f"Session state: {session.get('oauth_state')}")
            
            # Check for OAuth errors
            if error:
                flash(f'Authentication error: {error}', 'error')
                return redirect(url_for('index'))
            
            if not code:
                flash('Authentication was cancelled or failed.', 'error')
                return redirect(url_for('index'))
            
            # Verify state parameter
            session_state = session.get('oauth_state')
            if not session_state or state != session_state:
                logger.error(f"State mismatch - received: {state}, expected: {session_state}")
                flash('Authentication failed due to state mismatch. Please try again.', 'error')
                return redirect(url_for('index'))
            
            # Exchange code for token
            token = auth_service.exchange_code_for_token(code, state)
            session['access_token'] = token
            session.pop('oauth_state', None)
            
            flash('Authentication successful!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            logger.error(f"Authentication callback failed: {e}")
            flash('Authentication failed. Please try again.', 'error')
            return redirect(url_for('index'))
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            flash(f'Authentication error: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    @app.route('/logout')
    def logout():
        """Logout user."""
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        """Main dashboard."""
        logger.info(f"Dashboard accessed. Session keys: {list(session.keys())}")
        if not is_authenticated():
            logger.warning("Dashboard access denied - user not authenticated")
            flash('Please authenticate first.', 'warning')
            return redirect(url_for('index'))
        
        # Handle account key form submission
        if request.method == 'POST':
            account_key = request.form.get('account_key')
            if account_key:
                session['account_key'] = account_key
                flash('Account key updated successfully!', 'success')
            else:
                flash('Please enter an account key.', 'error')
        
        # Get account key from session or URL parameter
        account_key = session.get('account_key') or request.args.get('account_key')
        
        logger.info("Dashboard access granted - user authenticated")
        return render_template('dashboard.html', 
                             account_key=account_key,
                             app_title=Config.APP_TITLE)
    
    @app.route('/locations')
    def locations():
        """View locations."""
        if not is_authenticated():
            flash('Please authenticate first.', 'warning')
            return redirect(url_for('index'))
        
        # Get account key from session or URL parameter
        account_key = session.get('account_key') or request.args.get('account_key')
        if not account_key:
            flash('Please set your account key in the dashboard first.', 'warning')
            return redirect(url_for('dashboard'))
        
        # Update session with account key if it came from URL
        if request.args.get('account_key'):
            session['account_key'] = account_key
        
        try:
            access_token = session['access_token']['access_token']
            locations_data = api_service.get_locations(account_key, access_token)
            if locations_data is None:
                flash('Failed to fetch locations. Please try again.', 'error')
                return redirect(url_for('dashboard'))
            
            locations_list = locations_data.get('items', [])
            next_page_marker = locations_data.get('nextPageMarker')
            
            return render_template('locations.html', 
                                 locations=locations_list,
                                 account_key=account_key,
                                 next_page_marker=next_page_marker,
                                 app_title=Config.APP_TITLE)
        
        except Exception as e:
            logger.error(f"Error fetching locations: {e}")
            flash(f'Error fetching locations: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
    
    @app.route('/devices')
    def devices():
        """View devices."""
        if not is_authenticated():
            flash('Please authenticate first.', 'warning')
            return redirect(url_for('index'))
        
        # Get account key from session or URL parameter
        account_key = session.get('account_key') or request.args.get('account_key')
        if not account_key:
            flash('Please set your account key in the dashboard first.', 'warning')
            return redirect(url_for('dashboard'))
        
        # Update session with account key if it came from URL
        if request.args.get('account_key'):
            session['account_key'] = account_key
        
        try:
            access_token = session['access_token']['access_token']
            devices_data = api_service.get_devices(account_key, access_token)
            if devices_data is None:
                flash('Failed to fetch devices. Please try again.', 'error')
                return redirect(url_for('dashboard'))
            
            devices_list = devices_data.get('items', [])
            next_page_marker = devices_data.get('nextPageMarker')
            
            return render_template('devices.html', 
                                 devices=devices_list,
                                 account_key=account_key,
                                 next_page_marker=next_page_marker,
                                 app_title=Config.APP_TITLE)
        
        except Exception as e:
            logger.error(f"Error fetching devices: {e}")
            flash(f'Error fetching devices: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
    
    @app.route('/device-locations')
    def device_locations():
        """Show devices organized by locations"""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        account_key = session.get('account_key')
        if not account_key:
            logger.warning("No account key in session for device locations")
            return redirect(url_for('dashboard'))
        
        try:
            access_token = session.get('access_token')
            if not access_token:
                logger.error("No access token available")
                return redirect(url_for('index'))

            device_location_data = api_service.search_devices_by_location(account_key, access_token)
            logger.info(f"Retrieved {len(device_location_data)} device-location mappings")
            
            # Group devices by location
            location_groups = {}
            for item in device_location_data:
                location_name = item['location_name']
                if location_name not in location_groups:
                    location_groups[location_name] = {
                        'location': {
                            'name': location_name,
                            'id': item['location_id'],
                            'address': item['location_address'],
                            'usedForEmergencyServices': item['used_for_emergency']
                        },
                        'devices': []
                    }
                location_groups[location_name]['devices'].append(item)
            
            return render_template('device_locations.html', 
                                 location_groups=location_groups.values(),
                                 account_key=account_key)
        
        except Exception as e:
            logger.error(f"Error retrieving device locations: {str(e)}")
            return render_template('error.html', 
                                 error_message="Failed to retrieve device locations",
                                 error_details=str(e))

    @app.route('/phone-numbers')
    def phone_numbers():
        """View phone numbers."""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        account_key = session.get('account_key')
        if not account_key:
            logger.warning("No account key in session for phone numbers")
            return redirect(url_for('dashboard'))
        
        try:
            access_token = session.get('access_token')
            if not access_token:
                logger.error("No access token available")
                return redirect(url_for('index'))

            phone_numbers_response = api_service.get_phone_numbers(account_key, access_token['access_token'])
            phone_numbers = phone_numbers_response.get('items', []) if phone_numbers_response else []
            logger.info(f"Retrieved {len(phone_numbers)} phone numbers")
            
            return render_template('phone_numbers.html', 
                                 phone_numbers=phone_numbers,
                                 account_key=account_key)
        
        except Exception as e:
            logger.error(f"Error retrieving phone numbers: {str(e)}")
            return render_template('error.html', 
                                 error_message="Failed to retrieve phone numbers",
                                 error_details=str(e))

    @app.route('/extensions')
    def extensions():
        """Show all extensions for the account"""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        account_key = session.get('account_key')
        if not account_key:
            logger.warning("No account key in session for extensions")
            return redirect(url_for('dashboard'))
        
        try:
            access_token = session.get('access_token')
            if not access_token:
                logger.error("No access token available")
                return redirect(url_for('index'))

            extensions_response = api_service.get_extensions(account_key, access_token['access_token'])
            extensions = extensions_response.get('items', []) if extensions_response else []
            logger.info(f"Retrieved {len(extensions)} extensions")
            
            # Group extensions by type for better organization
            extension_groups = {}
            for ext in extensions:
                ext_type = ext.get('type', 'UNKNOWN')
                if ext_type not in extension_groups:
                    extension_groups[ext_type] = []
                extension_groups[ext_type].append(ext)
            
            return render_template('extensions.html', 
                                 extension_groups=extension_groups,
                                 account_key=account_key)
        
        except Exception as e:
            logger.error(f"Error retrieving extensions: {str(e)}")
            return render_template('error.html', 
                                 error_message="Failed to retrieve extensions",
                                 error_details=str(e))

    @app.route('/device-models')
    def device_models():
        """Show all available device models"""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        account_key = session.get('account_key')
        if not account_key:
            logger.warning("No account key in session for device models")
            return redirect(url_for('dashboard'))
        
        try:
            access_token = session.get('access_token')
            if not access_token:
                logger.error("No access token available")
                return redirect(url_for('index'))

            models_response = api_service.get_device_models(access_token['access_token'])
            device_models_list = models_response.get('items', []) if models_response else []
            logger.info(f"Retrieved {len(device_models_list)} device models")
            
            return render_template('device_models.html', 
                                 device_models=device_models_list,
                                 account_key=account_key)
        
        except Exception as e:
            logger.error(f"Error retrieving device models: {str(e)}")
            return render_template('error.html', 
                                 error_message="Failed to retrieve device models",
                                 error_details=str(e))

    @app.route('/device/<device_id>/reboot', methods=['POST'])
    def reboot_device(device_id):
        """Reboot a specific device"""
        if not is_authenticated():
            return jsonify({'success': False, 'message': 'Not authenticated'})
        
        account_key = session.get('account_key')
        if not account_key:
            return jsonify({'success': False, 'message': 'No account key in session'})
        
        try:
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({'success': False, 'message': 'No access token available'})

            result = api_service.reboot_device(device_id, access_token)
            logger.info(f"Device reboot initiated for: {device_id}")
            
            return jsonify({'success': True, 'message': 'Device reboot initiated successfully'})
        
        except Exception as e:
            logger.error(f"Error rebooting device: {str(e)}")
            return jsonify({'success': False, 'message': f'Failed to reboot device: {str(e)}'})

    @app.route('/device/<device_id>/resync', methods=['POST'])
    def resync_device(device_id):
        """Resync a specific device"""
        if not is_authenticated():
            return jsonify({'success': False, 'message': 'Not authenticated'})
        
        account_key = session.get('account_key')
        if not account_key:
            return jsonify({'success': False, 'message': 'No account key in session'})
        
        try:
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({'success': False, 'message': 'No access token available'})

            result = api_service.resync_device(device_id, access_token)
            logger.info(f"Device resync initiated for: {device_id}")
            
            return jsonify({'success': True, 'message': 'Device resync initiated successfully'})
        
        except Exception as e:
            logger.error(f"Error resyncing device: {str(e)}")
            return jsonify({'success': False, 'message': f'Failed to resync device: {str(e)}'})

    @app.route('/location/<location_id>')
    def location_detail(location_id):
        """View details for a specific location."""
        if not is_authenticated():
            flash('Please authenticate first.', 'warning')
            return redirect(url_for('index'))
        
        try:
            # Get devices for this location
            devices_data = api_service.get_location_devices(location_id)
            devices_list = devices_data.get('items', []) if devices_data else []
            
            # Get users for this location
            users_data = api_service.get_location_users(location_id)
            users_list = users_data.get('items', []) if users_data else []
            
            return render_template('location_detail.html', 
                                 location_id=location_id,
                                 devices=devices_list,
                                 users=users_list,
                                 app_title=Config.APP_TITLE)
        
        except Exception as e:
            logger.error(f"Error fetching location details: {e}")
            flash(f'Error fetching location details: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
    
    @app.route('/api/device/<device_id>')
    def api_device_details(device_id):
        """API endpoint to get device details."""
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        try:
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({'error': 'No access token available'}), 401
                
            device_data = api_service.get_device_details(device_id, access_token['access_token'])
            if device_data is None:
                return jsonify({'error': 'Device not found'}), 404
            
            return jsonify(device_data)
        
        except Exception as e:
            logger.error(f"Error fetching device details: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/device/<device_key>')
    def device_details(device_key):
        """Show device details page."""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        try:
            account_key = session.get('account_key')
            access_token = session.get('access_token')
            
            if not account_key:
                flash('Please set your account key in the dashboard first.', 'warning')
                return redirect(url_for('dashboard'))
            
            if not access_token:
                flash('Authentication required.', 'warning')
                return redirect(url_for('index'))
            
            # Get device details
            device_data = api_service.get_device_details(device_key, access_token['access_token'])
            
            if not device_data:
                flash('Device not found.', 'error')
                return redirect(url_for('devices'))
            
            return render_template('device_detail.html', 
                                 device=device_data, 
                                 account_key=account_key)
        
        except Exception as e:
            logger.error(f"Error loading device details: {str(e)}")
            flash(f'Error loading device details: {str(e)}', 'error')
            return redirect(url_for('devices'))

    @app.route('/device/<device_key>/location')
    def device_location(device_key):
        """Show device location details."""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        try:
            account_key = session.get('account_key')
            access_token = session.get('access_token')
            
            if not account_key:
                flash('Please set your account key in the dashboard first.', 'warning')
                return redirect(url_for('dashboard'))
            
            # Get device details first to get location info
            device_data = api_service.get_device_details(device_key, access_token['access_token'])
            
            if not device_data or not device_data.get('location'):
                flash('Device or location not found.', 'error')
                return redirect(url_for('devices'))
            
            location_id = device_data['location'].get('key') or device_data['location'].get('id')
            if location_id:
                return redirect(url_for('location_detail', location_id=location_id))
            else:
                flash('Location information not available for this device.', 'warning')
                return redirect(url_for('device_details', device_key=device_key))
        
        except Exception as e:
            logger.error(f"Error loading device location: {str(e)}")
            flash(f'Error loading device location: {str(e)}', 'error')
            return redirect(url_for('devices'))

    @app.route('/phone-number/<phone_number_id>')
    def phone_number_details(phone_number_id):
        """Show phone number details."""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        # Get account key from session
        account_key = session.get('account_key')
        if not account_key:
            flash('Please set your account key in the dashboard first.', 'warning')
            return redirect(url_for('dashboard'))
        
        try:
            access_token = session['access_token']['access_token']
            phone_number_data = api_service.get_phone_number_details(phone_number_id, access_token)
            
            if phone_number_data is None:
                flash('Phone number not found or access denied.', 'error')
                return redirect(url_for('phone_numbers'))
            
            return render_template('phone_number_detail.html', 
                                 phone_number=phone_number_data,
                                 account_key=account_key)
            
        except Exception as e:
            logger.error(f"Error loading phone number details: {str(e)}")
            flash(f'Error loading phone number details: {str(e)}', 'error')
            return redirect(url_for('phone_numbers'))

    @app.route('/favicon.ico')
    def favicon():
        """Serve favicon."""
        return '', 204
    
    @app.route('/reboot-device', methods=['POST'])
    def reboot_device_api():
        """API endpoint to reboot a device by key"""
        if not is_authenticated():
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        try:
            data = request.get_json()
            device_key = data.get('device_key')
            
            if not device_key:
                return jsonify({'success': False, 'error': 'Device key is required'})
            
            account_key = session.get('account_key')
            access_token = session.get('access_token')
            
            if not access_token:
                return jsonify({'success': False, 'error': 'No access token available'})
            
            result = api_service.reboot_device(device_key, access_token['access_token'])
            return jsonify({'success': True, 'result': result})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/resync-device', methods=['POST'])
    def resync_device_api():
        """API endpoint to resync a device by key"""
        if not is_authenticated():
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        try:
            data = request.get_json()
            device_key = data.get('device_key')
            
            if not device_key:
                return jsonify({'success': False, 'error': 'Device key is required'})
            
            account_key = session.get('account_key')
            access_token = session.get('access_token')
            
            if not access_token:
                return jsonify({'success': False, 'error': 'No access token available'})
            
            result = api_service.resync_device(device_key, access_token['access_token'])
            return jsonify({'success': True, 'result': result})
            return jsonify({'success': True, 'result': result})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/device-management')
    def device_management():
        """Device management interface"""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        try:
            account_key = session.get('account_key')
            access_token = session.get('access_token')
            
            if not account_key:
                flash('Please set your account key in the dashboard first.', 'warning')
                return redirect(url_for('dashboard'))
            
            devices_data = api_service.get_devices(account_key, access_token['access_token'])
            devices = devices_data.get('items', []) if devices_data else []
            
            return render_template('device_management.html', devices=devices)
        except Exception as e:
            flash(f'Error loading device management: {str(e)}', 'error')
            return redirect(url_for('dashboard'))

    @app.route('/extension/<extension_id>')
    def extension_details(extension_id):
        """Extension details view"""
        if not is_authenticated():
            return redirect(url_for('index'))
        
        try:
            # Extension details would require specific API endpoint
            flash('Extension details view not yet implemented', 'info')
            return redirect(url_for('extensions'))
        except Exception as e:
            flash(f'Error loading extension details: {str(e)}', 'error')
            return redirect(url_for('extensions'))

    @app.route('/debug/session')
    def debug_session():
        """Debug route to check session state."""
        if not Config.DEBUG:
            return "Debug mode only", 403
        
        return {
            'session_keys': list(session.keys()),
            'oauth_state': session.get('oauth_state'),
            'session_id': request.cookies.get('session')
        }
    
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler."""
        return render_template('404.html', app_title=Config.APP_TITLE), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler."""
        logger.error(f"Internal server error: {error}")
        return render_template('500.html', app_title=Config.APP_TITLE), 500
    
    return app

if __name__ == '__main__':
    try:
        Config.validate()
        app = create_app()
        
        logger.info(f"Starting {Config.APP_TITLE} on port {Config.PORT}")
        app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        print(f"Failed to start application: {e}")
        sys.exit(1)