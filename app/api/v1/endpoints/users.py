from fastapi import APIRouter, HTTPException, status
from app.utils.logger import api_logger

router = APIRouter()

@router.get(
    "/profile",
    summary="User Profile",
    description="Get user profile information"
)
async def get_user_profile():
    """
    Placeholder for user profile management
    """
    api_logger.info("👤 User profile endpoint called")
    return {
        "message": "User profile endpoint - under development",
        "planned_features": [
            "User preferences",
            "Token history",
            "Usage statistics"
        ]
    }

@router.get(
    "/history",
    summary="Token History", 
    description="Get user token history"
)
async def get_token_history():
    """
    Placeholder for token history tracking
    """
    api_logger.info("📊 Token history endpoint called")
    return {
        "message": "Token history endpoint - under development",
        "note": "This will track token usage per user"
    }