import requests
import time
from utils.token_cache import load_token, save_token, is_token_expired


ARCGIS_TOKEN_URL = "https://www.arcgis.com/sharing/rest/generateToken"




def _build_token_payload(username: str, password: str, referer: str, expiration_minutes: int = 60):
return {
"username": username,
"password": password,
"referer": referer,
"f": "json",
"expiration": expiration_minutes,
}




def request_new_token(username: str, password: str, referer: str, expiration_minutes: int = 60):
payload = _build_token_payload(username, password, referer, expiration_minutes)
r = requests.post(ARCGIS_TOKEN_URL, data=payload, timeout=15)
r.raise_for_status()
data = r.json()


if "token" not in data:
# return the whole response so caller can surface errors
return {"error": data}


# ArcGIS returns 'expires' in milliseconds
token_data = {
"username": username,
"referer": referer,
"token": data["token"],
"expires": int(data.get("expires", 0)),
"issued": int(time.time() * 1000),
}


save_token(username, token_data)
return token_data




def get_valid_token(username: str, password: str, referer: str, expiration_minutes: int = 60):
# Load from cache
cache = load_token(username)


# If referer changed, regenerate token (referer is part of token scope)
if cache and cache.get("referer") != referer:
return request_new_token(username, password, referer, expiration_minutes)


# If cached and not expired -> return
if cache and not is_token_expired(cache):
return cache


# Otherwise request new token
return request_new_token(username, password, referer, expiration_minutes)