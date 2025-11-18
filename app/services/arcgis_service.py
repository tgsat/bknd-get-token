import requests
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class ArcGISService:
    def __init__(self):
        self.timeout = 30
        
    async def generate_token(
        self,
        username: str,
        password: str,
        referer: str,
        portal_url: str = "https://www.arcgis.com/sharing/rest",
        expiration: int = 60
    ) -> Dict[str, Any]:
        """
        Generate ArcGIS token
        """
        params = {
            'username': username,
            'password': password,
            'referer': referer,
            'expiration': expiration,
            'f': 'json'
        }
        
        try:
            token_url = f"{portal_url}/generateToken"
            logger.info(f"🔑 Generating token for user: {username}")
            
            response = requests.post(
                token_url,
                data=params,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=self.timeout
            )
            
            response_data = response.json()
            
            if 'error' in response_data:
                error_msg = response_data.get('error', {}).get('message', 'Unknown error')
                logger.error(f"❌ ArcGIS error for {username}: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"ArcGIS Error: {error_msg}"
                )
            
            logger.info(f"✅ Token generated successfully for {username}")
            return response_data
            
        except requests.exceptions.Timeout:
            logger.error(f"⏰ Timeout generating token for {username}")
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Request timeout to ArcGIS server"
            )
        except requests.exceptions.ConnectionError:
            logger.error(f"🔌 Connection error generating token for {username}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cannot connect to ArcGIS server"
            )
        except Exception as e:
            logger.error(f"💥 Unexpected error for {username}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    async def validate_token(
        self,
        token: str,
        portal_url: str = "https://www.arcgis.com/sharing/rest"
    ) -> Dict[str, Any]:
        """
        Validate ArcGIS token
        """
        params = {
            'token': token,
            'f': 'json'
        }
        
        try:
            validate_url = f"{portal_url}/portals/self"
            logger.info(f"🔍 Validating token")
            
            response = requests.post(validate_url, data=params, timeout=self.timeout)
            response_data = response.json()
            
            if 'error' in response_data:
                logger.warning(f"⚠️ Token validation failed: {response_data['error']}")
                return {"valid": False, "error": response_data['error']}
            
            logger.info("✅ Token validation successful")
            return {"valid": True, "user": response_data.get('user')}
            
        except Exception as e:
            logger.error(f"💥 Token validation error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error validating token: {str(e)}"
            )
    
    async def logout(
        self,
        username: str,
        token: str,
        portal_url: str = "https://www.arcgis.com/sharing/rest"
    ) -> Dict[str, Any]:
        """
        Logout from ArcGIS (revoke token)
        """
        params = {
            'token': token,
            'f': 'json'
        }
        
        try:
            logout_url = f"{portal_url}/logout"
            logger.info(f"🚪 Logging out user: {username}")
            
            response = requests.post(logout_url, data=params, timeout=self.timeout)
            response_data = response.json()
            
            logger.info(f"✅ Logout successful for {username}")
            return {
                "success": True,
                "message": "Logout successful",
                "username": username,
                "arcgis_response": response_data
            }
            
        except Exception as e:
            logger.error(f"💥 Logout error for {username}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during logout: {str(e)}"
            )

# Global service instance
arcgis_service = ArcGISService()