from pydantic import BaseModel, Field


class LoginPayload(BaseModel):
username: str = Field(..., description="ArcGIS Online username")
password: str = Field(..., description="ArcGIS Online password")
referer: str = Field(..., description="Referer header or origin used for token generation")