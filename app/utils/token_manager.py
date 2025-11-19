import requests
import time
import threading
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class TokenManager:
    def __init__(self):
        self.current_token = None
        self.token_expiry = 0
        self.token_lock = threading.Lock()
        self.TOKEN_URL = "https://www.arcgis.com/sharing/rest/generateToken"
        
        # Setup session dengan retry mechanism
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get_token(self, username, password, referer):
        """Generate token baru"""
        params = {
            "username": username,
            "password": password,
            "referer": referer,
            "f": "json",
            "expiration": 60
        }
        
        try:
            response = self.session.post(self.TOKEN_URL, data=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "token" in data:
                return {
                    "success": True,
                    "token": data["token"],
                    "expires": data.get("expires", int(time.time()) + 7200),
                    "message": "Token berhasil di-generate"
                }
            else:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def validate_token(self, token, referer):
        """Validasi token"""
        if not token:
            return False
            
        validate_url = "https://www.arcgis.com/sharing/rest/generateToken"
        params = {
            "f": "json",
            "token": token
        }
        
        try:
            response = self.session.get(validate_url, params=params, timeout=10)
            data = response.json()
            return "error" not in data
        except:
            return False

# Global token manager instance
token_manager = TokenManager()