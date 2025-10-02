"""
Configuration loader for FF Rankings
Centralizes all API key and secret loading
"""
import os
import json

def get_secrets_path():
    """Get the path to secrets.json"""
    return os.path.join(os.path.dirname(__file__), '..', '..', 'secrets.json')

def load_secrets():
    """Load all secrets from secrets.json"""
    try:
        with open(get_secrets_path(), 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load secrets.json: {e}")
        return {}

def get_api_key(service, default=''):
    """
    Get API key for a specific service

    Args:
        service: Service name (e.g., 'pff', 'subvertadown')
        default: Default value if key not found

    Returns:
        API key string
    """
    secrets = load_secrets()
    key_name = f'{service}_api_key' if service != 'subvertadown' else f'{service}_cookie'
    return secrets.get(key_name, default)

def get_pff_api_key():
    """Get PFF API key"""
    return get_api_key('pff', '0f6ca1f4-79d4-11ee-b962-0242ac120002')

def get_subvertadown_cookie():
    """Get Subvertadown session cookie"""
    return get_api_key('subvertadown', '')

def get_yahoo_credentials():
    """Get Yahoo OAuth credentials"""
    secrets = load_secrets()
    return {
        'access_token': secrets.get('access_token', ''),
        'consumer_key': secrets.get('consumer_key', ''),
        'consumer_secret': secrets.get('consumer_secret', ''),
        'refresh_token': secrets.get('refresh_token', ''),
        'token_time': secrets.get('token_time', 0),
        'token_type': secrets.get('token_type', 'bearer')
    }
