import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

class APIAuthManager:
    def __init__(self, keys_file="api_keys.json"):
        self.keys_file = keys_file
        self.keys = self.load_keys()
    
    def load_keys(self):
        """Load API keys from file"""
        try:
            if os.path.exists(self.keys_file):
                with open(self.keys_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Load keys error: {str(e)}")
            return {}
    
    def save_keys(self):
        """Save API keys to file"""
        try:
            with open(self.keys_file, 'w') as f:
                json.dump(self.keys, f, indent=2)
        except Exception as e:
            print(f"Save keys error: {str(e)}")
    
    def generate_api_key(self, name="default"):
        """Generate new API key"""
        try:
            key = secrets.token_urlsafe(32)
            key_hash = hashlib.sha256(key.encode()).hexdigest()
            
            self.keys[key_hash] = {
                "name": name,
                "created_at": datetime.now().isoformat(),
                "last_used": None,
                "requests": 0,
                "active": True
            }
            
            self.save_keys()
            print(f"API key generated: {key}")
            return key
        except Exception as e:
            print(f"Key generation error: {str(e)}")
            return None
    
    def validate_api_key(self, key):
        """Validate API key"""
        try:
            key_hash = hashlib.sha256(key.encode()).hexdigest()
            
            if key_hash in self.keys:
                key_data = self.keys[key_hash]
                if key_data.get("active"):
                    key_data["last_used"] = datetime.now().isoformat()
                    key_data["requests"] += 1
                    self.save_keys()
                    return True
            
            return False
        except Exception as e:
            print(f"Validation error: {str(e)}")
            return False
    
    def revoke_api_key(self, key):
        """Revoke API key"""
        try:
            key_hash = hashlib.sha256(key.encode()).hexdigest()
            if key_hash in self.keys:
                self.keys[key_hash]["active"] = False
                self.save_keys()
                print(f"API key revoked")
                return True
            return False
        except Exception as e:
            print(f"Revoke error: {str(e)}")
            return False
    
    def get_key_stats(self, key):
        """Get API key statistics"""
        try:
            key_hash = hashlib.sha256(key.encode()).hexdigest()
            if key_hash in self.keys:
                return self.keys[key_hash]
            return None
        except Exception as e:
            print(f"Stats error: {str(e)}")
            return None

def require_api_key(f):
    """Decorator for API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_manager = APIAuthManager()
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({"error": "API key required"}), 401
        
        if not auth_manager.validate_api_key(api_key):
            return jsonify({"error": "Invalid API key"}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

if __name__ == "__main__":
    auth = APIAuthManager()
    key = auth.generate_api_key("test_key")
    print(f"Generated key: {key}")
    print(f"Valid: {auth.validate_api_key(key)}")
