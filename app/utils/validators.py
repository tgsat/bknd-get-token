import re
from typing import Optional
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """
    Validate URL format
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_username(username: str) -> bool:
    """
    Validate username format
    """
    if not username or len(username) < 3:
        return False
    # Basic username validation - adjust as needed
    return bool(re.match(r'^[a-zA-Z0-9_.-]+$', username))

def validate_referer(referer: str) -> bool:
    """
    Validate referer URL
    """
    return validate_url(referer)

def sanitize_input(input_string: str) -> str:
    """
    Basic input sanitization
    """
    if not input_string:
        return ""
    # Remove potentially dangerous characters
    return re.sub(r'[<>"\'&]', '', input_string)