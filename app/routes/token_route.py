from fastapi import APIRouter, HTTPException
from app.models.token_model import LoginPayload
from app.services.arcgis_service import get_valid_token
from utils.token_cache import clear_token


router = APIRouter(tags=["auth"])


@router.post("/auth/token")
def get_token(payload: LoginPayload):
res = get_valid_token(payload.username, payload.password, payload.referer)
if "error" in res:
# surface error message
raise HTTPException(status_code=400, detail=res["error"])
return {
"success": True,
"token": res["token"],
"expires": res["expires"],
"referer": res["referer"]
}




@router.post("/auth/logout")
def logout(payload: LoginPayload):
ok = clear_token(payload.username)
return {"success": True, "cache_cleared": ok}