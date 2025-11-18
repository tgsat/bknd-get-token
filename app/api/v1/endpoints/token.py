from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from app.models.schemas import (
    TokenRequest, 
    TokenResponse, 
    ValidateTokenRequest, 
    ValidateTokenResponse,
    LogoutRequest,
    LogoutResponse,
    ErrorResponse
)
from app.services.arcgis_service import arcgis_service
from app.services.cache_service import cache_service
from app.utils.logger import api_logger

router = APIRouter()

@router.post(
    "/generate",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        408: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Generate ArcGIS Token",
    description="Generate a new ArcGIS token using username and password"
)
async def generate_token(request: TokenRequest):
    """
    Generate ArcGIS token with the following parameters:
    
    - **username**: ArcGIS username (required)
    - **password**: ArcGIS password (required)
    - **referer**: Referer URL for security (required)
    - **portal_url**: ArcGIS portal URL (optional, default: arcgis.com)
    - **expiration**: Token expiration in minutes (optional, default: 60)
    """
    try:
        api_logger.info(f"🎯 Token generation request for user: {request.username}")
        
        # Generate token using ArcGIS service
        token_data = await arcgis_service.generate_token(
            username=request.username,
            password=request.password,
            referer=str(request.referer),
            portal_url=str(request.portal_url),
            expiration=request.expiration
        )
        
        # Cache the token (optional)
        await cache_service.set_token(
            request.username,
            {
                "token": token_data.get('token'),
                "expires": token_data.get('expires'),
                "ssl": token_data.get('ssl', False)
            }
        )
        
        response = TokenResponse(
            token=token_data.get('token'),
            expires=token_data.get('expires'),
            ssl=token_data.get('ssl', False),
            username=request.username
        )
        
        api_logger.info(f"✅ Token generated successfully for {request.username}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"💥 Unexpected error in token generation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post(
    "/validate",
    response_model=ValidateTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate ArcGIS Token",
    description="Validate an existing ArcGIS token"
)
async def validate_token(request: ValidateTokenRequest):
    """
    Validate ArcGIS token with the following parameters:
    
    - **token**: ArcGIS token to validate (required)
    - **portal_url**: ArcGIS portal URL (optional)
    """
    try:
        api_logger.info("🔍 Token validation request")
        
        validation_result = await arcgis_service.validate_token(
            token=request.token,
            portal_url=str(request.portal_url)
        )
        
        response = ValidateTokenResponse(**validation_result)
        api_logger.info("✅ Token validation completed")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"💥 Unexpected error in token validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post(
    "/revoke",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Revoke ArcGIS Token",
    description="Revoke (logout) an ArcGIS token"
)
async def revoke_token(request: LogoutRequest):
    """
    Revoke ArcGIS token with the following parameters:
    
    - **username**: Username associated with token (required)
    - **token**: Token to revoke (required)
    - **portal_url**: ArcGIS portal URL (optional)
    """
    try:
        api_logger.info(f"🚪 Token revocation request for user: {request.username}")
        
        # Revoke token using ArcGIS service
        logout_result = await arcgis_service.logout(
            username=request.username,
            token=request.token,
            portal_url=str(request.portal_url)
        )
        
        # Clear cached token
        await cache_service.delete_token(request.username)
        
        response = LogoutResponse(**logout_result)
        api_logger.info(f"✅ Token revoked successfully for {request.username}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"💥 Unexpected error in token revocation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get(
    "/info",
    summary="Token Information",
    description="Get information about token endpoints"
)
async def token_info():
    """
    Get information about available token operations
    """
    return {
        "endpoints": {
            "generate": "Generate new ArcGIS token",
            "validate": "Validate existing ArcGIS token",
            "revoke": "Revoke (logout) ArcGIS token"
        },
        "notes": [
            "Tokens are not stored on the server for security",
            "Referer URL is required for token security",
            "Default token expiration is 60 minutes"
        ]
    }