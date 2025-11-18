from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, HttpUrl

# Request Schemas
class TokenRequest(BaseModel):
    username: str = Field(..., description="ArcGIS username")
    password: str = Field(..., description="ArcGIS password")
    referer: HttpUrl = Field(..., description="Referer URL for token security")
    portal_url: Optional[HttpUrl] = Field(
        default="https://www.arcgis.com/sharing/rest",
        description="ArcGIS portal URL"
    )
    expiration: Optional[int] = Field(
        default=60,
        ge=1,
        le=1440,
        description="Token expiration in minutes (1-1440)"
    )

class ValidateTokenRequest(BaseModel):
    token: str = Field(..., description="ArcGIS token to validate")
    portal_url: Optional[HttpUrl] = Field(
        default="https://www.arcgis.com/sharing/rest",
        description="ArcGIS portal URL"
    )

class LogoutRequest(BaseModel):
    username: str = Field(..., description="Username for logout")
    token: str = Field(..., description="Token to revoke")
    portal_url: Optional[HttpUrl] = Field(
        default="https://www.arcgis.com/sharing/rest",
        description="ArcGIS portal URL"
    )

# Response Schemas
class TokenResponse(BaseModel):
    token: str = Field(..., description="ArcGIS access token")
    expires: str = Field(..., description="Token expiration timestamp")
    ssl: bool = Field(..., description="SSL enabled flag")
    username: str = Field(..., description="Username associated with token")

class ValidateTokenResponse(BaseModel):
    valid: bool = Field(..., description="Token validation status")
    user: Optional[Dict[str, Any]] = Field(None, description="User information")
    error: Optional[Dict[str, Any]] = Field(None, description="Error details")

class LogoutResponse(BaseModel):
    success: bool = Field(..., description="Logout success status")
    message: str = Field(..., description="Logout message")
    username: str = Field(..., description="Username that was logged out")
    arcgis_response: Optional[Dict[str, Any]] = Field(None, description="ArcGIS response")

# Error Schemas
class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    timestamp: str = Field(..., description="Error timestamp")

# Health Schemas
class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")