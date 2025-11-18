import time
import json
import os
from typing import Optional


CACHE_DIR = "token_cache"
if not os.path.exists(CACHE_DIR):
os.makedirs(CACHE_DIR)




def cache_path(username: str) -> str:
safe = username.replace("/", "_")
return os.path.join(CACHE_DIR, f"{safe}.json")




def save_token(username: str, data: dict) -> None:
path = cache_path(username)
with open(path, "w", encoding="utf-8") as f:
json.dump(data, f)




def load_token(username: str) -> Optional[dict]:
path = cache_path(username)
if not os.path.exists(path):
return None
with open(path, "r", encoding="utf-8") as f:
return json.load(f)




def is_token_expired(token_data: dict) -> bool:
# ArcGIS returns 'expires' in milliseconds since epoch
now = int(time.time() * 1000)
return now >= int(token_data.get("expires", 0))




def clear_token(username: str) -> bool:
path = cache_path(username)
if os.path.exists(path):
os.remove(path)
return True
return False